# DNS Configuration Guide for radhikatmosphere.com

This guide provides instructions for configuring DNS settings for the radhikatmosphere.com domain and its subdomains.

## Domain Registration

If you haven't already registered the domain, you can do so through a domain registrar like Namecheap, GoDaddy, or directly through AWS Route 53 if you're using their hosting services.

## DNS Records Configuration

### Main Domain (radhikatmosphere.com)

Configure the following DNS records for the main domain:

| Type | Name | Value | TTL |
|------|------|-------|-----|
| A | @ | Your server IP address | 3600 |
| A | www | Your server IP address | 3600 |
| CNAME | * | radhikatmosphere.com | 3600 |
| MX | @ | Your mail server (if applicable) | 3600 |
| TXT | @ | v=spf1 include:_spf.google.com ~all | 3600 |

### Subdomains

Configure the following DNS records for the subdomains:

#### Omniverse Subdomain (omniverse.radhikatmosphere.com)

| Type | Name | Value | TTL |
|------|------|-------|-----|
| A | omniverse | Your server IP address | 3600 |

#### Agent Subdomain (agent.radhikatmosphere.com)

| Type | Name | Value | TTL |
|------|------|-------|-----|
| A | agent | Your server IP address | 3600 |

## SSL Certificate Configuration

After setting up the DNS records, you'll need to obtain SSL certificates for secure HTTPS connections. This project uses Let's Encrypt for free SSL certificates, which are automatically configured using the `init-letsencrypt.sh` script.

## Verifying DNS Configuration

You can verify your DNS configuration using the following methods:

1. **Using dig command**:
   ```bash
   dig radhikatmosphere.com
   dig www.radhikatmosphere.com
   dig omniverse.radhikatmosphere.com
   dig agent.radhikatmosphere.com
   ```

2. **Using online DNS lookup tools**:
   - [MxToolbox](https://mxtoolbox.com/DNSLookup.aspx)
   - [DNSChecker](https://dnschecker.org/)

## DNS Propagation

After making changes to your DNS records, it may take some time (usually a few hours, but sometimes up to 48 hours) for the changes to propagate across the internet. During this time, some users may see the old configuration while others see the new one.

## Security Considerations

1. **Enable DNSSEC**: If your domain registrar supports it, enable DNSSEC to protect against DNS spoofing attacks.

2. **Restrict Zone Transfers**: Ensure that zone transfers are restricted to prevent unauthorized access to your DNS information.

3. **Use Strong TTL Values**: Set appropriate TTL (Time To Live) values. Lower values allow for quicker updates but increase DNS traffic.

## Troubleshooting

If you encounter issues with your DNS configuration:

1. Verify that the DNS records are correctly set up with your domain registrar or DNS provider.
2. Check for typos in domain names or IP addresses.
3. Ensure that your server's firewall allows incoming connections on ports 80 (HTTP) and 443 (HTTPS).
4. If using a CDN or proxy service, ensure it's correctly configured to point to your server.

## Additional Resources

- [DNS Basics](https://www.cloudflare.com/learning/dns/what-is-dns/)
- [Let's Encrypt Documentation](https://letsencrypt.org/docs/)
- [AWS Route 53 Documentation](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/Welcome.html)