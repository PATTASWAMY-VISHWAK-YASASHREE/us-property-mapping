#!/bin/bash
cd backend
python -m pytest tests/test_zillow_api.py -v
python -m pytest tests/services/test_email_service.py -v