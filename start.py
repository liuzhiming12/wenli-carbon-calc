import subprocess
import sys
import os

if __name__ == "__main__":
    print("========================================")
    print("   Starting Wenli Carbon Calculator...")
    print("========================================")
    
    # Change to script directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Start Streamlit
    python_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".venv", "Scripts", "python.exe")
    result = subprocess.run([python_path, "-m", "streamlit", "run", "ui/app.py", "--server.port", "8502"])
    sys.exit(result.returncode)
