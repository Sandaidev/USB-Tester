@ECHO OFF
pyinstaller --noconfirm --noupx --clean -d all --icon "icon.ico" "USBTester.py"
pause