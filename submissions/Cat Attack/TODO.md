~~DUCKYSCRIPT~~ DONE!
~~- Open cmd in the background~~
~~- Curl python to temp appdata directory ~~
~~- Install python quietly via cmdline~~
  ~~- Args:~~
    ~~- /quiet~~
    ~~- TargetDir=%LocalAppData%\python1~~
    ~~- AssociateFiles=0~~
    ~~- CompileAll=1~~
    ~~- Include_doc=0~~
    ~~- Include_launcher=0~~
    ~~- Include_tcltk=0~~
    ~~- Include_test=0~~
~~- Curl the main payload.py as an innocuous "py-manager.py" into python1 folder~~
~~- Curl the autostart.bat as "explorer.bat" into autostart folder~~
~~- Exit~~

PYTHON
- ~~Persistence: Copies itself into a few appdata directories~~ CANCELLED
- Behaviour
  ~~- Utilise input apis from windows to troll the user~~ DONE
    ~~- Block input~~ WORKS
    ~~- Change keyboard layout~~ No work :c
    ~~- Send a few keystrokes~~ WORKS
    ~~- Set double click threshold to crazy high so everything become doubleclick~~ WORKS 
    ~~- Swap mouse buttons~~ WORKS
    ~~- etc.etc.~~ Sense change, cursor trail 
  ~~- Create annoying 'adware' (actually just cat image) popups~~ DONE & WORKING!
  ~~- Redirects / forced rickrolls~~ DONE & WORKING!
  
~~BATCH SCRIPT~~ CANCELED - Implemented persistence via task scheduler instead
~~- Simply run the first instance of the python script it can find~~
~~- Python script should handle replacing deleted copies already.~~
