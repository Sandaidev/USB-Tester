@ECHO OFF
pyinstaller --noconfirm --onefile --noupx --clean --icon "icon.ico" "USBTester.py"
pause