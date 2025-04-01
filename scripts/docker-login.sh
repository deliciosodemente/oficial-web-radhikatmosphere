#!/bin/bash

# Source environment variables from .env
source "$(dirname "$0")/../.env.txt"

echo "Logging into NVIDIA NGC container registry..."
docker login nvcr.io -u '$oauthtoken' --password-stdin <<< "$NVIDIA_NGC_API_KEY"