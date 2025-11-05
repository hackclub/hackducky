# HackDucky

The Hackclub themed USB rubber ducky ! - Check out [hackducky](https://hackclub.slack.com/archives/C08B8HZBC85)

# What is this?

HackDucky is Hackclub's own version of making a USB rubber ducky built by hackclubers. A usb rubber ducky is basically something that looks like a USB but is actually a trojan. It pretends to be a keyboard to the computer allowing you to basically take control of the computer you plug it into.
<br><br>
This is a payload written for a hackyducky consisting of:
  1. Basic duckyscript for setting up the second stage of the payload.
  2. An embedded python distribution with the Tkinter and pillow libraries installed.
  3. A python script that does the real work.

# How it works
## Stage 1 - DuckyScript
The victim plugs in the HackyDucky. If their OS is Windows, the script is executed.
  - It downloads the second stage
  - It downloads an embedded python distribution
  - It creates an elevated command prompt, then schedules a task to be run at login

## Stage 2 - Python Script
This script is executed after the next logon.
<br>
There are 3 main features:
  - Input manipulation - Random mouse clicks, random mouse movement, random caps lock, etc.
  - Cat images - Gets an image from the [CATAAS](https://cataas.com/) api and displays it in an unclosable, unminimisable window
  - Browser hijacking - Will randomly open an embarassing webpage (I don't have much of a list right now, give me some ideas)
All these features run in seperate threads, and will randomly occur to disrupt the user

# Licence
MIT Licence

# Disclaimer
This was created for educational purposes only. 
Please do not use this on a machine if you do not have permission to do so.
