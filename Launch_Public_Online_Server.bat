@echo off
title ISBMS - Launch Instant Online Server Tunnel
echo ==================================================
echo   ISBMS - Business Management System Online Server
echo ==================================================
echo Starting local application server...
start /b python main_desktop.py

echo.
echo Launching public internet tunnel via localtunnel...
echo Your public live URL will be generated below:
echo ==================================================
npx localtunnel --port 8000
pause
