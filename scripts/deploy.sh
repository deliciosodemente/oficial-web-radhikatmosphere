#!/bin/bash

# Exit on error
set -e

# Load environment variables
if [ -f .env ]; then
    source .env
fi

# Check required environment variables
if [ -z "$AWS_PROFILE" ] || [ -z "$AWS_REGION" ] || [ -z "$STACK_NAME" ]; then
    echo "Please set AWS_PROFILE, AWS_REGION and STACK_NAME environment variables"
    exit 1
fi

# Build frontend
echo "Building frontend..."
npm install
npm run build

# Deploy CloudFormation stack
echo "Deploying infrastructure..."
aws cloudformation deploy \
    --template-file infrastructure/cloudformation.yaml \
    --stack-name $STACK_NAME \
    --parameter-overrides \
        Environment=production \
    --capabilities CAPABILITY_IAM \
    --region $AWS_REGION \
    --profile $AWS_PROFILE

# Get S3 bucket name and CloudFront distribution ID
BUCKET_NAME=$(aws cloudformation describe-stacks \
    --stack-name $STACK_NAME \
    --query 'Stacks[0].Outputs[?OutputKey==`FrontendBucketName`].OutputValue' \
    --output text \
    --region $AWS_REGION \
    --profile $AWS_PROFILE)

CLOUDFRONT_ID=$(aws cloudformation describe-stacks \
    --stack-name $STACK_NAME \
    --query 'Stacks[0].Outputs[?OutputKey==`CloudFrontDistributionId`].OutputValue' \
    --output text \
    --region $AWS_REGION \
    --profile $AWS_PROFILE)

# Upload frontend to S3
echo "Uploading frontend to S3..."
aws s3 sync build/ s3://$BUCKET_NAME/ \
    --delete \
    --region $AWS_REGION \
    --profile $AWS_PROFILE

# Invalidate CloudFront cache
echo "Invalidating CloudFront cache..."
aws cloudfront create-invalidation \
    --distribution-id $CLOUDFRONT_ID \
    --paths "/*" \
    --region $AWS_REGION \
    --profile $AWS_PROFILE

echo "Deployment completed successfully!"