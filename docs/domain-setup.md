# Domain Configuration for radhikatmosphere.com

This document provides information about the domain configuration for the Radhikat Mosphere platform, including the main domain and subdomains for specialized services.

## Domain Structure

The platform uses the following domain structure:

- **Main Domain**: www.radhikatmosphere.com
  - Primary website for users
  - Secure access with HTTPS
  - Redirects from non-www to www for consistency

- **GPU Resources Subdomain**: omniverse.radhikatmosphere.com
  - Dedicated to NVIDIA Omniverse GPU-accelerated services
  - Optimized for high-performance computing tasks
  - Direct access to S3 bucket for Omniverse assets

- **Agent Subdomain**: agent.radhikatmosphere.com
  - Hosts AI agent services
  - Separate environment for agent operations

## Security Features

All domains implement the following security features:

- **HTTPS Only**: All HTTP traffic is automatically redirected to HTTPS
- **SSL/TLS**: Using Let's Encrypt certificates with automatic renewal
- **Security Headers**:
  - Strict-Transport-Security (HSTS)
  - X-Content-Type-Options
  - X-Frame-Options
  - X-XSS-Protection
  - Content-Security-Policy

## S3 Bucket Integration

The platform integrates with NVIDIA Omniverse S3 bucket:

- Main bucket: `s3://radhikatmosphere--use1-az6--x-s3/.nvidia-omniverse/`
- Accessible via API endpoints at `/api/s3/`
- Special optimized access for the Omniverse subdomain at `omniverse.radhikatmosphere.com/s3/`

## Setup Instructions

### Prerequisites

- Registered domain (radhikatmosphere.com)
- Server with Docker and Docker Compose installed
- DNS configured according to the [DNS Configuration Guide](dns-configuration.md)

### Initial Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/oficial-web-radhikatmosphere.git
   cd oficial-web-radhikatmosphere
   ```

2. Create required directories:
   ```bash
   mkdir -p certbot/www certbot/conf public
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your AWS credentials and other settings
   ```

4. Initialize SSL certificates:
   ```bash
   chmod +x scripts/init-letsencrypt.sh
   ./scripts/init-letsencrypt.sh
   ```

5. Start the services:
   ```bash
   docker-compose up -d
   ```

### Verifying the Setup

After completing the setup, verify that the domains are working correctly:

1. Visit https://www.radhikatmosphere.com in your browser
2. Check that HTTPS is working and the certificate is valid
3. Test the subdomains:
   - https://omniverse.radhikatmosphere.com
   - https://agent.radhikatmosphere.com

## Maintenance

### SSL Certificate Renewal

Let's Encrypt certificates are valid for 90 days. The certbot service in the Docker Compose setup automatically attempts renewal every 12 hours when certificates are close to expiration.

### Updating Configuration

To update the Nginx configuration:

1. Edit the configuration files in `infrastructure/nginx/`
2. Restart the Nginx service:
   ```bash
   docker-compose restart nginx
   ```

## Troubleshooting

### Common Issues

1. **Certificate Issues**:
   - Check the certbot logs: `docker-compose logs certbot`
   - Verify that ports 80 and 443 are open on your server
   - Ensure DNS is correctly configured

2. **Nginx Configuration**:
   - Check the Nginx logs: `docker-compose logs nginx`
   - Validate the configuration: `docker-compose exec nginx nginx -t`

3. **Domain Not Resolving**:
   - Verify DNS settings with your domain registrar
   - Check DNS propagation using online tools

## Additional Resources

- [Nginx Documentation](https://nginx.org/en/docs/)
- [Let's Encrypt Documentation](https://letsencrypt.org/docs/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)