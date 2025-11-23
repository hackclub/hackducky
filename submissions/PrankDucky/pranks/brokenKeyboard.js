// ⌨️ Broken Keyboard - "Breaks" your keyboard

var shell = WScript.CreateObject("WScript.Shell");
var keys = ["{CAPSLOCK}", "{NUMLOCK}", "{SCROLLLOCK}"];

for (var i = 0; i < 200; i++) {
    var key = keys[Math.floor(Math.random() * keys.length)];
    shell.SendKeys(key);

    if (Math.random() < 0.1) {
        shell.Run("rundll32 user32.dll,MessageBeep -1");
    }

    WScript.Sleep(100 + Math.random() * 400);
}
