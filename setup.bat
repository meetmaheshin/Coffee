@echo off
echo ================================================
echo Coffee Tester Feedback Collection App - Setup
echo ================================================
echo.

echo [1/4] Setting up Python Backend...
cd backend
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing Python dependencies...
pip install -r requirements.txt

echo.
echo [2/4] Setting up Node.js Frontend...
cd ..\frontend

echo Installing Node.js dependencies...
call npm install

echo.
echo [3/4] Creating environment files...
cd ..
if not exist backend\.env (
    copy backend\.env.example backend\.env
    echo Created backend\.env
)
if not exist frontend\.env (
    copy frontend\.env.example frontend\.env
    echo Created frontend\.env
)

echo.
echo [4/4] Setup Complete!
echo.
echo ================================================
echo To run the application:
echo ================================================
echo.
echo Terminal 1 - Backend:
echo   cd backend
echo   venv\Scripts\activate
echo   python main.py
echo.
echo Terminal 2 - Frontend:
echo   cd frontend
echo   npm run dev
echo.
echo Then open: http://localhost:5173
echo ================================================
echo.
pause
