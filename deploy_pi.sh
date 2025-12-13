#!/bin/bash

# Raspberry Pi Deployment Script for LLAMA Chat Backend
# This script sets up and deploys the Docker container on Raspberry Pi

set -e

echo "Starting Raspberry Pi deployment for LLAMA Chat Backend..."

# Check if running on Raspberry Pi (ARM64)
if [[ $(uname -m) != "aarch64" ]]; then
    echo "Warning: This script is designed for Raspberry Pi (ARM64). Current architecture: $(uname -m)"
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Docker is not installed. Installing Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
    echo "Docker installed. Please log out and back in, or run 'newgrp docker' to use Docker."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "Docker Compose is not installed. Installing..."
    sudo apt-get update
    sudo apt-get install -y docker-compose
fi

# Clone or update the repository
REPO_DIR="dgc_cw"
if [ -d "$REPO_DIR" ]; then
    echo "Repository exists. Pulling latest changes..."
    cd $REPO_DIR
    git pull
    cd ..
else
    echo "Cloning repository..."
    git clone https://github.com/DondlingerGeneralContracting/dgc_cw.git
fi

cd $REPO_DIR

# Check for environment variables
if [ -z "$LLAMA_API_KEY" ]; then
    echo "LLAMA_API_KEY environment variable not set."
    read -p "Enter your LLAMA API key: " -s LLAMA_API_KEY
    echo
    export LLAMA_API_KEY="$LLAMA_API_KEY"
fi

if [ -z "$LLAMA_API_URL" ]; then
    export LLAMA_API_URL="https://api.llama.com/v1/chat/completions"
fi

# Navigate to docker directory
cd docker

# Build and run the container
echo "Building and starting Docker container..."
docker-compose up -d --build

# Wait for container to start
echo "Waiting for container to start..."
sleep 30

# Check if container is running
if docker-compose ps | grep -q "Up"; then
    echo "Deployment successful!"
    echo "API available at: http://localhost:5000/api/chat"
    echo "Health check: http://localhost:5000/health"

    # Get container logs
    echo "Container logs:"
    docker-compose logs --tail=20
else
    echo "Deployment failed. Checking logs..."
    docker-compose logs
    exit 1
fi

echo "Raspberry Pi deployment completed."