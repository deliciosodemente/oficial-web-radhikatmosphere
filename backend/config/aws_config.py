import os
import boto3
import time
from dotenv import load_dotenv
import paramiko

class AWSConfig:
    def __init__(self):
        load_dotenv()
        self.aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
        if not self.aws_access_key_id:
            raise ValueError("AWS_ACCESS_KEY_ID environment variable is missing")
        self.aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
        if not self.aws_secret_access_key:
            raise ValueError("AWS_SECRET_ACCESS_KEY environment variable is missing")
        self.aws_region = os.getenv('AWS_REGION', 'us-east-1')
        self.domain = 'radhikatmosphere.com'
        self.ec2_host = os.getenv('AWS_EC2_HOST')
        self.ec2_port = int(os.getenv('AWS_EC2_PORT', '22'))
        self.ec2_username = os.getenv('AWS_EC2_USERNAME')
        self.ec2_key_path = os.getenv('AWS_EC2_KEY_PATH')
        
        # S3 bucket configuration
        self.s3_bucket = os.getenv('AWS_S3_BUCKET')
        if not self.s3_bucket:
            raise ValueError("AWS_S3_BUCKET environment variable is missing")
        self.cloudfront_distribution_id = os.getenv('AWS_CLOUDFRONT_DISTRIBUTION_ID')
        
    def get_boto3_session(self):
        """Returns a boto3 session with AWS credentials"""
        return boto3.Session(

            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            region_name=self.aws_region
        )
    
    def verify_connection(self):
        """Verifies connection to AWS services"""
        try:
            # Verify AWS credentials by listing S3 buckets
            session = self.get_boto3_session()
            s3 = session.client('s3')
            s3.list_buckets()
            
            # Verify EC2 connection if host is provided
            if self.ec2_host and self.ec2_key_path:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.RejectPolicy())
                ssh.connect(
                    self.ec2_host,
                    port=self.ec2_port,

                    username=self.ec2_username,
                    key_filename=self.ec2_key_path
                )
                ssh.close()
            
            return True
        except Exception as e:
            print(f"Error connecting to AWS: {str(e)}")
            return False
    
    def deploy_to_s3(self, local_path, s3_prefix=''):
        """Deploys files to S3 bucket"""
        try:
            session = self.get_boto3_session()
            s3 = session.resource('s3')
            bucket = s3.Bucket(self.s3_bucket)
            
            # Upload all files from local_path to S3
            for root, dirs, files in os.walk(local_path):
                for file in files:
                    local_file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(local_file_path, local_path)
                    s3_key = f"{s3_prefix}/{relative_path}" if s3_prefix else relative_path
                    
                    # Upload file with appropriate content type
                    content_type = self._get_content_type(file)
                    bucket.upload_file(
                        local_file_path, 
                        s3_key,
                        ExtraArgs={'ContentType': content_type}
                    )
            
            # Invalidate CloudFront cache if distribution ID is provided
            if self.cloudfront_distribution_id:
                self._invalidate_cloudfront_cache()
                
            return True
        except Exception as e:
            print(f"Error deploying to S3: {str(e)}")
            return False
    
    def deploy_to_ec2(self, local_path, remote_path):
        """Deploys files to EC2 instance"""
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(
                self.ec2_host,
                port=self.ec2_port,
                username=self.ec2_username,
                key_filename=self.ec2_key_path
            )
            
            sftp = ssh.open_sftp()
            self._upload_directory(sftp, local_path, remote_path)
            ssh.close()
            return True
        except Exception as e:
            print(f"Error deploying to EC2: {str(e)}")
            return False
    
    def _upload_directory(self, sftp, local_path, remote_path):
        """Uploads a directory to the server"""
        for item in os.listdir(local_path):
            local_item = os.path.join(local_path, item)
            remote_item = f"{remote_path}/{item}"
            
            if os.path.isfile(local_item):
                sftp.put(local_item, remote_item)
            elif os.path.isdir(local_item):
                try:
                    sftp.stat(remote_item)
                except:
                    sftp.mkdir(remote_item)
                self._upload_directory(sftp, local_item, remote_item)
    
    def _get_content_type(self, filename):
        """Returns the content type based on file extension"""
        extension = os.path.splitext(filename)[1].lower()
        content_types = {
            '.html': 'text/html',
            '.css': 'text/css',
            '.js': 'application/javascript',
            '.json': 'application/json',
            '.png': 'image/png',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.gif': 'image/gif',
            '.svg': 'image/svg+xml',
            '.ico': 'image/x-icon',
            '.txt': 'text/plain',
            '.pdf': 'application/pdf',
            '.zip': 'application/zip'
        }
        return content_types.get(extension, 'application/octet-stream')
    
    def _invalidate_cloudfront_cache(self):
        """Invalidates CloudFront cache"""
        try:
            session = self.get_boto3_session()
            cloudfront = session.client('cloudfront')
            cloudfront.create_invalidation(
                DistributionId=self.cloudfront_distribution_id,
                InvalidationBatch={
                    'Paths': {
                        'Quantity': 1,
                        'Items': ['/*']
                    },
                    'CallerReference': str(int(time.time()))
                }
            )
            return True
        except Exception as e:
            print(f"Error invalidating CloudFront cache: {str(e)}")
            return False
    
    def verify_domain_config(self):
        """Verifies domain configuration"""
        try:
            session = self.get_boto3_session()
            route53 = session.client('route53')
            
            # Get hosted zones
            response = route53.list_hosted_zones_by_name(DNSName=self.domain)
            
            if not response['HostedZones']:
                return "Domain not found in Route53"
            
            hosted_zone_id = response['HostedZones'][0]['Id']
            
            # Get record sets
            records = route53.list_resource_record_sets(
                HostedZoneId=hosted_zone_id,
                StartRecordName=self.domain,
                StartRecordType='A',
                MaxItems='1'
            )
            
            return records
        except Exception as e:
            print(f"Error verifying domain: {str(e)}")
            return None