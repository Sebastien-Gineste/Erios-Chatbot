#!/bin/bash

# Script to build and run the ERIOS ChatBot Docker image
IMAGE_NAME=erios-chatbot
DOCKERFILE_PATH=eriosChatBot.Dockerfile
CONTAINER_NAME=erios-chatbot-container
PORT=8501


# Build the Docker image
echo "Building Docker image..."
docker build -f $DOCKERFILE_PATH -t $IMAGE_NAME .

# Stop and remove any existing container with the same name
docker rm -f $CONTAINER_NAME 2>/dev/null || true

# Load environment variables from .env file if it exists
if [ -f ".env" ]; then
    echo "Loading environment variables from .env file..."
    export $(cat ".env" | grep -v '^#' | xargs)
    echo "✅ Environment variables loaded"
else
    echo "⚠️  No .env file found. Make sure OPENAI_KEY is set in your environment."
fi

# Run the Docker container with environment variable
echo "Running Docker container..."
docker run --name $CONTAINER_NAME \
    -p $PORT:8501 \
    -e OPENAI_KEY="$OPENAI_KEY" \
    $IMAGE_NAME 