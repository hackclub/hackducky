
import { useState, useEffect } from "react";

const EasterEggs = () => {
  const [clickCount, setClickCount] = useState(0);
  const [showDuck, setShowDuck] = useState(false);
  const [duckPosition, setDuckPosition] = useState({ x: 0, y: 0 });

  // Flying duck easter egg on multiple clicks
  useEffect(() => {
    if (clickCount >= 10) {
      setShowDuck(true);
      const timer = setTimeout(() => {
        setShowDuck(false);
        setClickCount(0);
      }, 3000);
      return () => clearTimeout(timer);
    }
  }, [clickCount]);

  // Random duck movement
  useEffect(() => {
    if (showDuck) {
      const interval = setInterval(() => {
        setDuckPosition({
          x: Math.random() * (window.innerWidth - 50),
          y: Math.random() * (window.innerHeight - 50)
        });
      }, 500);
      return () => clearInterval(interval);
    }
  }, [showDuck]);

  const handleDocumentClick = () => {
    setClickCount(prev => prev + 1);
  };

  useEffect(() => {
    document.addEventListener('click', handleDocumentClick);
    return () => document.removeEventListener('click', handleDocumentClick);
  }, []);

  return (
    <>
      {/* Hidden duck that appears on rapid clicking */}
      {showDuck && (
        <div 
          className="fixed text-4xl animate-bounce z-50 pointer-events-none transition-all duration-500"
          style={{ 
            left: `${duckPosition.x}px`, 
            top: `${duckPosition.y}px`,
            transform: 'translate(-50%, -50%)'
          }}
        >
          🦆
        </div>
      )}

      {/* Secret message in corner */}
      <div 
        className="fixed bottom-4 right-4 text-xs text-muted-foreground opacity-30 hover:opacity-100 transition-opacity cursor-pointer z-40"
        onClick={() => alert("🦆 Psst... try the Konami code! (↑↑↓↓←→←→BA) 🦆")}
      >
        ?
      </div>

      {/* Hidden developer credit */}
      <div className="fixed bottom-0 left-0 text-xs text-transparent hover:text-muted-foreground transition-colors p-2 z-40">
        Made with 🦆 by HackClub
      </div>

      {/* Random floating elements */}
      <div className="fixed top-1/4 right-8 text-2xl animate-pulse opacity-20 hover:opacity-60 transition-opacity pointer-events-none">
        💻
      </div>
      <div className="fixed top-3/4 left-8 text-2xl animate-pulse opacity-20 hover:opacity-60 transition-opacity pointer-events-none">
        🔧
      </div>
      <div className="fixed top-1/2 right-1/4 text-2xl animate-pulse opacity-20 hover:opacity-60 transition-opacity pointer-events-none">
        ⚡
      </div>
    </>
  );
};

export default EasterEggs;
