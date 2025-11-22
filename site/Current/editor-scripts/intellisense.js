// SOme basic completions for hackscript
monaco.languages.register({ id: "hackscript" });

monaco.languages.setMonarchTokensProvider("hackscript", {
    defaultToken: "identifier",
    ignoreCase: true,
    tokenizer: {
        root: [
            [/REM_BLOCK\b.*$/, { token: "comment", next: "@remBlock" }],
            [/REM\b\s*$/, { token: "comment", next: "@remBlock" }],
            [/REM\b.*$/, "comment"],
            [/STRING_LN\b\s*$/, { token: "keyword", next: "@stringLnBlock" }],
            [/STRINGLN\b\s*$/, { token: "keyword", next: "@stringLnBlock" }],
            [/STRING\b\s*$/, { token: "keyword", next: "@stringBlock" }],
            [
                /(STRING_LN|STRINGLN|STRING)\b(\s+)(.*$)/,
                ["keyword", "white", "string"],
            ],
            [
                /\b(END_STRING|END_STRINGLN|STRING_LN|STRINGLN|STRING_BLOCK|STRINGLN_BLOCK|DEFAULT_DELAY|DELAY|DEFINE|VAR|IF|ELSE|END_IF|WHILE|END_WHILE|FUNCTION|END_FUNCTION|RETURN|INJECT_MOD|RANDOM_(?:LOWERCASE_LETTER|UPPERCASE_LETTER|LETTER|NUMBER|SPECIAL|CHAR)|ENTER|ESCAPE|TAB|SPACE|SHIFT|ALT|CTRL|CONTROL|COMMAND|WINDOWS|GUI|CAPS_LOCK|NUM_LOCK|SCROLL_LOCK|UP_ARROW|DOWN_ARROW|LEFT_ARROW|RIGHT_ARROW|PAGE_UP|PAGE_DOWN|HOME|END|INSERT|DELETE|BACKSPACE|PAUSE|PRINT_SCREEN|MENU|APP|F\d{1,2})\b/,
                "keyword",
            ],
            // Idk classifying it as function doesn't do anything...
            [/[A-Za-z_][\w$]*(?=\s*\()/, "string"],
            [/\$[A-Za-z_]\w*/, "variable"],
            [/#\w+/, "type"],
            [/\d+/, "number"],
            [/==|!=|>=|<=|>|<|\+|-|\*|\/|%|\^|=/, "operator"],
        ],
        remBlock: [
            [/END_REM\b/, { token: "comment", next: "@pop" }],
            [/.*/, "comment"],
        ],
        stringBlock: [
            [/END_STRING\b/, { token: "keyword", next: "@pop" }],
            [/.*/, "string"],
        ],
        stringLnBlock: [
            [/END_STRINGLN\b/, { token: "keyword", next: "@pop" }],
            [/.*/, "string"],
        ],
    },
});

const hackScriptSuggestions = [
    {
        label: "REM",
        insertText: "REM ",
        documentation: "Single-line comment",
    },
    {
        label: "REM_BLOCK",
        insertText: "REM_BLOCK ${1:TITLE}\n\t$0\nEND_REM",
        insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
        documentation: "Start a multi-line comment block",
    },
    {
        label: "END_REM",
        insertText: "END_REM",
        documentation: "End a REM_BLOCK",
    },
    {
        label: "STRING",
        insertText: "STRING ",
        documentation: "Inject text",
    },
    {
        label: "STRINGLN",
        insertText: "STRINGLN ",
        documentation: "Inject text followed by Enter",
    },
    {
        label: "STRING_BLOCK",
        insertText: "STRING\n\t$0\nEND_STRING",
        insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
        documentation: "Inject multiple STRING lines as one block",
    },
    {
        label: "STRINGLN_BLOCK",
        insertText: "STRINGLN\n\t$0\nEND_STRINGLN",
        insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
        documentation: "Inject multi-line STRINGLN block",
    },
    {
        label: "DELAY",
        insertText: "DELAY ${1:100}",
        insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
        documentation: "Pause execution in ms",
    },
    {
        label: "DEFINE",
        insertText: "DEFINE #${1:NAME} ${2:value}",
        insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
        documentation: "Create a constant",
    },
    {
        label: "VAR",
        insertText: "VAR $${1:NAME} = ${2:value}",
        insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
        documentation: "Declare a variable",
    },
    {
        label: "IF",
        insertText: "IF ${1:condition}\n\t$0\nEND_IF",
        insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
        documentation: "Conditional block",
    },
    {
        label: "ELSE",
        insertText: "ELSE\n\t$0",
        insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
        documentation: "Else branch",
    },
    {
        label: "WHILE",
        insertText: "WHILE ${1:condition}\n\t$0\nEND_WHILE",
        insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
        documentation: "Loop while condition is true",
    },
    {
        label: "FUNCTION",
        insertText: "FUNCTION ${1:NAME}()\n\t$0\nEND_FUNCTION",
        insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
        documentation: "Define a function",
    },
    {
        label: "RETURN",
        insertText: "RETURN ${1:value}",
        documentation: "Return from function",
    },
    {
        label: "INJECT_MOD",
        insertText: "INJECT_MOD ${1:WINDOWS}",
        insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet,
        documentation: "Inject standalone modifier key",
    },
];

monaco.languages.registerCompletionItemProvider("hackscript", {
    provideCompletionItems: function (model, position) {
        const word = model.getWordUntilPosition(position);
        const range = {
            startLineNumber: position.lineNumber,
            endLineNumber: position.lineNumber,
            startColumn: word.startColumn,
            endColumn: word.endColumn,
        };
        return {
            suggestions: hackScriptSuggestions.map((item) => ({
                label: item.label,
                kind: monaco.languages.CompletionItemKind.Keyword,
                documentation: item.documentation,
                insertText: item.insertText,
                insertTextRules: item.insertTextRules,
                range,
            })),
        };
    },
});

const keystrokeKeywords = [
    { label: "ENTER", documentation: "Press the Enter key." },
    { label: "ESCAPE", documentation: "Press the Escape key." },
    { label: "TAB", documentation: "Press the Tab key." },
    { label: "SPACE", documentation: "Press the Space key." },
    { label: "UP_ARROW", documentation: "Press the Up Arrow key." },
    { label: "DOWN_ARROW", documentation: "Press the Down Arrow key." },
    { label: "LEFT_ARROW", documentation: "Press the Left Arrow key." },
    { label: "RIGHT_ARROW", documentation: "Press the Right Arrow key." },
    { label: "PAGE_UP", documentation: "Press the Page Up key." },
    { label: "PAGE_DOWN", documentation: "Press the Page Down key." },
    { label: "HOME", documentation: "Press the Home key." },
    { label: "END", documentation: "Press the End key." },
    { label: "INSERT", documentation: "Press the Insert key." },
    { label: "DELETE", documentation: "Press the Delete key." },
    { label: "BACKSPACE", documentation: "Press the Backspace key." },
    { label: "PAUSE", documentation: "Press the Pause key." },
    { label: "PRINT_SCREEN", documentation: "Press the Print Screen key." },
    { label: "MENU", documentation: "Press the Menu key." },
    { label: "APP", documentation: "Press the Application key." },
    { label: "CAPS_LOCK", documentation: "Toggle Caps Lock." },
    { label: "NUM_LOCK", documentation: "Toggle Num Lock." },
    { label: "SCROLL_LOCK", documentation: "Toggle Scroll Lock." },
    { label: "SHIFT", documentation: "Hold the Shift modifier." },
    { label: "ALT", documentation: "Hold the Alt modifier." },
    { label: "CONTROL", documentation: "Hold the Control modifier." },
    { label: "CTRL", documentation: "Hold the Ctrl modifier." },
    { label: "COMMAND", documentation: "Hold the Command modifier." },
    { label: "WINDOWS", documentation: "Hold the Windows modifier." },
    { label: "GUI", documentation: "Hold the GUI modifier." },
    { label: "F1", documentation: "Press the F1 key." },
    { label: "F2", documentation: "Press the F2 key." },
    { label: "F3", documentation: "Press the F3 key." },
    { label: "F4", documentation: "Press the F4 key." },
    { label: "F5", documentation: "Press the F5 key." },
    { label: "F6", documentation: "Press the F6 key." },
    { label: "F7", documentation: "Press the F7 key." },
    { label: "F8", documentation: "Press the F8 key." },
    { label: "F9", documentation: "Press the F9 key." },
    { label: "F10", documentation: "Press the F10 key." },
    { label: "F11", documentation: "Press the F11 key." },
    { label: "F12", documentation: "Press the F12 key." },
];

keystrokeKeywords.forEach(({ label, documentation }) => {
    hackScriptSuggestions.push({
        label,
        insertText: label + " ",
        documentation,
    });
});