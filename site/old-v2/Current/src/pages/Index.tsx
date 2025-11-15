import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { TerminalIcon, Zap, Send, ArrowRight, Code, Cpu, Usb } from "lucide-react";
import Navigation from "@/components/Navigation";
import Terminal from "@/components/Terminal";
import MatrixRain from "@/components/MatrixRain";
import EasterEggs from "@/components/EasterEggs";

const Index = () => {
  const duckMemes = [
    "🦆 Quack the code, hack the duck! 🦆",
    "🦆 Rubber ducky debugging, but make it physical! 🦆",
    "🦆 When your USB drive becomes sentient 🦆",
    "🦆 Ducky script go brrr 🦆",
    "🦆 From pond to pwn 🦆",
    "🦆 Quack attack incoming! 🦆",
    "🦆 Duck, duck, hack! 🦆",
    "🦆 Making waves in cybersecurity 🦆",
    "🦆 404: Duck not found... just kidding! 🦆",
    "🦆 sudo make me a sandwich... with duck sauce 🦆",
    "🦆 Git commit -m 'Added more quack' 🦆",
    "🦆 console.log('Hello Duck!') 🦆"
  ];

  const [currentMemeIndex, setCurrentMemeIndex] = useState(0);
  const [displayText, setDisplayText] = useState("");
  const [isTyping, setIsTyping] = useState(true);
  const [konamiCode, setKonamiCode] = useState([]);
  const [showSecret, setShowSecret] = useState(false);

  // Konami code sequence
  const konamiSequence = ['ArrowUp', 'ArrowUp', 'ArrowDown', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'ArrowLeft', 'ArrowRight', 'KeyB', 'KeyA'];

  useEffect(() => {
    const handleKeyDown = (e) => {
      const newSequence = [...konamiCode, e.code].slice(-10);
      setKonamiCode(newSequence);
      
      if (JSON.stringify(newSequence) === JSON.stringify(konamiSequence)) {
        setShowSecret(true);
        setTimeout(() => setShowSecret(false), 5000);
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [konamiCode]);

  useEffect(() => {
    const currentMeme = duckMemes[currentMemeIndex];
    let index = 0;
    
    const typeText = () => {
      if (index < currentMeme.length) {
        setDisplayText(currentMeme.slice(0, index + 1));
        index++;
        setTimeout(typeText, 100);
      } else {
        setIsTyping(false);
        setTimeout(() => {
          setDisplayText("");
          setCurrentMemeIndex((prev) => (prev + 1) % duckMemes.length);
          setIsTyping(true);
          index = 0;
        }, 2000);
      }
    };

    if (isTyping) {
      typeText();
    }
  }, [currentMemeIndex, isTyping]);

  return (
    <>
      <div className="min-h-screen bg-background relative overflow-hidden">
        <MatrixRain />
        <EasterEggs />
        <Navigation />
        
        {/* Konami Code Secret */}
        {showSecret && (
          <div className="fixed top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 z-50 bg-primary text-primary-foreground p-8 rounded-lg text-center animate-fade-in">
            <h2 className="text-2xl font-bold mb-4">🦆 SECRET DUCK MODE ACTIVATED! 🦆</h2>
            <p>You found the Konami code! Welcome to the Duck Dynasty!</p>
          </div>
        )}
        
        {/* Hero Section */}
        <section className="relative z-10 pt-24 pb-16">
          <div className="container mx-auto px-4">
            <div className="text-center max-w-4xl mx-auto">
              <h1 className="text-5xl md:text-7xl font-bold mb-6 text-gradient neon-glow glitch">
                HackDucky
              </h1>
              <div className="text-xl md:text-2xl mb-4 text-secondary h-8 relative">
                <span className="inline-block">
                  {displayText}
                  {isTyping && <span className="animate-pulse ml-1">|</span>}
                </span>
              </div>
              <p className="text-lg mb-8 text-muted-foreground max-w-2xl mx-auto">
                HackDucky is a YSWS where you make a ducky script + a 3D case design for the rubber ducky 
                and we ship you back a physical HackDucky board with your custom case!
              </p>
              
              <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
                <Button asChild size="lg" className="text-lg px-8 animate-glow-pulse">
                  <Link to="/submit">
                    <Send className="w-5 h-5 mr-2" />
                    Start Shipping
                  </Link>
                </Button>
                <Button asChild variant="outline" size="lg" className="text-lg px-8">
                  <Link to="/tutorial">
                    <Zap className="w-5 h-5 mr-2" />
                    Learn How
                  </Link>
                </Button>
              </div>
            </div>
          </div>
        </section>

        {/* How It Works */}
        <section className="relative z-10 py-16">
          <div className="container mx-auto px-4">
            <h2 className="text-3xl md:text-4xl font-bold text-center mb-12 text-gradient">
              How It Works
            </h2>
            
            <div className="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
              <Card className="terminal-glow hover:scale-105 transition-transform duration-300 group cursor-pointer" 
                    onClick={() => alert("🦆 Quack! You found an easter egg! 🦆")}>
                <CardHeader>
                  <CardTitle className="flex items-center text-primary group-hover:animate-pulse">
                    <Code className="w-6 h-6 mr-2" />
                    You Ship
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <ul className="space-y-2 text-muted-foreground">
                    <li>• A ducky script (.txt file)</li>
                    <li>• 3D case design (.stl or .step file)</li>
                  </ul>
                </CardContent>
              </Card>

              <Card className="terminal-glow hover:scale-105 transition-transform duration-300">
                <CardHeader>
                  <CardTitle className="flex items-center text-secondary">
                    <Cpu className="w-6 h-6 mr-2" />
                    We Ship
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <ul className="space-y-2 text-muted-foreground">
                    <li>• HackDucky board</li>
                    <li>• Custom 3D printed case</li>
                    <li>• Pre-loaded with your script</li>
                  </ul>
                </CardContent>
              </Card>
            </div>
          </div>
        </section>

        {/* Get Started Terminal */}
        <section className="relative z-10 py-16">
          <div className="container mx-auto px-4">
            <h2 className="text-3xl md:text-4xl font-bold text-center mb-12 text-gradient">
              Get Started
            </h2>
            <div className="max-w-4xl mx-auto">
              <Terminal />
            </div>
          </div>
        </section>

        {/* Features */}
        <section className="relative z-10 py-16">
          <div className="container mx-auto px-4">
            <h2 className="text-3xl md:text-4xl font-bold text-center mb-12 text-gradient">
              What You Get
            </h2>
            
            <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
              <Card className="text-center terminal-glow hover:scale-105 transition-all duration-300">
                <CardHeader>
                  <Usb className="w-12 h-12 mx-auto mb-4 text-primary" />
                  <CardTitle>HackDucky Board</CardTitle>
                  <CardDescription>
                    Identical to rubber ducky functionality
                  </CardDescription>
                </CardHeader>
              </Card>

              <Card className="text-center terminal-glow hover:scale-105 transition-all duration-300">
                <CardHeader>
                  <TerminalIcon className="w-12 h-12 mx-auto mb-4 text-secondary" />
                  <CardTitle>Custom Case</CardTitle>
                  <CardDescription>
                    3D printed from your own design specifications
                  </CardDescription>
                </CardHeader>
              </Card>

              <Card className="text-center terminal-glow hover:scale-105 transition-all duration-300">
                <CardHeader>
                  <Code className="w-12 h-12 mx-auto mb-4 text-accent" />
                  <CardTitle>Pre-loaded Script</CardTitle>
                  <CardDescription>
                    Your ducky script ready to execute
                  </CardDescription>
                </CardHeader>
              </Card>
            </div>
          </div>
        </section>

        {/* CTA */}
        <section className="relative z-10 py-16">
          <div className="container mx-auto px-4 text-center">
            <h2 className="text-3xl md:text-4xl font-bold mb-6 text-gradient">
              Ready to Join HackDucky?
            </h2>
            <p className="text-lg mb-8 text-muted-foreground max-w-2xl mx-auto">
              Join HackDucky and get your hands on cutting-edge hacking hardware!
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
              <Button asChild size="lg" className="text-lg px-8 animate-glow-pulse">
                <Link to="/submit">
                  Ship Your Code Now
                  <ArrowRight className="w-5 h-5 ml-2" />
                </Link>
              </Button>
              <Button asChild variant="secondary" className="text-lg px-8">
                <a href="https://hackclub.slack.com/archives/C08B8HZBC85" target="_blank" rel="noopener noreferrer">
                  Join HackClub Slack
                </a>
              </Button>
            </div>
          </div>
        </section>
      </div>
      <footer className="w-full py-4 text-center text-xs text-muted-foreground bg-background/80 border-t border-border mt-8">
        Website built by @Aarav J for Hack Club.
      </footer>
    </>
  );
};

export default Index;
