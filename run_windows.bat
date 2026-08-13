@echo off
setlocal
cd /d "%~dp0"
if not exist ".streamlit" mkdir ".streamlit"
(
echo [browser]
echo gatherUsageStats = false
) > ".streamlit\config.toml"
echo.
echo ============================================================
echo   STUDENT PERFORMANCE INTELLIGENCE - STARTING DASHBOARD
echo ============================================================
echo.
python -m pip install -r "%~dp0requirements.txt"
python -m streamlit run "%~dp0app\app.py"
pause
