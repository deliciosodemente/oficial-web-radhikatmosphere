import os
from pydantic import BaseModel
from typing import Optional

class AWSDeployConfig(BaseModel):
    """Configuración para el despliegue en AWS"""
    
    # AWS Credentials
    aws_access_key_id: str = os.getenv("AWS_ACCESS_KEY_ID", "")
    aws_secret_access_key: str = os.getenv("AWS_SECRET_ACCESS_KEY", "")
    aws_region: str = os.getenv("AWS_REGION", "us-east-1")
    
    # EC2 Configuration (if using EC2)
    ec2_host: str = os.getenv("AWS_EC2_HOST", "")
    ec2_port: int = int(os.getenv("AWS_EC2_PORT", "22"))
    ec2_username: str = os.getenv("AWS_EC2_USERNAME", "")
    ec2_key_path: str = os.getenv("AWS_EC2_KEY_PATH", "~/.ssh/aws_key")
    
    # S3 and CloudFront Configuration
    s3_bucket: str = os.getenv("AWS_S3_BUCKET", "radhikatmosphere-assets")
    cloudfront_distribution_id: str = os.getenv("AWS_CLOUDFRONT_DISTRIBUTION_ID", "")
    
    # Domain Configuration
    domain: str = os.getenv("AWS_DOMAIN", "radhikatmosphere.com")
    frontend_path: str = os.getenv("AWS_FRONTEND_PATH", "/frontend")
    backend_path: str = os.getenv("AWS_BACKEND_PATH", "/api")
    
    # Route53 Configuration
    route53_hosted_zone_id: str = os.getenv("AWS_ROUTE53_HOSTED_ZONE_ID", "")
    
    # SSL Configuration
    ssl_email: str = os.getenv("AWS_SSL_EMAIL", "")
    acm_certificate_arn: str = os.getenv("AWS_ACM_CERTIFICATE_ARN", "")