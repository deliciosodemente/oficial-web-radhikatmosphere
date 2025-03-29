#!/usr/bin/env python3

import os
from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class LightsailDeployConfig:
    """
    Configuración para el despliegue en Amazon Lightsail
    """
    # Información del servidor Lightsail
    server_ip: str = os.getenv("LIGHTSAIL_IP", "52.86.51.202")
    ssh_user: str = os.getenv("LIGHTSAIL_SSH_USER", "bitnami")
    ssh_port: int = int(os.getenv("LIGHTSAIL_SSH_PORT", "22"))
    ssh_key_path: str = os.getenv("LIGHTSAIL_SSH_KEY_PATH", "~/.ssh/lightsail.pem")
    
    # Información del dominio
    domain: str = os.getenv("DOMAIN", "radhikatmosphere.com")
    
    # Directorios remotos
    remote_app_dir: str = os.getenv("LIGHTSAIL_REMOTE_DIR", "/opt/bitnami/apache/htdocs/radhikatmosphere")
    remote_nginx_dir: str = os.getenv("LIGHTSAIL_NGINX_DIR", "/opt/bitnami/nginx/conf/server_blocks")
    
    # Archivos de configuración
    nginx_config_file: str = os.getenv("NGINX_CONFIG_FILE", "config/nginx.conf")
    nginx_target_file: str = os.getenv("NGINX_TARGET_FILE", "{remote_nginx_dir}/radhikatmosphere.conf")
    
    # Archivos a desplegar
    deploy_files: List[str] = field(default_factory=lambda: [
        "build",              # Frontend compilado
        "backend",            # Código del backend
        "config",             # Archivos de configuración
        "package.json",       # Dependencias de Node.js
        "package-lock.json",  # Versiones exactas de dependencias
        "server.js"           # Archivo principal del servidor Node.js
    ])
    
    # Comandos post-despliegue
    post_deploy_commands: List[str] = field(default_factory=lambda: [
        "cd {remote_app_dir}",
        "npm install --production",
        "pm2 stop server || true",  # Detener el servidor si está en ejecución
        "pm2 start server.js --name radhikatmosphere"
    ])
    
    # Comandos de reinicio
    restart_commands: List[str] = field(default_factory=lambda: [
        "sudo /opt/bitnami/ctlscript.sh restart nginx"
    ])
    
    def get_formatted_commands(self, commands: List[str]) -> List[str]:
        """
        Formatea los comandos con las variables de configuración
        """
        formatted_commands = []
        for cmd in commands:
            formatted_cmd = cmd.format(
                remote_app_dir=self.remote_app_dir,
                remote_nginx_dir=self.remote_nginx_dir,
                domain=self.domain,
                server_ip=self.server_ip
            )
            formatted_commands.append(formatted_cmd)
        return formatted_commands