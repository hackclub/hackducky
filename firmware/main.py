import board
import digitalio
import time
import usb_hid
import os
from adafruit_hid.keyboard import Keyboard

from layouts.keyboard_layout_win_fr import KeyboardLayout as LayoutFR
from layouts.keyboard_layout_win_de import KeyboardLayout as LayoutDE
from layouts.keyboard_layout_win_cz import KeyboardLayout as LayoutCZ
from layouts.keyboard_layout_win_da import KeyboardLayout as LayoutDA
from layouts.keyboard_layout_win_es import KeyboardLayout as LayoutES
from layouts.keyboard_layout_win_hu import KeyboardLayout as LayoutHU
from layouts.keyboard_layout_win_br import KeyboardLayout as LayoutBR
from layouts.keyboard_layout_win_it import KeyboardLayout as LayoutIT
from layouts.keyboard_layout_win_po import KeyboardLayout as LayoutPO
from layouts.keyboard_layout_win_sw import KeyboardLayout as LayoutSW
from layouts.keyboard_layout_win_tr import KeyboardLayout as LayoutTR
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS as LayoutUS #azerty

from layouts.keycode_win_br import Keycode as KeycodeBR
from layouts.keycode_win_cz import Keycode as KeycodeCZ
from layouts.keycode_win_da import Keycode as KeycodeDA
from layouts.keycode_win_de import Keycode as KeycodeDE
from layouts.keycode_win_es import Keycode as KeycodeES
from layouts.keycode_win_fr import Keycode as KeycodeFR
from layouts.keycode_win_hu import Keycode as KeycodeHU
from layouts.keycode_win_it import Keycode as KeycodeIT
from layouts.keycode_win_po import Keycode as KeycodePO
from layouts.keycode_win_sw import Keycode as KeycodeSW
from layouts.keycode_win_tr import Keycode as KeycodeTR
from layouts.keycode_win_uk import Keycode as KeycodeUK
from adafruit_hid.keycode import Keycode as KeycodeUS

print("Starting up...")
time.sleep(3)

status_led = digitalio.DigitalInOut(board.LED)
status_led.direction = digitalio.Direction.OUTPUT

kbd = Keyboard(usb_hid.devices)
layouts = {
    "fr": LayoutFR(kbd),
    "de": LayoutDE(kbd),
    "cz": LayoutCZ(kbd),
    "da": LayoutDA(kbd),
    "es": LayoutES(kbd),
    "hu": LayoutHU(kbd),
    "it": LayoutIT(kbd),
    "po": LayoutPO(kbd),
    "sw": LayoutSW(kbd),
    "tr": LayoutTR(kbd),
    "us": LayoutUS(kbd),
    "br": LayoutBR(kbd)
}
keycodes = {
    "fr": KeycodeFR,
    "de": KeycodeDE,
    "cz": KeycodeCZ,
    "da": KeycodeDA,
    "es": KeycodeES,
    "hu": KeycodeHU,
    "it": KeycodeIT,
    "po": KeycodePO,
    "sw": KeycodeSW,
    "tr": KeycodeTR,
    "us": KeycodeUS,
    "br": KeycodeBR
}
layout = "us"
keycode = keycodes[layout]

def flash_status():
    """Flash the onboard LED for visual feedback"""
    status_led.value = True
    time.sleep(0.1)
    status_led.value = False

def send_string(text):
    """Send a string as keyboard input"""
    layouts[layout].write(text)

def interpret_ducky_script(filename):
    """Interpret a DuckyScript file and execute commands"""
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith('REM'):
                continue

            parts = line.split(' ', 1)
            command = parts[0].upper()
            
            if command == 'STRING' and len(parts) > 1:
                send_string(parts[1])
            elif command == 'DELAY' and len(parts) > 1:
                time.sleep(float(parts[1]) / 1000.0)
            elif command == 'GUI' and len(parts) > 1:
                second_part = parts[1].upper()
                if second_part == 'SPACE':  
                    kbd.press(keycode.GUI, keycode.SPACE)
                elif second_part == 'TAB':  
                    kbd.press(keycode.GUI, keycode.TAB)
                elif second_part == 'C':    
                    kbd.press(keycode.GUI, keycode.C)
                elif second_part == 'V':    
                    kbd.press(keycode.GUI, keycode.V)
                elif second_part == 'A':    
                    kbd.press(keycode.GUI, keycode.A)
                elif second_part == 'S':    
                    kbd.press(keycode.GUI, keycode.S)
                elif second_part == 'Z':   
                    kbd.press(keycode.GUI, keycode.Z)
                elif second_part == 'F':    
                    kbd.press(keycode.GUI, keycode.F)
                elif second_part == 'Q':    
                    kbd.press(keycode.GUI, keycode.Q)
                elif second_part == 'W':    
                    kbd.press(keycode.GUI, keycode.W)
                else:
                    kbd.press(keycode.GUI)
                    send_string(parts[1])
                kbd.release_all()
            elif command == 'ENTER':
                kbd.press(keycode.ENTER)
                kbd.release_all()
            elif command == "LAYOUT" and len(parts) == 2:
                desired_layout = parts[1].lower()
                if desired_layout not in list(layouts.keys()):
                    raise Exception(f"Layout '{desired_layout}' not found in layouts {list(layouts.keys())}")
                global layout
                layout = desired_layout
                keycode = keycodes[layout]
            time.sleep(0.1)

def execute_ducky_scripts():
    """Find and execute all .ducky scripts in order"""
    ducky_files = []

    print("Checking for ducky scripts...")
    
    try:
        files = os.listdir('/ducks')
        ducky_files = ['/ducks/' + f for f in files if f.endswith('.ducky')]
        print(f"Found files: {ducky_files}")
    except OSError as e:
        print(f"Error accessing directory: {e}")
        return

    if not ducky_files:
        print("No ducky scripts found")
        return
    
    ducky_files.sort()
    
    for script in ducky_files:
        flash_status()  
        print(f"Attempting to execute {script}")
        try:
            with open(script, 'r') as f:
                print(f"Script contents: {f.read()}")
            interpret_ducky_script(script)
            time.sleep(1)  
        except Exception as e:
            print(f"Error executing {script}: {e}")

print("BadUSB starting...")
flash_status()  
execute_ducky_scripts()
print("BadUSB execution complete")