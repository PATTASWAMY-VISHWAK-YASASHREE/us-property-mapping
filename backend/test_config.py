import os
import sys
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(backend_dir))

# Test the config module
try:
    from app.core.config import settings
    print("Successfully imported settings")
    print(f"BACKEND_CORS_ORIGINS: {settings.BACKEND_CORS_ORIGINS}")
    
    # Test with a string value
    os.environ["BACKEND_CORS_ORIGINS"] = "http://localhost:3000,http://localhost:8000"
    from app.core.config import Settings
    test_settings = Settings()
    print(f"Test with string: {test_settings.BACKEND_CORS_ORIGINS}")
    
    # Test with a list value
    os.environ["BACKEND_CORS_ORIGINS"] = '["http://localhost:3000", "http://localhost:8000"]'
    test_settings = Settings()
    print(f"Test with JSON string: {test_settings.BACKEND_CORS_ORIGINS}")
    
    print("All tests passed!")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()