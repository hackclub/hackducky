import './intellisense.js'


// CREATE AN EDITOR
var h_div = document.getElementById('monaco_editor');
var editor = monaco.editor.create(h_div, {
    value: [
        'REM_BLOCK',
        '\tWelcome to the HackScript editor!',
        '\tHere you can test your script and see simulated keypresses!',
        '\tPS: Click the button on the right to open the HackScript reference :3',
        'END_REM'
    ].join('\n'),
    language: 'hackscript',
    theme: "vs-dark"
}, {
    storageService: {
        get() {},
        getBoolean(key) {
            if (key === "expandSuggestionDocs")
                return true;

            return false;
        },
        remove() {},
        store() {},
        onWillSaveState() {},
        onDidChangeStorage() {}
    }
});

window.editor = editor;

const runCompilerBtn = document.getElementById('run-compiler-btn');
const compilerScriptSelector = 'script[type="text/python"][data-compiler-script]';

runCompilerBtn.addEventListener('click', () => {
    const existing = document.querySelector(compilerScriptSelector);
    if (existing) existing.remove();
    
    const script = document.createElement('script');
    script.type = 'text/python';
    script.src = 'editor-scripts/compiler.bry';
    script.dataset.compilerScript = 'true';
    document.body.appendChild(script);
});