import board
import digitalio
import time
import usb_hid
import os
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

from layouts.keyboard_layout_win_fr import KeyboardLayout as LayoutFR
from layouts.keyboard_layout_win_de import KeyboardLayout as LayoutDE
from layouts.keyboard_layout_win_cz import KeyboardLayout as LayoutCZ
from layouts.keyboard_layout_win_da import KeyboardLayout as LayoutDA
from layouts.keyboard_layout_win_es import KeyboardLayout as LayoutES
from layouts.keyboard_layout_win_hu import KeyboardLayout as LayoutHU
from layouts.keyboard_layout_win_it import KeyboardLayout as LayoutIT
from layouts.keyboard_layout_win_po import KeyboardLayout as LayoutPO
from layouts.keyboard_layout_win_sw import KeyboardLayout as LayoutSW
from layouts.keyboard_layout_win_tr import KeyboardLayout as LayoutTR
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS as LayoutUS

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
    "us": LayoutUS(kbd)
}
layout = "us"

def flash_status():
    """Flash the onboard LED for visual feedback"""
    status_led.value = True
    time.sleep(0.1)
    status_led.value = False

def send_string(text):
    """Send a string as keyboard input"""
    print(layout)
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
                    kbd.press(Keycode.GUI, Keycode.SPACE)
                elif second_part == 'TAB':  
                    kbd.press(Keycode.GUI, Keycode.TAB)
                elif second_part == 'C':    
                    kbd.press(Keycode.GUI, Keycode.C)
                elif second_part == 'V':    
                    kbd.press(Keycode.GUI, Keycode.V)
                elif second_part == 'A':    
                    kbd.press(Keycode.GUI, Keycode.A)
                elif second_part == 'S':    
                    kbd.press(Keycode.GUI, Keycode.S)
                elif second_part == 'Z':   
                    kbd.press(Keycode.GUI, Keycode.Z)
                elif second_part == 'F':    
                    kbd.press(Keycode.GUI, Keycode.F)
                elif second_part == 'Q':    
                    kbd.press(Keycode.GUI, Keycode.Q)
                elif second_part == 'W':    
                    kbd.press(Keycode.GUI, Keycode.W)
                else:
                    kbd.press(Keycode.GUI)
                    send_string(parts[1])
                kbd.release_all()
            elif command == 'ENTER':
                kbd.press(Keycode.ENTER)
                kbd.release_all()
            elif command == "LAYOUT" and len(parts) == 2:
                global layout
                layout = parts[1].lower()
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