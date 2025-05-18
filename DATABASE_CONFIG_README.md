# Database Configuration Changes

## Overview

This document explains the changes made to fix the batch file and database configuration issues.

## Changes Made

1. **Updated PostgreSQL Password**:
   - Changed the database password from `postgres` to `vishwak` in all configuration files
   - Updated the `docker-compose.yml` file to use the new password
   - Updated all batch files to reference the new password

2. **Added Database Initialization Script**:
   - Created the `docker/postgres/init-db` directory
   - Added `01-init.sql` script to initialize the database with the correct configuration
   - The script creates a `db_info` table with a verification message

3. **Added Database Connection Test**:
   - Created a new test file `backend/tests/test_db_connection.py` to verify database connectivity
   - Updated `run_tests.bat` to include the database connection test
   - Added a new test option `db` to run only the database connection test

4. **Updated Environment Variables**:
   - Set the `DATABASE_URL` environment variable in `run_tests.bat` to use the correct password

## How to Test

1. **Test Database Connection**:
   ```
   run_tests.bat db
   ```

2. **Run All Tests**:
   ```
   run_tests.bat all
   ```

## Troubleshooting

If you encounter issues with the database connection:

1. Make sure PostgreSQL is running on port 5432
2. Verify that the database name is `wealth_map`
3. Verify that the password is set to `vishwak`
4. Check that the `init-db` directory is properly mounted in the Docker container

## Port Configuration

- Frontend: Port 8080
- Backend API: Port 8000
- PostgreSQL Database: Port 5432
- PgAdmin: Port 5050