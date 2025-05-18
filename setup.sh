#!/bin/bash

# Wealth Map Platform Setup Script
# This script installs all requirements and starts all servers for the Wealth Map Platform

# Text colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print section headers
print_section() {
    echo -e "\n${GREEN}==== $1 ====${NC}\n"
}

# Function to print errors
print_error() {
    echo -e "${RED}ERROR: $1${NC}"
}

# Function to print warnings
print_warning() {
    echo -e "${YELLOW}WARNING: $1${NC}"
}

# Check if Docker and Docker Compose are installed
check_docker() {
    print_section "Checking Docker Installation"
    
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        echo "Visit https://docs.docker.com/get-docker/ for installation instructions."
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        echo "Visit https://docs.docker.com/compose/install/ for installation instructions."
        exit 1
    fi
    
    echo -e "${GREEN}✓${NC} Docker and Docker Compose are installed."
}

# Check for required environment variables
check_env_vars() {
    print_section "Checking Environment Variables"
    
    # Create .env files if they don't exist
    if [ ! -f ./backend/.env ]; then
        echo "Creating backend/.env file with default values..."
        cat > ./backend/.env << EOL
# Database
DATABASE_URL=postgresql://postgres:postgres@db:5432/wealth_map

# Security
SECRET_KEY=dev_secret_key_for_local_development_only
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=7
MFA_ENABLED=true
MFA_ISSUER=WealthMapAPI
MFA_REQUIRED=false

# API Keys
RAPIDAPI_KEY=your_rapidapi_key_here
MAPBOX_API_KEY=your_mapbox_api_key_here

# Zillow API Settings
ZILLOW_API_HOST=zillow-com1.p.rapidapi.com
ZILLOW_CACHE_EXPIRY=3600
ZILLOW_MAX_RETRIES=3
ZILLOW_RETRY_DELAY=2
ZILLOW_IMAGE_STORAGE_PATH=/tmp/property_images

# Environment
ENVIRONMENT=development
MOCK_EXTERNAL_APIS=true

# Logging
LOG_LEVEL=DEBUG
SECURITY_LOG_FILE=/app/logs/security.log

# HTTPS settings
HTTPS_ONLY=false

# Frontend URL
FRONTEND_URL=http://localhost:8080

# Rate limiting
RATE_LIMIT_ENABLED=false
RATE_LIMIT_DEFAULT=100/minute
RATE_LIMIT_LOGIN=5/minute

# Email settings
SMTP_SERVER=
SMTP_PORT=587
SMTP_USERNAME=
SMTP_PASSWORD=
SMTP_SENDER=noreply@wealthmap.com
SMTP_TLS=true
EOL
        print_warning "Backend .env file created with default values. Please update with your actual API keys."
    else
        echo -e "${GREEN}✓${NC} Backend .env file exists."
    fi
    
    if [ ! -f ./frontend/.env ]; then
        echo "Creating frontend/.env file with default values..."
        cat > ./frontend/.env << EOL
VITE_API_URL=http://localhost:8000
VITE_MAPBOX_TOKEN=your_mapbox_token_here
EOL
        print_warning "Frontend .env file created with default values. Please update with your actual API keys."
    else
        echo -e "${GREEN}✓${NC} Frontend .env file exists."
    fi
    
    # Create logs directory for backend
    mkdir -p ./backend/logs
    touch ./backend/logs/security.log
    echo -e "${GREEN}✓${NC} Created logs directory and security log file."
}

# Install dependencies for local development (without Docker)
install_dependencies_local() {
    print_section "Installing Dependencies (Local Development)"
    
    # Install frontend dependencies
    echo "Installing frontend dependencies..."
    cd frontend
    if ! npm install; then
        print_error "Failed to install frontend dependencies."
        exit 1
    fi
    cd ..
    echo -e "${GREEN}✓${NC} Frontend dependencies installed."
    
    # Install backend dependencies
    echo "Installing backend dependencies..."
    cd backend
    
    # Check if Python virtual environment exists, create if not
    if [ ! -d "venv" ]; then
        echo "Creating Python virtual environment..."
        python3 -m venv venv
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Install dependencies
    if ! pip install -r requirements.txt; then
        print_error "Failed to install backend dependencies."
        exit 1
    fi
    
    cd ..
    echo -e "${GREEN}✓${NC} Backend dependencies installed."
}

# Start services for local development (without Docker)
start_services_local() {
    print_section "Starting Services (Local Development)"
    
    # Start PostgreSQL (assuming it's installed locally)
    echo "Please ensure PostgreSQL is running locally with the following configuration:"
    echo "  - Database: wealth_map"
    echo "  - Username: postgres"
    echo "  - Password: postgres"
    echo "  - Port: 5432"
    
    # Start backend in background
    echo "Starting backend server..."
    cd backend
    source venv/bin/activate
    nohup uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload > ./logs/backend.log 2>&1 &
    BACKEND_PID=$!
    cd ..
    echo -e "${GREEN}✓${NC} Backend server started (PID: $BACKEND_PID)."
    
    # Start frontend in background
    echo "Starting frontend server..."
    cd frontend
    nohup npm run dev > ../backend/logs/frontend.log 2>&1 &
    FRONTEND_PID=$!
    cd ..
    echo -e "${GREEN}✓${NC} Frontend server started (PID: $FRONTEND_PID)."
    
    echo -e "\n${GREEN}Services are now running:${NC}"
    echo "  - Backend: http://localhost:8000"
    echo "  - Frontend: http://localhost:5173"
    echo "  - API Documentation: http://localhost:8000/docs"
    
    echo -e "\n${YELLOW}To stop the services, run: kill $BACKEND_PID $FRONTEND_PID${NC}"
}

# Start services using Docker Compose
start_services_docker() {
    print_section "Starting Services (Docker)"
    
    echo "Building and starting Docker containers..."
    if ! docker-compose up -d; then
        print_error "Failed to start Docker containers."
        exit 1
    fi
    
    echo -e "\n${GREEN}Services are now running:${NC}"
    echo "  - Backend: http://localhost:8000"
    echo "  - Frontend: http://localhost:8080"
    echo "  - API Documentation: http://localhost:8000/docs"
    echo "  - PgAdmin: http://localhost:5050"
    echo "    - Email: admin@wealthmap.com"
    echo "    - Password: admin"
    
    echo -e "\n${YELLOW}To stop the services, run: docker-compose down${NC}"
}

# Main execution
main() {
    print_section "Wealth Map Platform Setup"
    
    # Check Docker installation
    check_docker
    
    # Check and create environment files
    check_env_vars
    
    # Ask user whether to use Docker or local development
    echo -e "\nDo you want to use Docker for development? (Recommended)"
    read -p "Enter [Y/n]: " use_docker
    use_docker=${use_docker:-Y}
    
    if [[ $use_docker =~ ^[Yy]$ ]]; then
        # Docker-based setup
        start_services_docker
    else
        # Local development setup
        install_dependencies_local
        start_services_local
    fi
    
    print_section "Setup Complete"
    echo -e "Please check the requirements.md file for more information about API keys and dependencies."
}

# Run the main function
main