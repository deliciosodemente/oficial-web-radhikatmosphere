#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test script for AWS configuration

This script tests the AWS configuration using the credentials and key files provided.
It verifies connections to S3, EC2/Lightsail, and other AWS services as configured.
"""

import os
import sys
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent))

from backend.config.aws_config import AWSConfig

def main():
    print("\n===== AWS Configuration Test =====\n")
    
    try:
        # Initialize AWS configuration
        print("Initializing AWS configuration...")
        aws_config = AWSConfig()
        print("AWS configuration initialized successfully.")
        
        # Print configuration details (masked for security)
        print("\nConfiguration Details:")
        print(f"- AWS Access Key ID: {aws_config.aws_access_key_id[:5]}...")
        print(f"- AWS Secret Access Key: {aws_config.aws_secret_access_key[:5]}...")
        print(f"- AWS Region: {aws_config.aws_region}")
        print(f"- S3 Bucket: {aws_config.s3_bucket}")
        
        if aws_config.ec2_host:
            print(f"- EC2/Lightsail Host: {aws_config.ec2_host}")
            print(f"- EC2/Lightsail Username: {aws_config.ec2_username}")
            print(f"- EC2/Lightsail Key Path: {aws_config.ec2_key_path}")
            print(f"  Key file exists: {os.path.exists(aws_config.ec2_key_path)}")
        else:
            print("- EC2/Lightsail: Not configured")
        
        # Verify connection to AWS services
        print("\nVerifying connection to AWS services...")
        aws_config.verify_connection()
        
        print("\n===== Test Complete =====\n")
        
    except Exception as e:
        print(f"\nError: {str(e)}")
        print("\n===== Test Failed =====\n")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())