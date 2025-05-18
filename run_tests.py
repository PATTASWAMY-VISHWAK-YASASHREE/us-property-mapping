import sys
import os
import subprocess
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_dir))
os.environ["PYTHONPATH"] = str(backend_dir)

print(f"Current PYTHONPATH: {os.environ.get('PYTHONPATH', 'Not set')}")
print(f"Current sys.path: {sys.path}")

try:
    # Try importing the app module
    import app
    print("Successfully imported app module")
    
    # Try importing app.main
    from app import main
    print("Successfully imported app.main module")
    
    # Try importing the app object from app.main
    from app.main import app
    print("Successfully imported app object from app.main")
    
    # Run pytest
    print("Running pytest...")
    os.chdir(backend_dir)
    subprocess.run(["python", "-m", "pytest"])
except ImportError as e:
    print(f"Import error: {e}")