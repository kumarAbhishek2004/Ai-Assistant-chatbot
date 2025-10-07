@echo off
echo ========================================
echo Personal Assistant Chatbot - Setup
echo ========================================
echo.

echo [1/2] Setting up Backend...
cd backend

echo Creating virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing Python dependencies...
pip install -r requirements.txt

echo.
echo Backend setup complete!
echo.

cd ..

echo [2/2] Setting up Frontend...
cd frontend

echo Installing Node dependencies...
call npm install

echo.
echo Frontend setup complete!
echo.

cd ..

echo ========================================
echo Setup Complete! 
echo ========================================
echo.
echo To run the application:
echo   1. Run start_backend.bat in one terminal
echo   2. Run start_frontend.bat in another terminal
echo   3. Open http://localhost:3000 in your browser
echo.
pause
