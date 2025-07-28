import os
import time 
import sys

os.system("color 4F")
os.system("title SYSTEM ALERT")

print("Warning: a potential threat has been located on your computer")
time.sleep(1)
print("analyzing system files")
time.sleep(2)

for i in range (1, 6):
    print(f" - Scanning C:\\System32\\file{i}.dll ... OK")
    time.sleep(0.5)



os.system("color 0A")
