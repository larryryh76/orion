#!/bin/bash

# Deploy to DigitalOcean/AWS/Google Cloud
echo "Deploying Orion to cloud server..."

# Build Docker image
docker build -t orion-system ./docker

# Deploy to cloud (example for DigitalOcean)
docker tag orion-system registry.digitalocean.com/your-registry/orion-system
docker push registry.digitalocean.com/your-registry/orion-system

# Or deploy to free services
echo "Alternative free deployments:"
echo "1. Railway: railway up"
echo "2. Render: render deploy"
echo "3. Fly.io: flyctl deploy"

echo "Server will be accessible at: https://your-domain.com"
echo "Set webhook in mobile app to receive notifications"