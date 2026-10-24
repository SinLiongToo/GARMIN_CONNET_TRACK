@echo off
cd /d "%~dp0"
set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8
title Garmin Connect Dashboard & GPS Auto Updater

echo ======================================================
echo   Garmin Connect Auto Updater (Health Data + GPX Tracks)
echo =======================================================
echo.

where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python not found. Please ensure Python is installed and added to PATH.
    pause
    exit /b 1
)

echo [1/2] Syncing health metrics and updating dashboard...
python main.py --sync --days 1000 --no-open

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Health sync encountered an issue. Please check the message above.
    pause
    exit /b 1
)

echo.
echo [2/2] Downloading latest GPS tracks (skipping treadmill)...
python download_gpx.py --mode all --limit 50

echo.
echo Complete! Opening dashboard in browser...
start "" "garmin_health_dashboard.html"
