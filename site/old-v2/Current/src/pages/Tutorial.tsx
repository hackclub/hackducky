import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Code, Download, Upload, Zap, ArrowRight, Wrench, Cpu, Terminal as TerminalIcon, Github } from "lucide-react";
import { Link } from "react-router-dom";
import Navigation from "@/components/Navigation";
import MatrixRain from "@/components/MatrixRain";

const Tutorial = () => {
  const duckyCommands = [
    { command: "STRING", description: "Types the specified text exactly as written", example: "STRING Hello World!" },
    { command: "ENTER", description: "Presses the Enter/Return key", example: "ENTER" },
    { command: "DELAY", description: "Waits for specified milliseconds before next command", example: "DELAY 1000" },
    { command: "CONTROL", description: "Holds Ctrl key while pressing next key", example: "CONTROL a" },
    { command: "ALT", description: "Holds Alt key while pressing next key", example: "ALT TAB" },
    { command: "GUI", description: "Windows/Super/Cmd key for opening start menu", example: "GUI r" },
    { command: "SHIFT", description: "Holds Shift key while pressing next key", example: "SHIFT TAB" },
    { command: "TAB", description: "Presses the Tab key for navigation", example: "TAB" },
    { command: "ESCAPE", description: "Presses the Escape key", example: "ESCAPE" },
    { command: "SPACE", description: "Presses the Space bar", example: "SPACE" },
    { command: "BACKSPACE", description: "Presses the Backspace key", example: "BACKSPACE" },
    { command: "DELETE", description: "Presses the Delete key", example: "DELETE" },
  ];

  const advancedCommands = [
    { command: "F1-F12", description: "Function keys for shortcuts", example: "F4" },
    { command: "ARROW_UP/DOWN/LEFT/RIGHT", description: "Arrow keys for navigation", example: "ARROW_DOWN" },
    { command: "HOME/END", description: "Move cursor to start/end of line", example: "HOME" },
    { command: "PAGEUP/PAGEDOWN", description: "Page navigation keys", example: "PAGEUP" },
    { command: "PRINTSCREEN", description: "Takes a screenshot", example: "PRINTSCREEN" },
    { command: "CAPSLOCK", description: "Toggles caps lock", example: "CAPSLOCK" },
  ];

  return (
    <>
      <div className="min-h-screen bg-background relative overflow-hidden">
        <MatrixRain />
        <Navigation />
        
        <div className="relative z-10 pt-24 pb-16">
          <div className="container mx-auto px-4">
            <div className="max-w-5xl mx-auto">
              <div className="text-center mb-12">
                <h1 className="text-4xl md:text-5xl font-bold mb-4 text-gradient neon-glow">
                  HackDucky Complete Guide
                </h1>
                <p className="text-lg text-muted-foreground">
                  Master HackScript (enhanced ducky script) and 3D case design for your HackDucky board
                </p>
              </div>

              {/* Welcome & Introduction */}
              <Card className="mb-8 terminal-glow">
                <CardHeader>
                  <CardTitle className="flex items-center text-primary">
                    <Zap className="w-6 h-6 mr-2" />
                    Welcome to HackDucky Scripting!
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-muted-foreground mb-4">
                    Ever wanted to plug in a USB device and automate a computer? HackDucky lets you do just that using a simple scripting language inspired by Ducky Script. Read on to learn the basics and start building your own scripts!
                  </p>
                </CardContent>
              </Card>

              {/* Supported Commands */}
              <Card className="mb-8 terminal-glow">
                <CardHeader>
                  <CardTitle className="flex items-center text-secondary">
                    <Code className="w-6 h-6 mr-2" />
                    Supported Commands
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <ul className="list-disc pl-6 text-muted-foreground space-y-1">
                    <li><strong>REM</strong>: Comments for humans, ignored by the duck.</li>
                    <li><strong>DELAY</strong>: Pauses between actions (milliseconds).</li>
                    <li><strong>STRING</strong>: Types out text like a human.</li>
                    <li><strong>GUI, CONTROL, ALT, SHIFT</strong>: Modifier keys for shortcuts.</li>
                    <li><strong>ENTER</strong>: Simulates pressing Enter.</li>
                    <li><strong>TAB, ESCAPE, SPACE, BACKSPACE, DELETE</strong>: Special keys.</li>
                    <li><strong>F1-F12, Arrow Keys, HOME/END, PAGEUP/PAGEDOWN, CAPSLOCK</strong>: Navigation and function keys.</li>
                    {/* If DEFAULT_DELAY is supported, add: */}
                    <li><strong>DEFAULT_DELAY</strong>: (Optional) Sets a default delay between commands.</li>
                  </ul>
                </CardContent>
              </Card>

              {/* Example: Automate Notepad */}
              <Card className="mb-8 terminal-glow">
                <CardHeader>
                  <CardTitle className="flex items-center text-primary">
                    <Download className="w-6 h-6 mr-2" />
                    Example: Open Notepad, Type, Save, Close
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="bg-muted p-4 rounded-md mb-4">
                    <code className="text-sm block">
                      REM Basic example script<br />
                      DEFAULT_DELAY 200<br /><br />
                      REM Open Run dialog<br />
                      GUI r<br />
                      DELAY 500<br /><br />
                      REM Launch Notepad<br />
                      STRING notepad<br />
                      ENTER<br />
                      DELAY 1000<br /><br />
                      REM Type some text<br />
                      STRING Hello from HackDucky!<br />
                      ENTER<br /><br />
                      REM Save the file<br />
                      CTRL s<br />
                      STRING test.txt<br />
                      ENTER<br />
                      ALT F4
                    </code>
                  </div>
                  <p className="text-muted-foreground mb-2"><strong>What's happening here?</strong></p>
                  <ul className="list-disc pl-6 text-muted-foreground space-y-1 mb-2">
                    <li><code>GUI r</code> opens the Run dialog.</li>
                    <li><code>STRING notepad</code> types "notepad" and hits Enter.</li>
                    <li><code>STRING Hello from HackDucky!</code> types a message.</li>
                    <li><code>CTRL s</code> saves the file as "test.txt".</li>
                    <li><code>ALT F4</code> closes Notepad.</li>
                  </ul>
                  <p className="text-xs text-blue-400">If <code>DEFAULT_DELAY</code> is not supported by your firmware, simply remove that line and use <code>DELAY</code> as needed between commands.</p>
                </CardContent>
              </Card>

              {/* More Example Ideas */}
              <Card className="mb-8 terminal-glow">
                <CardHeader>
                  <CardTitle className="flex items-center text-secondary">
                    <TerminalIcon className="w-6 h-6 mr-2" />
                    More Ideas to Try
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <ul className="list-disc pl-6 text-muted-foreground space-y-1">
                    <li>Open a website and type a message</li>
                    <li>Prank script that rickrolls someone as soon as you plug in the USB</li>
                    <li>Automate login (using only supported commands)</li>
                    <li>Try running Doom in the terminal!</li>
                  </ul>
                </CardContent>
              </Card>

              {/* Pro Tips */}
              <Card className="mb-8 terminal-glow">
                <CardHeader>
                  <CardTitle className="flex items-center text-accent">
                    <Wrench className="w-6 h-6 mr-2" />
                    Pro Tips
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <ul className="list-disc pl-6 text-muted-foreground space-y-1">
                    <li>Start simple, then add more features.</li>
                    <li>Use <code>DELAY</code> wisely—too fast and your computer might miss keystrokes.</li>
                    <li>Test your script before using it on someone else's computer.</li>
                    <li>Have fun and share your creations in the #hackducky channel on Hack Club Slack!</li>
                  </ul>
                  <p className="text-xs text-blue-400 mt-2">Advanced features like variables, loops, and functions are coming soon!</p>
                </CardContent>
              </Card>

              {/* CAD Tutorial */}
              <Card className="mb-8 terminal-glow">
                <CardHeader>
                  <CardTitle className="flex items-center text-secondary">
                    <Wrench className="w-6 h-6 mr-2" />
                    3D Case Design Tutorial
                  </CardTitle>
                  <CardDescription>Learn to design custom cases for your HackDucky</CardDescription>
                </CardHeader>
                <CardContent className="space-y-6">
                  <div className="grid md:grid-cols-2 gap-6">
                    <div>
                      <h4 className="font-semibold text-primary mb-3">📐 Design Requirements</h4>
                      Coming Soon!
                    </div>
                    <div>
                      <h4 className="font-semibold text-primary mb-3">🛠️ Recommended CAD Software</h4>
                      <ul className="text-sm text-muted-foreground space-y-2">
                        <li>• <strong>Fusion 360</strong> (Free for students)</li>
                        <li>• <strong>Tinkercad</strong> (Browser-based, beginner)</li>
                        <li>• <strong>FreeCAD</strong> (Open source)</li>
                        <li>• <strong>Onshape</strong> (Cloud-based)</li>
                        <li>• <strong>SolidWorks</strong> (Professional)</li>
                        <li>• <strong>Blender</strong> (Advanced modeling)</li>
                      </ul>
                    </div>
                  </div>

                  <div>
                    <h4 className="font-semibold text-secondary mb-3">🎯 Step-by-Step Design Process</h4>
                    Coming Soon!
                  </div>

                  <div>
                    <h4 className="font-semibold text-accent mb-3">💡 Design Tips & Tricks</h4>
                    <div className="grid md:grid-cols-2 gap-4">
                      <div className="bg-green-500/10 border border-green-500/30 rounded-md p-3">
                        <h5 className="font-semibold text-green-400 mb-2">✅ Do This</h5>
                        <ul className="text-sm text-green-200 space-y-1">
                          <li>• Add chamfers to sharp edges</li>
                          <li>• Include snap-fit mechanisms</li>
                          <li>• Test fit with cardboard first</li>
                          <li>• Add grip texture or patterns</li>
                          <li>• Consider lanyard holes</li>
                        </ul>
                      </div>
                      <div className="bg-red-500/10 border border-red-500/30 rounded-md p-3">
                        <h5 className="font-semibold text-red-400 mb-2">❌ Avoid This</h5>
                        <ul className="text-sm text-red-200 space-y-1">
                          <li>• Walls thinner than 1.2mm</li>
                          <li>• Sharp internal corners</li>
                          <li>• Overhangs without support</li>
                          <li>• Too tight tolerances</li>
                          <li>• Forgetting USB clearance</li>
                        </ul>
                      </div>
                    </div>
                  </div>

                  <div className="bg-blue-500/10 border border-blue-500/30 rounded-md p-4">
                    <h5 className="font-semibold text-blue-400 mb-2">🎨 Creative Ideas</h5>
                    <ul className="text-sm text-blue-200 space-y-1">
                      <li>• Duck-shaped case with beak as USB port</li>
                      <li>• Stealth design that looks like a flash drive</li>
                      <li>• Transparent case to show internal components</li>
                      <li>• Modular case with swappable decorative panels</li>
                      <li>• Keychain-friendly compact design</li>
                      <li>• LED diffuser windows for status lights</li>
                    </ul>
                  </div>
                </CardContent>
              </Card>

              {/* File Requirements */}
              <Card className="mb-8 terminal-glow">
                <CardHeader>
                  <CardTitle className="flex items-center text-accent">
                    <Upload className="w-6 h-6 mr-2" />
                    File Submission Guidelines
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="grid md:grid-cols-2 gap-6">
                    <div>
                      <h4 className="font-semibold text-secondary mb-3">📄 HackScript Requirements</h4>
                      <ul className="text-sm text-muted-foreground space-y-1">
                        <li>• File format: .txt</li>
                        <li>• Use proper Ducky Script syntax</li>
                        <li>• You Can include comments with REM</li>
                        <li>• Test your script before submitting</li>
                      </ul>
                    </div>
                    <div>
                      <h4 className="font-semibold text-secondary mb-3">🎯 CAD File Requirements</h4>
                      <ul className="text-sm text-muted-foreground space-y-1">
                        <li>• File formats: STL or STEP preferred</li>
                        <li>• Maximum file size: 10MB</li>
                        <li>• Proper orientation for printing (eg : no wasteful supports on overhangs)</li>
                        <li>• Should fit the hackducky board 😭</li>
                      </ul>
                    </div>
                  </div>
                  
                  <div className="bg-blue-500/10 border border-blue-500/30 rounded-md p-4">
                    <p className="text-sm text-blue-200">
                      <strong>HackScript Advantage:</strong> Use conditional logic and functions to create 
                      adaptive scripts that work across different environments and user scenarios! Functions and if statements will be coming soon!
                    </p>
                  </div>
                </CardContent>
              </Card>

              {/* Next Steps */}
              <div className="text-center">
                <h2 className="text-3xl font-bold mb-4 text-gradient">Ready to Create Your HackDucky?</h2>
                <p className="text-muted-foreground mb-6 max-w-2xl mx-auto">
                  Now that you have mastered both HackScript and 3D case design, 
                  it's time to bring your creation to life! Submit your masterpiece and get ready to receive 
                  your custom HackDucky board.
                </p>
                <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
                  <Button asChild size="lg" className="animate-glow-pulse">
                    <Link to="/submit">
                      Submit Your HackDucky Creation
                      <ArrowRight className="w-5 h-5 ml-2" />
                    </Link>
                  </Button>
                  <Button asChild variant="outline" size="lg">
                    <a href="https://github.com/hackclub/hackducky" target="_blank" rel="noopener noreferrer">
                      <Github className="w-5 h-5 mr-2" />
                      View GitHub Repo
                    </a>
                  </Button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      {/* Footer */}
      <footer className="w-full py-4 text-center text-xs text-muted-foreground bg-background/80 border-t border-border mt-8">
        Website built by @Aarav J. DM @Aarav J on Slack for any questions.
      </footer>
    </>
  );
};

export default Tutorial;
