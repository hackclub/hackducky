# 3XAYRemoteAccess
**Author**: Ayan Bindal (@3XAY) <br>
**Version**: 1.0 <br>
**Language**: DuckyScript 1.0

## Overview
My remote access script can be loaded onto a USB Rubber Ducky or a similar device to gain remote access to any Windows computer. The script itself is very short and will execute quickly, allowing you to remove it within a few seconds. The rest of the script will run without the USB Rubber Ducky to finish the installation. You can then control the computer via Discord. A small amount of setup is required the first time you use this tool, check the [Installation](#Installation) section for more information.

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