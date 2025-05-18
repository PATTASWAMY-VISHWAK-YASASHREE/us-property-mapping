#!/bin/bash
cd /workspace/backend
python -c "
import sys
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path.cwd()
sys.path.insert(0, str(backend_dir))

# Try importing the UserActivity class
try:
    from app.models.user import UserActivity
    print('Successfully imported UserActivity')
    print(f'UserActivity fields: {[column.name for column in UserActivity.__table__.columns]}')
except ImportError as e:
    print(f'Import error: {e}')
except Exception as e:
    print(f'Error: {e}')
"