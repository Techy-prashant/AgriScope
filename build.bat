@echo off
echo Cleaning old build artifacts...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

echo Building AutoEverGreen...
python -m PyInstaller --name AutoEverGreen --onedir --windowed --clean --noconfirm --collect-all customtkinter main.py

echo Copying configuration and state...
xcopy /E /I /Y config dist\AutoEverGreen\config
copy /Y state.json dist\AutoEverGreen\

echo Build complete! Executable is located at dist\AutoEverGreen\AutoEverGreen.exe
