#!/bin/bash
cd /workspace/backend
export PYTHONPATH=/workspace/backend
echo "Running test_imports.py with PYTHONPATH=$PYTHONPATH"
python test_imports.py