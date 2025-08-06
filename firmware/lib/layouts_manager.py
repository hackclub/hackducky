from adafruit_hid.keyboard import Keyboard
import usb_hid

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
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS as LayoutUS

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
from adafruit_hid.keycode import Keycode as KeycodeUS

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
