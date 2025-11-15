
import { useEffect, useState } from "react";

const MatrixRain = () => {
  const [chars, setChars] = useState<Array<{ char: string; delay: number; column: number }>>([]);

  useEffect(() => {
    const characters = "ハックダッキー0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    const newChars = [];
    
    for (let i = 0; i < 20; i++) {
      newChars.push({
        char: characters[Math.floor(Math.random() * characters.length)],
        delay: Math.random() * 5,
        column: i * 5,
      });
    }
    
    setChars(newChars);
  }, []);

  return (
    <div className="fixed inset-0 overflow-hidden pointer-events-none opacity-10 z-0">
      {chars.map((item, index) => (
        <div
          key={index}
          className="absolute text-primary text-sm matrix-char"
          style={{
            left: `${item.column}%`,
            '--delay': `${item.delay}s`,
          } as React.CSSProperties}
        >
          {item.char}
        </div>
      ))}
    </div>
  );
};

export default MatrixRain;
