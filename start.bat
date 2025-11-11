@echo off
echo ================================================
echo Starting Coffee Tester Feedback Collection App
echo ================================================
echo.

echo Starting Backend Server...
start "Coffee Backend" cmd /k "cd backend && venv\Scripts\activate && python main.py"

timeout /t 3 /nobreak > nul

echo Starting Frontend Development Server...
start "Coffee Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo ================================================
echo Both servers are starting...
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:5173
echo API Docs: http://localhost:8000/docs
echo ================================================
echo.
echo Press any key to stop all servers...
pause > nul

taskkill /FI "WindowTitle eq Coffee Backend*" /T /F
taskkill /FI "WindowTitle eq Coffee Frontend*" /T /F
