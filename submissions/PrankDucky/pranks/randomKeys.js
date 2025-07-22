// 🗝️ Random Keys - Types random keys

var shell = WScript.CreateObject("WScript.Shell");
var chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()";

for (var i = 0; i < 300; i++) {
    var ch = chars[Math.floor(Math.random() * chars.length)];
    shell.SendKeys(ch);
    WScript.Sleep(40);
}
