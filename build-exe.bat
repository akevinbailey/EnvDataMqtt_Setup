@echo off
setlocal enableextensions

REM ==========================================================
REM Build EnvDataMqtt_Setup.exe (one-file) with PyInstaller
REM ==========================================================

cd /d "%~dp0"

set "NAME=EnvDataMqtt_Setup"
set "SCRIPT=.\src\EnvDataMqtt_Setup.py"
set "ICON_1=.\resources\EnvDataMqtt_Setup.ico"
set "ICON_2=.\resources\EnvDataMqtt_Setup.png"

echo [CLEAN] Removing previous build artifacts...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist "%NAME%.spec" del /q "%NAME%.spec"

echo [BUILD] Packaging with PyInstaller...
py -m PyInstaller --clean --noconfirm ^
    --name "%NAME%" ^
    --onefile --noconsole ^
    --icon "%ICON_1%" ^
    --hidden-import PySide6.QtCore ^
    --hidden-import PySide6.QtGui ^
    --hidden-import PySide6.QtWidgets ^
    --hidden-import PySide6.QtBluetooth ^
    --add-data "%ICON_1%;./resources" ^
    --add-data "%ICON_2%;./resources" ^
     "%SCRIPT%"
if errorlevel 1 (
  echo [ERROR] PyInstaller failed. See messages above.
  exit /b 1
)

echo [DONE] Built: dist\%NAME%.exe
echo If the icon does not show immediately in Explorer, refresh or clear the icon cache.
pause