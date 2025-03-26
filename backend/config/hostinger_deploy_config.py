import os
from dataclasses import dataclass
from typing import Optional

@dataclass
class HostingerDeployConfig:
    """Configuración para el despliegue en Hostinger"""
    
    # Credenciales y conexión
    api_key: str = os.getenv("HOSTINGER_API_KEY", "")
    ssh_host: str = os.getenv("HOSTINGER_SSH_HOST", "")
    ssh_port: int = int(os.getenv("HOSTINGER_SSH_PORT", "22"))
    ssh_username: str = os.getenv("HOSTINGER_SSH_USERNAME", "")
    ssh_key_path: str = os.getenv("HOSTINGER_SSH_KEY_PATH", "~/.ssh/hostinger_key")
    
    # Dominio y rutas
    domain: str = os.getenv("HOSTINGER_DOMAIN", "radhikatmosphere.com")
    frontend_path: str = os.getenv("HOSTINGER_FRONTEND_PATH", "/public_html/unity")
    backend_path: str = os.getenv("HOSTINGER_BACKEND_PATH", "/public_html/api")
    
    # Configuración de SSL
    ssl_email: str = os.getenv("HOSTINGER_SSL_EMAIL", "")
    ssl_domains: list = None
    
    def __post_init__(self):
        if self.ssl_domains is None:
            self.ssl_domains = [self.domain, f"www.{self.domain}"]
    
    def validate(self) -> bool:
        """Valida que la configuración sea correcta"""
        required_vars = [
            self.api_key,
            self.ssh_host,
            self.ssh_username,
            self.domain,
            self.ssl_email
        ]
        
        return all(required_vars)
    
    def get_ssh_config(self) -> dict:
        """Retorna la configuración SSH para paramiko"""
        return {
            "hostname": self.ssh_host,
            "port": self.ssh_port,
            "username": self.ssh_username,
            "key_filename": os.path.expanduser(self.ssh_key_path)
        }
    
    def get_frontend_url(self) -> str:
        """Retorna la URL del frontend"""
        return f"https://{self.domain}/unity"
    
    def get_backend_url(self) -> str:
        """Retorna la URL del backend"""
        return f"https://{self.domain}/api"
    
    def get_health_check_url(self) -> str:
        """Retorna la URL para verificar la salud del backend"""
        return f"{self.get_backend_url()}/health" 