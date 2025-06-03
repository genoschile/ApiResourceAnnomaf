#!/bin/bash
#
# Author: Bnjmn <bastudillo.alarcon@gmail.com>
# Date: 2025-04-09
# Description: This script builds a Docker image for the AWS Translate service.
# Usage: ./install.sh

IMAGE_NAME="aws-translate"

IMAGE_NAME="aws-translate" 

error_exit() {
    echo "Error: $1"
    exit 1
}

command -v docker &> /dev/null || error_exit "Docker is not installed"
docker info &> /dev/null || error_exit "Docker is not running"
[ -f "dockerfile" ] || error_exit "No Dockerfile found in the current directory."
[ -w "." ] || error_exit "You do not have write permissions in the current directory"
[ -f ".env" ] || echo "The .env file was not found"

read -p "Are you sure you want to build the Docker image? '${IMAGE_NAME}'? (s/n): " confirm
if [[ ! "$confirm" =~ ^[sS]$ ]]; then
    echo "Process canceled by the user"
    exit 0
fi

echo "Building the Docker image '${IMAGE_NAME}'..."
docker build -t "${IMAGE_NAME}" .

if [ $? -eq 0 ]; then
    echo "The '${IMAGE_NAME}' image was built successfully!"
else
    echo "Error: There was a problem building the image."
    exit 1
fi
