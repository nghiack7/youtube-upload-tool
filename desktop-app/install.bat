@echo off
REM YouTube Upload Tool - Desktop App Installer (Windows)

echo 🎬 YouTube Upload Tool - Desktop App Installer
echo ==============================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python 3.8+ first.
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python found
python --version

REM Create virtual environment
echo.
echo 📦 Creating virtual environment...
python -m venv venv

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
echo.
echo 📥 Installing dependencies...
python -m pip install --quiet --upgrade pip
python -m pip install --quiet PyQt6 google-api-python-client google-auth-oauthlib google-auth-httplib2 yt-dlp

echo ✅ Dependencies installed

REM Create launcher script
echo.
echo 🚀 Creating launcher script...

(
echo @echo off
echo cd /d "%%~dp0"
echo call venv\Scripts\activate.bat
echo python youtube_uploader.py
echo pause
) > youtube-uploader.bat

echo ✅ Launcher script created: youtube-uploader.bat

REM Create config directory
set CONFIG_DIR=%USERPROFILE%\.youtube_uploader
if not exist "%CONFIG_DIR%" mkdir "%CONFIG_DIR%"

echo.
echo ✅ Installation complete!
echo.
echo 📁 Configuration directory: %CONFIG_DIR%
echo.
echo 🚀 To launch the app:
echo    Double-click youtube-uploader.bat
echo.
echo 📖 Next steps:
echo    1. Create OAuth credentials at https://console.cloud.google.com/
echo    2. Save client_secrets.json to: %CONFIG_DIR%
echo    3. Open the app and click "Authenticate with YouTube"
echo.
echo 📖 Full guide: DESKTOP_APP.md
echo.
pause
