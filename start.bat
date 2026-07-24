@echo off  
echo ========================================
echo   Starting Wenli Carbon Calculator...
echo   文理碳计 启动中...
echo ========================================
cd /d "%~dp0"

:: Activate virtual environment
call ..\.venv\Scripts\activate.bat

:: Start Streamlit
python -m streamlit run ui/app.py --server.port 8502

pause  
