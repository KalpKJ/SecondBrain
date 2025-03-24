@echo off
echo Starting Second Brain System...
echo.

echo Step 1: Activating virtual environment...
cd /d %~dp0
call venv\Scripts\activate
echo Virtual environment activated.
echo.

echo Step 2: Starting Ollama...
start cmd /k "title Ollama Server && ollama serve"
echo Waiting for Ollama to initialize...
timeout /t 5 /nobreak > nul
echo Ollama started.
echo.

echo Step 3: Starting Flask API server...
start cmd /k "title Flask API && cd /d %~dp0 && call venv\Scripts\activate && python backend\api.py"
echo Waiting for API server to initialize...
timeout /t 3 /nobreak > nul
echo Flask API started.
echo.

echo Step 4: Starting Vue.js frontend...
start cmd /k "title Vue Frontend && cd /d %~dp0\frontend\second-brain-ui && npm run dev"
echo Waiting for frontend to initialize...
timeout /t 5 /nobreak > nul
echo Vue.js frontend started.
echo.

echo All Second Brain components are now running!
echo.
echo - Frontend: http://localhost:5173
echo - API: http://localhost:5000
echo - Ollama: http://localhost:11434
echo.
echo Your browser will open automatically in 3 seconds...
timeout /t 3 /nobreak > nul

start http://localhost:5173

echo.
echo Press any key to shut down all Second Brain components...
pause > nul

echo.
echo Shutting down components...
taskkill /f /fi "WINDOWTITLE eq Ollama Server" > nul 2>&1
taskkill /f /fi "WINDOWTITLE eq Flask API" > nul 2>&1
taskkill /f /fi "WINDOWTITLE eq Vue Frontend" > nul 2>&1
echo System stopped.
echo.

echo Thank you for using Second Brain!
timeout /t 3 /nobreak > nul
