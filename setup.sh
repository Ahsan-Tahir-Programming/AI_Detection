#!/bin/bash

# Full Stack Frontend + Backend Setup Script
# This script guides you through setting up the complete AI Detection System

echo "=========================================="
echo "AI Detection System - Full Stack Setup"
echo "=========================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Step 1: Backend Setup${NC}"
echo "Installing Python dependencies..."
pip install -r requirements.txt
echo -e "${GREEN}✓ Backend dependencies installed${NC}"
echo ""

echo -e "${YELLOW}Step 2: Frontend Setup${NC}"
echo "Installing Node.js dependencies..."
cd frontend
npm install
echo -e "${GREEN}✓ Frontend dependencies installed${NC}"
cd ..
echo ""

echo -e "${YELLOW}Step 3: Running the Application${NC}"
echo ""
echo "Option 1: Run separately (Recommended for development)"
echo "  Terminal 1 - Backend:"
echo "    cd ."
echo "    uvicorn app.main:app --reload --port 8000"
echo ""
echo "  Terminal 2 - Frontend:"
echo "    cd frontend"
echo "    npm run dev"
echo ""
echo "Option 2: Run with Docker Compose (Recommended for production)"
echo "    docker-compose up --build"
echo ""

echo -e "${YELLOW}Step 4: Access the Application${NC}"
echo ""
echo "Backend API:"
echo "  - Main App: http://localhost:8000"
echo "  - Swagger Docs: http://localhost:8000/docs"
echo ""
echo "Frontend:"
echo "  - Web App: http://localhost:3000"
echo ""

echo -e "${YELLOW}Step 5: Test the System${NC}"
echo "1. Open http://localhost:3000 in your browser"
echo "2. Select a model (e.g., 'nestle_chiller')"
echo "3. Provide image URL"
echo "4. Configure detection parameters"
echo "5. Click 'Run Detection'"
echo ""

echo -e "${GREEN}Setup Complete!${NC}"
echo ""
echo "For detailed documentation, see:"
echo "  - Main Readme: README.md"
echo "  - Frontend: frontend/README.md"
echo "  - Documentation: docs/FULL_STACK_SETUP.md"
