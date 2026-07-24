@echo off  
echo Starting Wenli Carbon Calculator...
cd /d "%~dp0"
python -m streamlit run ui/app.py --server.port 8502
pause  
