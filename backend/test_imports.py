import sys
import os

# Print the current Python path
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
except ImportError as e:
    print(f"Import error: {e}")