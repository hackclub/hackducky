#!/usr/bin/env python3
import time
import random
import threading
import sys

try:
    import winsound
    HAS_WINSOUND = True
except ImportError:
    HAS_WINSOUND = False

class SoundTroll:
    def __init__(self):
        self.running = False
        
    def beep(self, freq=800, duration=200):
        if HAS_WINSOUND:
            try:
                winsound.Beep(freq, duration)
            except:
                print("\a", end="", flush=True)
        else:
            print("\a", end="", flush=True)
            time.sleep(duration / 1000)
    
    def mosquito(self):
        freqs = [2000, 2200, 2400]
        for f in freqs:
            if not self.running: break
            self.beep(f, 100)
            time.sleep(0.05)
    
    def alarm(self):
        for _ in range(3):
            if not self.running: break
            self.beep(800, 200)
            time.sleep(0.1)
            self.beep(1000, 200)
            time.sleep(0.1)
    
    def chaos(self):
        while self.running:
            freq = random.randint(200, 3000)
            duration = random.randint(50, 500)
            self.beep(freq, duration)
            time.sleep(random.randint(10, 1000) / 1000)
    
    def start(self, mode="medium", duration=None):
        self.running = True
        print(f"[*] Starting {mode} audio...")
        
        def sound_loop():
            patterns = [self.mosquito, self.alarm]
            
            while self.running:
                if mode == "low":
                    random.choice(patterns)()
                    time.sleep(random.randint(5, 10))
                elif mode == "medium":
                    random.choice(patterns)()
                    time.sleep(random.randint(2, 5))
                elif mode == "high":
                    random.choice(patterns)()
                    time.sleep(random.randint(1, 3))
                elif mode == "chaos":
                    self.chaos()
                    break
        
        thread = threading.Thread(target=sound_loop)
        thread.daemon = True
        thread.start()
        
        if duration:
            time.sleep(duration)
            self.stop()
    
    def stop(self):
        self.running = False
        print("\n[*] Stopped")

def main():
    troll = SoundTroll()
    
    mode = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] in ["low", "medium", "high", "chaos"] else "medium"
    duration = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2].isdigit() else None
    
    try:
        troll.start(mode, duration)
        if not duration:
            input("Press Enter to stop...")
            troll.stop()
    except KeyboardInterrupt:
        troll.stop()

if __name__ == "__main__":
    main()