#!/bin/bash

# Exit on error
set -e

# Load environment variables
if [ -f .env ]; then
    source .env
fi

# Check required environment variables
required_vars=("AWS_ACCESS_KEY_ID" "AWS_SECRET_ACCESS_KEY" "AWS_REGION" "LIGHTSAIL_IP" "LIGHTSAIL_SSH_USER")
for var in "${required_vars[@]}"; do
    if [ -z "${!var}" ]; then
        echo "ERROR: La variable $var no está configurada en .env"
        exit 1
    fi
done

# Build frontend
echo "Construyendo frontend..."
npm install
npm run build

# Ejecutar script de despliegue en Lightsail
echo "Iniciando despliegue en AWS Lightsail..."
python3 scripts/deploy_lightsail.py

# Start backend service with PM2
echo "Iniciando servicio backend..."
ssh -i "${LIGHTSAIL_SSH_KEY_PATH}" ${LIGHTSAIL_SSH_USER}@${LIGHTSAIL_IP} \
  "pm2 start python3 backend/main.py --name 'backend-service' --interpreter python3 --log logs/backend.log"

# Verify deployment status
echo "Verificando estado del servicio..."
ssh -i "${LIGHTSAIL_SSH_KEY_PATH}" ${LIGHTSAIL_SSH_USER}@${LIGHTSAIL_IP} "pm2 list"

# Add Docker authentication
chmod +x ./scripts/docker-login.sh
./scripts/docker-login.sh

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

# Recargar configuración de Nginx
echo "Recargando Nginx..."
sudo systemctl reload nginx

echo "Deployment complete!"