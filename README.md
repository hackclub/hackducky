# HackDucky - New YSWS!

The hackclub themed USB rubber ducky ! - Check out [hackducky](https://hackclub.slack.com/archives/C08B8HZBC85)

# What is this?

Hackducky is hackclubs own version of making a USB rubber ducky built by hackclubers.A usb rubber ducky is basically something that looks like a USB but is actually a trojan. It pretends to be a keyboard to the computer allowing you to basically take control of the computer you plug it into

## What you get

- Hackducky Board
    -  Dual USB ports (USB-A and USB-C)
    -  LED for the status and spare LED!- you can use it for other things if you like !
    -  Button for any extra features you may want to add !
    -  Debug points to use it as a devboard!


## Getting Started

1. Follow the guide on the website! - hackducky.hackclub.com
2. A quick reference of all supported features for the ducky may be found [here](https://github.com/x-9917638/hackducky/blob/main/reference.md)

# Submission Criteria  

## 1. Time Requirement  
- **Tracking:** Minimum of **5** hours tracked with hackatime .
- Note on the requirements. I understand it doesnt take 5 hours to build a single script or even many in duckyscript so here's what you can do, If you want to excecute a python file then compile the file to exe or whatever excecutable form you need, Upload it somewhere public and then create a simple duckyscript to download and run it. You can totally spend more time on the python script and make it complex or for the challenge spend 5 hours on your duckyscript!  

## 2. Originality  
- Your project must be an **original idea** and not a direct copy from a tutorial.  
- Tutorials can be referenced, but your submission should be your own creation.  

## 3. Submission Limit  
- You can submit **multiple projects**, but you can only receive **one HackDucky**.  


# Setup Guide

We ship a raw hackducky to you. There is no firmware preinstalled. These steps will help you get started with the ducky!

## Step 1: Flashing CircuitPython to the board.
1. Head to the [Raspberry Pi Pico 2 CircuitPython download page](https://circuitpython.org/board/raspberry_pi_pico2/)
2. Download the .uf2 firmware.
3. Plug in your HackDucky. A new drive named RPI-RP2 should appear.
4. Drag and drop the .uf2 firmware into the drive.
5. Eject the HackDucky, then plug it back in. If a drive named CIRCUITPYTHON appears, it was successful!

## Step 2: Installing the firmware.
1. Clone this repo: `git clone https://github.com/hackclub/hackducky`
2. Open the folder.
3. Copy all the files in the firmware folder into the CIRCUITPYTHON drive.
4. Make sure to choose to **replace** existing files, then **delete the existing code.py file.**
5. Now head to the [adafruit bundle release page](https://github.com/adafruit/Adafruit_CircuitPython_Bundle/releases/)
6. Download the file that looks like **adafruit-circuitpython-bundle-10.x-mpy-YYYYMMDD**
7. Unzip the file.
8. From the folder created, copy the **lib** folder to the HackDucky.

## Step 3: Adding your script
1. Delete any existing files in the **ducks** folder on your HackDucky.
2. Copy your script into the **ducks** folder with the extension **.ducky**


# Troubleshooting/FAQ

## Read-only filesystem / I don't see a drive, how do I add my script?
Your Ducky is in payload mode.

Press and hold the programming pin (the pin closest to the USB-A port) while plugging it in.

## What the LED indicators mean?

- Triple blink: Startup Sequence
- Single blink: Working/Processing - running/Starting Execution
- Rapid blinking: DuckyScript is incorrect / Firmware broke 😭 - Create a PR or new issue desribing the firmware problem

## My script isn't working!
- Make sure you are not in programming mode: pull and plug back in
- If that didn't work:
  - Open the file debug.log.
  - Check for ERROR lines. 
  - If the error is complaining about your script, check your syntax.
  - If it isn't, create an issue!

## The keyboard is not recognised!:
- Try different USB port
- Check USB connection
- Verify target system supports USB HID

# Safety Notes

- pls dont hack people with this pls - its only ethical
