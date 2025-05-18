# Wealth Map Platform Ignition Key

This document explains how to use the `start_all.bat` Windows batch file, which serves as an "ignition key" to start all components of the Wealth Map Platform (backend, frontend, and database) with a single command.

## Overview

The `start_all.bat` script provides a simple way to start all the necessary services for the Wealth Map Platform. It offers two modes of operation:

1. **Docker Mode (Recommended)**: Starts all services using Docker Compose
2. **Local Development Mode**: Starts services directly on your local machine

## Prerequisites

### For Docker Mode:
- Docker Desktop installed and running
- Docker Compose installed

### For Local Development Mode:
- PostgreSQL installed and running
- Python 3.8+ installed
- Node.js and npm installed

## How to Use

1. Open a Command Prompt window
2. Navigate to the project root directory
3. Run the ignition key:
   ```
   start_all.bat
   ```
4. Follow the on-screen prompts

## What the Ignition Key Does

When you run `start_all.bat`, the script will:

1. Check if Docker and Docker Compose are installed
2. Verify that environment files exist (and offer to create them if they don't)
3. Ask you to choose between Docker mode and Local Development mode
4. Start all services based on your selection
5. Display URLs to access the application components

### Docker Mode

In Docker mode, the script will:
- Start the PostgreSQL database container
- Start the backend FastAPI server container
- Start the frontend Vue.js container
- Start PgAdmin for database management

### Local Development Mode

In Local Development mode, the script will:
- Check if PostgreSQL is installed and configured
- Create a Python virtual environment if needed
- Install frontend dependencies if needed
- Start the backend server using uvicorn
- Start the frontend server using npm

## Accessing the Application

After starting the services, you can access:

- **Frontend**: 
  - Docker mode: http://localhost:8080
  - Local mode: http://localhost:5173 or http://localhost:5174
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Database Admin** (Docker mode only): http://localhost:5050
  - Email: admin@wealthmap.com
  - Password: admin

## Stopping the Services

- **Docker Mode**: Press any key in the command window or run `docker-compose down`
- **Local Mode**: Close the command windows or use Task Manager to end the processes

## Troubleshooting

If you encounter issues:

1. Make sure Docker Desktop is running (for Docker mode)
2. Check that PostgreSQL is running and configured correctly (for Local mode)
3. Verify that the required ports (8000, 8080, 5432, 5050) are not in use by other applications
4. Check the log files in the `backend/logs` directory

## Additional Information

For more detailed information about the Wealth Map Platform, refer to:
- `requirements.md` - Project requirements
- `project-structure.md` - Project structure overview
- `backend/README.md` - Backend documentation
- `frontend/README.md` - Frontend documentation (if available)