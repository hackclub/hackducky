
import { useState } from "react";
import { Button } from "@/components/ui/button";

const Terminal = () => {
  const [input, setInput] = useState("");
  const [history, setHistory] = useState<string[]>([
    "Welcome to HackDucky Terminal! 🦆",
    "Type 'help' to see available commands"
  ]);

  const easterEggCommands = {
    'duck': "🦆 Quack! You found the duck command! 🦆",
    'quack': "🦆 QUACK QUACK QUACK! 🦆",
    'hack': "🔓 Access granted! Welcome, hacker! 🔓",
    'matrix': "Wake up, Neo... The Matrix has you... 🕶️",
    'coffee': "☕ Error: Coffee not found. Please insert coffee to continue.",
    'sudo': "🚫 Nice try! But this duck doesn't fall for sudo tricks.",
    'rm -rf /': "💀 Whoa there, cowboy! That's a dangerous command!",
    'hello': "👋 Hello, fellow hacker! Welcome to HackDucky!",
    'cat': "🐱 Meow! Wrong animal, try 'duck' instead!",
    'ls': "📁 ducky_scripts/ 3d_models/ secrets/ definitely_not_backdoors/",
    'whoami': "🦆 You are a rubber duck debugging expert!",
    'date': `📅 It's ${new Date().toLocaleDateString()} - Perfect day for hacking!`,
    'pwd': "📍 /home/hackducky/pond",
    'echo hello world': "Hello World! 🌍",
    'ping google.com': "🏓 PONG! (64 bytes from google.com)",
    'fortune': "🔮 Fortune says: Your rubber duck will bring great debugging luck!",
    '42': "🤖 The Answer to the Ultimate Question of Life, the Universe, and Everything!",
    'konami': "🕹️ Try the Konami code on the main page! (↑↑↓↓←→←→BA)"
  };

  const handleCommand = (e: React.FormEvent) => {
    e.preventDefault();
    if (input.trim() === "") return;

    const newHistory = [...history, `$ ${input}`];
    const command = input.toLowerCase().trim();
    
    if (command.includes("help")) {
      newHistory.push("Available commands: help, clear, submit");
      newHistory.push("🦆 Secret commands: Try 'duck', 'quack', 'hack', 'matrix', 'coffee'...");
    } else if (command.includes("clear")) {
      setHistory([
        "Welcome to HackDucky Terminal! 🦆",
        "Type 'help' to see available commands"
      ]);
      setInput("");
      return;
    } else if (command.includes("submit")) {
      newHistory.push("Redirecting to submission page...");
      setTimeout(() => {
        window.location.href = "/submit";
      }, 1000);
    } else if (easterEggCommands[command]) {
      newHistory.push(easterEggCommands[command]);
    } else if (command.includes("exit") || command.includes("quit")) {
      newHistory.push("🚪 Nice try! But you can't escape the duck that easily! 🦆");
    } else if (command.includes("virus") || command.includes("malware")) {
      newHistory.push("🛡️ Error: Antivirus duck activated! Malware blocked! 🦆");
    } else if (command.includes("password")) {
      newHistory.push("🔐 Password hint: It's probably 'password123' 😅");
    } else {
      newHistory.push(`Command not found: ${input}`);
      newHistory.push("💡 Tip: Try some creative commands! This duck has secrets...");
    }
    
    setHistory(newHistory);
    setInput("");
  };

  return (
    <div className="bg-card border border-border rounded-lg p-6 font-mono text-sm terminal-glow">
      <div className="flex items-center justify-between mb-4">
        <div className="flex space-x-2">
          <div className="w-3 h-3 rounded-full bg-destructive cursor-pointer" 
               onClick={() => alert("🦆 You can't close the duck terminal! 🦆")}></div>
          <div className="w-3 h-3 rounded-full bg-yellow-500 cursor-pointer"
               onClick={() => alert("🦆 Minimize? More like duck-imize! 🦆")}></div>
          <div className="w-3 h-3 rounded-full bg-primary cursor-pointer"
               onClick={() => alert("🦆 Maximum duck power activated! 🦆")}></div>
        </div>
        <span className="text-muted-foreground">hackducky-terminal</span>
      </div>
      
      <div className="space-y-1 mb-4 h-64 overflow-y-auto">
        {history.map((line, index) => (
          <div key={index} className={line.startsWith('$') ? "text-primary" : "text-muted-foreground"}>
            {line}
          </div>
        ))}
      </div>

      <form onSubmit={handleCommand} className="flex items-center space-x-2">
        <span className="text-primary">$</span>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          className="flex-1 bg-transparent border-none outline-none text-primary"
          placeholder="Type your commands here..."
        />
        <Button type="submit" size="sm" variant="outline">
          Execute
        </Button>
      </form>
    </div>
  );
};

export default Terminal;
