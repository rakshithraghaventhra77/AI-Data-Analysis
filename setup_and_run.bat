@echo off
REM AI Powered Data Analysis Generator - Automated Setup & Run Script
setlocal enabledelayedexpansion

echo.
echo =====================================
echo AI DATA ANALYZER - SETUP & RUN
echo =====================================
echo.

REM Check if Python is installed
python --version > nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from python.org
    pause
    exit /b 1
)

echo [*] Python found: 
python --version

REM Create virtual environment if it doesn't exist
if not exist ".venv" (
    echo [*] Creating virtual environment...
    python -m venv .venv
    echo [+] Virtual environment created
) else (
    echo [+] Virtual environment already exists
)

REM Activate virtual environment
echo [*] Activating virtual environment...
call .venv\Scripts\activate.bat

REM Upgrade pip
echo [*] Upgrading pip...
python -m pip install --upgrade pip > nul 2>&1

REM Install requirements
echo [*] Installing dependencies...
cd project
pip install -r requirements.txt > nul 2>&1
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo [+] Dependencies installed successfully

REM Check if dataset exists
if not exist "olist_orders_dataset.csv" (
    echo.
    echo WARNING: olist_orders_dataset.csv not found in project folder
    echo Please ensure your dataset is in: !cd!
    echo.
)

REM Display startup info
echo.
echo =====================================
echo STARTING APPLICATION
echo =====================================
echo.
echo Dashboard URL: http://localhost:5000
echo Status Page: http://localhost:5000/system-info
echo.
echo Available Endpoints:
echo   /               - Dashboard UI
echo   /metrics        - Key metrics (JSON)
echo   /order-status   - Order status distribution
echo   /monthly-trend  - Monthly trends
echo   /insights       - AI insights
echo   /delivery-breakdown - Delivery stats
echo   /data-quality   - Data quality report
echo   /predict        - ML predictions
echo   /report         - Download PDF report
echo   /system-info    - System information
echo.
echo Press Ctrl+C to stop the server
echo =====================================
echo.

REM Start Flask app
python app.py

pause
