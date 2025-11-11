import board
import digitalio
import storage
import usb_hid

program_pin = digitalio.DigitalInOut(board.GP0)
program_pin.direction = digitalio.Direction.INPUT
program_pin.pull = digitalio.Pull.UP

print("Boot.py: Starting...")
print("Boot.py: Configuring USB HID")
# HID is enabled even in programming mode because that makes it easier to debug.
usb_hid.enable((usb_hid.Device.KEYBOARD,))


if not program_pin.value:
    print("Boot.py: Entering programming mode")
    storage.remount("/", readonly=True)

else:
    print("Boot.py: Entering payload mode")
    storage.disable_usb_drive()

    try:
        # storage.remount("/", readonly=False)
        if usb_hid.devices:
            print("Boot.py: HID keyboard enabled successfully")
        else:
            print("Boot.py: WARNING - No HID devices available after enable")
    except Exception as e:
        print(f"Boot.py: Error enabling HID: {str(e)}")

print("Boot.py: Completed")
