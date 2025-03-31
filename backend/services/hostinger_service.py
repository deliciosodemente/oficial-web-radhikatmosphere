import os
import paramiko
from typing import Dict, Any, Optional
from dotenv import load_dotenv

class HostingerService:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv('HOSTINGER_API_KEY')
        self.ssh_host = os.getenv('HOSTINGER_SSH_HOST')
        self.ssh_port = int(os.getenv('HOSTINGER_SSH_PORT', '22'))
        self.ssh_username = os.getenv('HOSTINGER_SSH_USERNAME')
        self.ssh_key_path = os.getenv('HOSTINGER_SSH_KEY_PATH')
        self.domain = 'radhikatmosphere.com'
        self.web_root = '/public_html'

    async def deploy_frontend(self, unity_build_path: str) -> Dict[str, Any]:
        """Despliega el frontend de Unity a Hostinger"""
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(
                self.ssh_host,
                port=self.ssh_port,
                username=self.ssh_username,
                key_filename=self.ssh_key_path
            )
            
            sftp = ssh.open_sftp()
            remote_path = f"{self.web_root}/unity"
            
            # Crear directorio si no existe
            try:
                sftp.stat(remote_path)
            except:
                sftp.mkdir(remote_path)
            
            # Subir archivos del build de Unity
            self._upload_directory(sftp, unity_build_path, remote_path)
            
            return {
                "status": "success",
                "message": "Frontend desplegado exitosamente",
                "url": f"https://{self.domain}/unity"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error en el despliegue: {str(e)}"
            }

    async def deploy_backend(self, backend_path: str) -> Dict[str, Any]:
        """Despliega el backend a Hostinger"""
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(
                self.ssh_host,
                port=self.ssh_port,
                username=self.ssh_username,
                key_filename=self.ssh_key_path
            )
            
            sftp = ssh.open_sftp()
            remote_path = f"{self.web_root}/api"
            
            # Crear directorio si no existe
            try:
                sftp.stat(remote_path)
            except:
                sftp.mkdir(remote_path)
            
            # Subir archivos del backend
            self._upload_directory(sftp, backend_path, remote_path)
            
            # Configurar el entorno virtual y dependencias
            commands = [
                f"cd {remote_path}",
                "python3 -m venv venv",
                "source venv/bin/activate",
                "pip install -r requirements.txt",
                "systemctl restart omniverse-api"
            ]
            
            for cmd in commands:
                stdin, stdout, stderr = ssh.exec_command(cmd)
                if stderr.channel.recv_exit_status() != 0:
                    raise Exception(f"Error ejecutando comando: {cmd}")
            
            return {
                "status": "success",
                "message": "Backend desplegado exitosamente",
                "api_url": f"https://{self.domain}/api"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error en el despliegue: {str(e)}"
            }

    def _upload_directory(self, sftp, local_path: str, remote_path: str):
        """Sube un directorio completo al servidor"""
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

    async def get_hosting_stats(self) -> Dict[str, Any]:
        """Obtiene estadísticas del hosting"""
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(
                self.ssh_host,
                port=self.ssh_port,
                username=self.ssh_username,
                key_filename=self.ssh_key_path
            )
            
            # Obtener uso de disco
            stdin, stdout, stderr = ssh.exec_command("df -h /")
            disk_usage = stdout.read().decode()
            
            # Obtener uso de memoria
            stdin, stdout, stderr = ssh.exec_command("free -m")
            memory_usage = stdout.read().decode()
            
            # Obtener logs de acceso
            stdin, stdout, stderr = ssh.exec_command("tail -n 100 /var/log/apache2/access.log")
            access_logs = stdout.read().decode()
            
            return {
                "status": "success",
                "disk_usage": disk_usage,
                "memory_usage": memory_usage,
                "recent_access_logs": access_logs
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error obteniendo estadísticas: {str(e)}"
            }

    async def configure_ssl(self) -> Dict[str, Any]:
        """Configura SSL para el dominio"""
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(
                self.ssh_host,
                port=self.ssh_port,
                username=self.ssh_username,
                key_filename=self.ssh_key_path
            )
            
            # Verificar si ya existe certificado SSL
            stdin, stdout, stderr = ssh.exec_command(f"certbot certificates | grep {self.domain}")
            if stdout.channel.recv_exit_status() == 0:
                return {
                    "status": "success",
                    "message": "SSL ya está configurado"
                }
            
            # Instalar certificado SSL
            commands = [
                f"certbot --apache -d {self.domain} -d www.{self.domain} --non-interactive --agree-tos --email admin@{self.domain}"
            ]
            
            for cmd in commands:
                stdin, stdout, stderr = ssh.exec_command(cmd)
                if stderr.channel.recv_exit_status() != 0:
                    raise RuntimeError(f"Error ejecutando comando: {cmd}")
            
            return {
                "status": "success",

                "message": "SSL configurado exitosamente"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error configurando SSL: {str(e)}"
            } 