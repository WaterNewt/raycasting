#!/bin/bash

# Detecting the platform
OS=$(uname -s)

# Check for UPX
UPX_DIR=""
if [ "$OS" == "Linux" ] || [ "$OS" == "Darwin" ]; then
    UPX_DIR=$(command -v upx)
elif [ "$OS" == "MINGW64_NT-10.0" ]; then
    UPX_DIR=$(where.exe upx)
fi

if [ -z "$UPX_DIR" ]; then
    echo "UPX is not installed or not found in the PATH."
    echo "Please install UPX for better compression or remove '--upx-dir' option."
    exit 1
fi

# Set icon file based on platform
ICON_FILE=""
if [ "$OS" == "MINGW64_NT-10.0" ]; then
    ICON_FILE="icon.ico"
else
    ICON_FILE="icon.png"
fi

# Set script file
SCRIPT_FILE="main.py"

# Run PyInstaller
pyinstaller --windowed --icon "$ICON_FILE" --name RayCast --upx-dir "$UPX_DIR" --clean --add-data "$ICON_FILE:." --noconfirm "$SCRIPT_FILE"
exit_code=$?

if [ $exit_code -ne 0 ]; then
    echo "PyInstaller failed to compile the script. Please make sure it is installed."
    exit 1
fi

echo "Compilation successful."
exit 0
