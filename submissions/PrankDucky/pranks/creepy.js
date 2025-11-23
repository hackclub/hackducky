// 👻 Creepy - Says creepy stuff every 83.2 seconds(ik super specific)
var shell = WScript.CreateObject("WScript.Shell");
var voice = WScript.CreateObject("SAPI.SpVoice");

var messages = [
    "I'm watching you...",
    "Are you alone?",
    "Something's behind you!",
    "The cake is a lie.",
];

for (var i = 0; i < 10; i++) {
    var msg = messages[Math.floor(Math.random() * messages.length)];
    voice.Speak(msg);
    WScript.Sleep(83200);
}
