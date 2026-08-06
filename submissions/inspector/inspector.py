import datetime
import socket
import platform
import psutil
import GPUtil
import requests


info = {}
info["timestamp"] = str(datetime.datetime.now())

info["hostname"] = socket.gethostname()
info["OS"] = platform.platform()

info["CPU"] =  platform.processor()
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