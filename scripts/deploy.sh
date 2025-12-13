#!/bin/bash
set -e

# 1. Pull latest changes
echo "Pulling latest changes..."
git pull origin main

# 2. Build and start containers
echo "Starting services with Docker..."
docker-compose up -d --build

# 3. Prune unused images (optional, to save space)
docker image prune -f

echo "Deployment complete! Server is running."
