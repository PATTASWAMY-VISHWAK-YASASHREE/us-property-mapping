import sys
import os
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_dir))

try:
    from app.main import app
    print("Successfully imported app.main")
except ImportError as e:
    print(f"Import error: {e}")
    print(f"Current sys.path: {sys.path}")