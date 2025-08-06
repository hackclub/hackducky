import board
import digitalio
import time
import usb_hid
import os

print("Main.py: Starting up...")
time.sleep(1)  # Reduced delay for testing

# Setup LED
status_led = digitalio.DigitalInOut(board.LED)
status_led.direction = digitalio.Direction.OUTPUT

def flash_error():
    while True:
        status_led.value = True
        time.sleep(0.1)
        status_led.value = False
        time.sleep(0.1)

# Initialize keyboard right away if we're in payload mode
try:
    print("Main.py: Checking USB HID devices...")
    if not usb_hid.devices:
        print("Main.py: No USB HID devices found!")
        flash_error()

    print(f"Main.py: Found {len(usb_hid.devices)} HID devices")
    from layouts_manager import *
    layout = "us"
    keycode = keycodes[layout]
    print("Main.py: Keyboard initialized successfully")

    # Test keyboard initialization
    kbd.release_all()
    print("Main.py: Keyboard test successful")


except Exception as e:
    print(f"Main.py: Failed to initialize keyboard: {str(e)}")
    flash_error()

def flash_status():
    """Flash the onboard LED for visual feedback"""
    status_led.value = True
    time.sleep(0.1)
    status_led.value = False

def send_string(text):
    """Send a string as keyboard input"""
    print(f"Sending string: {text}")
    layouts[layout].write(text)

def set_layout(lyt):
    if lyt not in list(layouts.keys()):
        raise Exception(f"Layout '{lyt}' is not a valid layout ({', '.join(list(layouts.keys()))})")
    global layout
    global keycode
    keycode = keycodes[lyt]
    layout = lyt

def press_modifier(parts, modifier_key):
    """Generic function to handle modifier key combinations (GUI, CTRL, SHIFT, ALT)"""
    if len(parts) < 2:
        return
        
    second_part = parts[1].upper()
    modifier_name = modifier_key.upper()
    
    print(f"Processing {modifier_name} command with {second_part}")
    
    # Get the modifier keycode attribute
    modifier_keycode = getattr(keycode, modifier_key.upper())
    
    if second_part == 'SPACE':
        kbd.press(modifier_keycode)
        time.sleep(0.1)
        kbd.press(keycode.SPACE)
        time.sleep(0.1)
        kbd.release_all()
        time.sleep(0.5)  # Add delay after modifier command
    elif second_part == 'CONTROL' or second_part == 'SHIFT' or second_part == 'ALT' or second_part == 'GUI':
        kbd.press(modifier_keycode)
        press_modifier(parts[2:], second_part)
        time.sleep(0.1)
        kbd.release_all()
        time.sleep(0.5)
    elif len(second_part) == 1 and second_part in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        kbd.press(modifier_keycode)
        time.sleep(0.1)
        if hasattr(keycode, second_part):
            kbd.press(getattr(keycode, second_part))
        else:
            # For characters that don't have direct keycode attributes
            layouts[layout].write(second_part.lower())
        time.sleep(0.1)
        kbd.release_all()
        time.sleep(0.5)  # Add delay after modifier command
    
    flash_status()

def interpret_ducky_script(filename):
    """Interpret a DuckyScript file and execute commands"""
    
    try:
        with open(filename, 'r', encoding='utf-8-sig') as file:
            default_delay = 0.2

            for line in file:
                try:
                    line = line.strip()
                    if not line or line.startswith('REM'):
                        continue

                    print(f"Processing line: {line}")
                    parts = line.split(' ', 1)
                    command = parts[0].upper()

                    if command == 'STRING' and len(parts) > 1:
                        print(f"Found STRING command with text: {parts[1]}")
                        # Add delay before typing
                        time.sleep(0.5)
                        send_string(parts[1])
                        flash_status()
                    elif command == 'LAYOUT' and len(parts) > 1:
                        set_layout(parts[1])
                    elif command == 'DELAY' and len(parts) > 1:
                        delay_time = float(parts[1]) / 1000.0
                        print(f"Delaying for {delay_time} seconds")
                        time.sleep(delay_time)
                    elif (command == 'GUI' or command == 'CTRL' or command == 'SHIFT' or command == 'ALT') and len(parts) > 1:
                        press_modifier(parts, command)
                    elif command == 'ENTER':
                        print("Sending ENTER")
                        kbd.press(keycode.ENTER)
                        time.sleep(0.1)
                        kbd.release_all()
                        # Add delay after ENTER
                        time.sleep(0.5)
                        flash_status()
                    elif command == 'TAB':
                        print("Sending TAB")
                        kbd.press(keycode.TAB)
                        time.sleep(0.1)
                        kbd.release_all()
                        # Add delay after TAB
                        time.sleep(0.5)
                        flash_status()
                    elif command == 'ESCAPE':
                        print("Sending ESCAPE")
                        kbd.press(keycode.ESCAPE)
                        time.sleep(0.1)
                        kbd.release_all()
                        # Add delay after ESCAPE
                        time.sleep(0.5)
                        flash_status()
                    elif command == 'SPACE':
                        print("Sending SPACE")
                        kbd.press(keycode.SPACE)
                        time.sleep(0.1)
                        kbd.release_all()
                        # Add delay after SPACE
                        time.sleep(0.5)
                        flash_status()
                    elif command == 'BACKSPACE':
                        print("Sending BACKSPACE")
                        kbd.press(keycode.BACKSPACE)
                        time.sleep(0.1)
                        kbd.release_all()
                        # Add delay after BACKSPACE
                        time.sleep(0.5)
                        flash_status()
                    elif command == 'DELETE':
                        print("Sending DELETE")
                        kbd.press(keycode.DELETE)
                        time.sleep(0.1)
                        kbd.release_all()
                        # Add delay after DELETE
                        time.sleep(0.5)
                        flash_status()
                    elif command[0] == 'F' and command[1:].isdigit():
                        key_num = int(command[1:])
                        if key_num in range(1, 13):
                            print(f"Sending F{key_num}")
                            kbd.press(getattr(keycode, f'F{key_num}'))
                            time.sleep(0.1)
                            kbd.release_all()
                            # Add delay after function key
                            time.sleep(0.5)
                            flash_status()
                    elif command == 'CAPSLOCK':
                        print("Toggling CAPSLOCK")
                        kbd.press(keycode.CAPS_LOCK)
                        time.sleep(0.1)
                        kbd.release_all()
                        # Add delay after CAPSLOCK
                        time.sleep(0.5)
                        flash_status()
                    elif command == 'LEFTARROW':
                        print("Sending LEFTARROW")
                        kbd.press(keycode.LEFT_ARROW)
                        time.sleep(0.1)
                        kbd.release_all()
                        # Add delay after LEFT_ARROW
                        time.sleep(0.5)
                        flash_status()
                    elif command == 'RIGHTARROW':
                        print("Sending RIGHTARROW")
                        kbd.press(keycode.RIGHT_ARROW)
                        time.sleep(0.1)
                        kbd.release_all()
                        # Add delay after RIGHT_ARROW
                        time.sleep(0.5)
                        flash_status()
                    elif command == 'UPARROW':
                        print("Sending UPARROW")
                        kbd.press(keycode.UP_ARROW)
                        time.sleep(0.1)
                        kbd.release_all()
                        # Add delay after UP_ARROW
                        time.sleep(0.5)
                        flash_status()
                    elif command == 'DOWNARROW':
                        print("Sending DOWNARROW")
                        kbd.press(keycode.DOWN_ARROW)
                        time.sleep(0.1)
                        kbd.release_all()
                        # Add delay after DOWN_ARROW
                        time.sleep(0.5)
                        flash_status()
                    elif command == 'HOME':
                        print("Sending HOME")
                        kbd.press(keycode.HOME)
                        time.sleep(0.1)
                        kbd.release_all()
                        # Add delay after HOME
                        time.sleep(0.5)
                        flash_status()
                    elif command == 'END':
                        print("Sending END")
                        kbd.press(keycode.END)
                        time.sleep(0.1)
                        kbd.release_all()
                        # Add delay after END
                        time.sleep(0.5)
                        flash_status()
                    elif command == 'PAGE_UP':
                        print("Sending PAGE_UP")
                        kbd.press(keycode.PAGE_UP)
                        time.sleep(0.1)
                        kbd.release_all()
                        # Add delay after PAGE_UP
                        time.sleep(0.5)
                        flash_status()
                    elif command == 'PAGE_DOWN':
                        print("Sending PAGE_DOWN")
                        kbd.press(keycode.PAGE_DOWN)
                        time.sleep(0.1)
                        kbd.release_all()
                        # Add delay after PAGE_DOWN
                        time.sleep(0.5)
                        flash_status()
                    elif command == 'DEFAULT_DELAY':
                        print("setting DEFAULT_DELAY")
                        default_delay = float(parts[1]) / 1000.0

                    time.sleep(default_delay)  # Default is 0.2 but customizable
                except Exception as line_error:
                    print(f"Error processing line '{line}': {str(line_error)}")
                    continue
    except Exception as e:
        print(f"Error reading file {filename}: {str(e)}")

# Main execution
print("Looking for ducky scripts...")
try:
    # Check for ducks directory in a CircuitPython-compatible way
    try:
        os.listdir('/ducks')
    except OSError:
        print("Creating /ducks directory")
        os.mkdir('/ducks')

    files = os.listdir('/ducks')
    ducky_files = sorted(['/ducks/' + f for f in files if f.endswith('.ducky')])
    print(ducky_files)
    if not ducky_files:
        print("No ducky scripts found")
        # Flash LED pattern to indicate no scripts
        for _ in range(3):
            flash_status()
            time.sleep(0.5)
    else:
        print(f"Found scripts: {ducky_files}")
        for script in ducky_files:
            print(f"Executing {script}")
            flash_status()
            try:
                interpret_ducky_script(script)
                time.sleep(1)
                print(f"Successfully executed {script}")
            except Exception as script_error:
                print(f"Error executing {script}: {str(script_error)}")
                # Flash error pattern but continue with next script
                for _ in range(2):
                    flash_status()
                    time.sleep(0.2)
except Exception as e:
    print(f"Fatal error: {str(e)}")
    while True:
        # Distinct error pattern
        for _ in range(3):
            flash_status()
            time.sleep(0.1)
        time.sleep(1)

print("Execution complete")