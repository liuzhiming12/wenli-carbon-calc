@echo off
echo ========================================
echo   Starting Wenli Carbon Calculator...
echo ========================================
cd /d "%~dp0"

:: Activate virtual environment
call "D:\桌面\hongniao_study\.venv\Scripts\activate.bat"

:: Start Streamlit
"D:\桌面\hongniao_study\.venv\Scripts\python.exe" -m streamlit run ui/app.py --server.port 8502

pause
