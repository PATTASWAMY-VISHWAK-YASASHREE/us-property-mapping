@echo off
echo Installing Python dependencies for testing...
cd backend
pip install -r requirements.txt
cd ..
echo Dependencies installed successfully.