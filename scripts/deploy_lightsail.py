#!/usr/bin/env python3

import os
import sys
import subprocess
import argparse
import shutil
import tempfile
from pathlib import Path

# Añadir el directorio raíz del proyecto al path para importar módulos
sys.path.append(str(Path(__file__).parent.parent))

from backend.config.lightsail_deploy_config import LightsailDeployConfig

# Colores para mensajes en la terminal
COLORS = {
    'GREEN': '\033[0;32m',
    'YELLOW': '\033[1;33m',
    'RED': '\033[0;31m',
    'NC': '\033[0m'  # No Color
}

def print_colored(message, color):
    """Imprime un mensaje con color"""
    print(f"{COLORS[color]}{message}{COLORS['NC']}")

def run_command(command, cwd=None):
    """Ejecuta un comando y retorna su salida"""
    print_colored(f"Ejecutando: {command}", 'YELLOW')
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            text=True,
            capture_output=True,
            cwd=cwd
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print_colored(f"Error al ejecutar el comando: {e}", 'RED')
        print_colored(f"Salida de error: {e.stderr}", 'RED')
        sys.exit(1)

def create_deploy_package(config, temp_dir):
    """Crea un paquete de despliegue con los archivos necesarios"""
    print_colored("Creando paquete de despliegue...", 'GREEN')
    
    # Crear directorio temporal para el paquete
    deploy_dir = os.path.join(temp_dir, "deploy")
    os.makedirs(deploy_dir, exist_ok=True)
    
    # Copiar archivos al directorio de despliegue
    project_root = Path(__file__).parent.parent
    for file_path in config.deploy_files:
        source = os.path.join(project_root, file_path)
        dest = os.path.join(deploy_dir, file_path)
        
        if os.path.isdir(source):
            if os.path.exists(dest):
                shutil.rmtree(dest)
            shutil.copytree(source, dest)
        else:
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            shutil.copy2(source, dest)
    
    # Crear archivo tar.gz
    archive_path = os.path.join(temp_dir, "deploy.tar.gz")
    run_command(f"tar -czf {archive_path} -C {deploy_dir} .")
    
    return archive_path

def upload_to_lightsail(config, archive_path):
    """Sube el paquete de despliegue a Lightsail"""
    print_colored("Subiendo paquete a Lightsail...", 'GREEN')
    
    # Expandir la ruta de la clave SSH
    ssh_key_path = os.path.expanduser(config.ssh_key_path)
    
    # Verificar que la clave SSH existe
    if not os.path.isfile(ssh_key_path):
        print_colored(f"Error: La clave SSH no existe en {ssh_key_path}", 'RED')
        sys.exit(1)
    
    # Subir el archivo
    scp_command = f"scp -i {ssh_key_path} -P {config.ssh_port} {archive_path} {config.ssh_user}@{config.server_ip}:/tmp/deploy.tar.gz"
    run_command(scp_command)

def deploy_on_lightsail(config):
    """Ejecuta los comandos de despliegue en el servidor Lightsail"""
    print_colored("Desplegando en Lightsail...", 'GREEN')
    
    # Expandir la ruta de la clave SSH
    ssh_key_path = os.path.expanduser(config.ssh_key_path)
    
    # Crear directorio remoto si no existe
    mkdir_cmd = f"ssh -i {ssh_key_path} -p {config.ssh_port} {config.ssh_user}@{config.server_ip} 'mkdir -p {config.remote_app_dir}'"
    run_command(mkdir_cmd)
    
    # Descomprimir y desplegar
    deploy_commands = [
        f"cd /tmp",
        f"tar -xzf /tmp/deploy.tar.gz -C {config.remote_app_dir}",
        f"rm /tmp/deploy.tar.gz"
    ]
    
    # Añadir comandos post-despliegue
    deploy_commands.extend(config.get_formatted_commands(config.post_deploy_commands))
    
    # Configurar Nginx
    nginx_commands = [
        f"sudo cp {config.remote_app_dir}/{config.nginx_config_file} {config.nginx_target_file.format(remote_nginx_dir=config.remote_nginx_dir)}",
        f"sudo /opt/bitnami/nginx/sbin/nginx -t"
    ]
    deploy_commands.extend(nginx_commands)
    
    # Añadir comandos de reinicio
    deploy_commands.extend(config.get_formatted_commands(config.restart_commands))
    
    # Ejecutar comandos en el servidor
    ssh_command = f"ssh -i {ssh_key_path} -p {config.ssh_port} {config.ssh_user}@{config.server_ip} '{'; '.join(deploy_commands)}'"
    output = run_command(ssh_command)
    print(output)

def main():
    """Función principal"""
    parser = argparse.ArgumentParser(description="Desplegar aplicación en Amazon Lightsail")
    parser.add_argument("--build", action="store_true", help="Construir la aplicación antes de desplegar")
    args = parser.parse_args()
    
    # Cargar configuración
    config = LightsailDeployConfig()
    
    # Directorio raíz del proyecto
    project_root = Path(__file__).parent.parent
    
    # Construir la aplicación si se solicita
    if args.build:
        print_colored("Construyendo la aplicación...", 'GREEN')
        run_command("npm run build", cwd=str(project_root))
    
    # Crear directorio temporal
    with tempfile.TemporaryDirectory() as temp_dir:
        # Crear paqu