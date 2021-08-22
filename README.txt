How to use the script :

- reset your astral points at your favorite npc
- input your stats in input_stats.txt
- launch astral_simulator.exe and wait windows to close
- open XX_astral_tree.svg if it does not open by itself

How to package :
- pip install pyinstaller
- pyinstaller --onefile astral_simulator.py

Convert a list of svg to a gif :
-  magick.exe -delay 60 -loop 0 *.svg myimage.gif