@echo off
echo ========================================
echo Installing Missing Dependencies
echo ========================================
echo.

cd /d "%~dp0backend"

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Installing langgraph-checkpoint-sqlite...
pip install langgraph-checkpoint-sqlite==2.0.11

echo.
echo Installing all requirements...
pip install -r requirements.txt

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo You can now run start_backend.bat
pause
