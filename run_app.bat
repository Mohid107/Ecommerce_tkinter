@echo off
echo Starting ShopEasy App...
".venv\Scripts\python.exe" run.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Application crashed with error code %ERRORLEVEL%.
    pause
)
