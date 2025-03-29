import os
import paramiko
from dotenv import load_dotenv

class HostingerConfig:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv('HOSTINGER_API_KEY')
        self.domain = 'radhikatmosphere.com'
        self.ssh_host = os.getenv('HOSTINGER_SSH_HOST')
        self.ssh_port = int(os.getenv('HOSTINGER_SSH_PORT', '22'))
        self.ssh_username = os.getenv('HOSTINGER_SSH_USERNAME')
        self.ssh_key_path = os.getenv('HOSTINGER_SSH_KEY_PATH')

    def verify_connection(self):
        """Verifica la conexión con Hostinger"""
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.RejectPolicy())
            ssh.connect(
                self.ssh_host,
                port=self.ssh_port,

                username=self.ssh_username,
                key_filename=self.ssh_key_path
            )
            return True
        except Exception as e:
            print(f"Error de conexión: {str(e)}")
            return False

    def deploy_website(self, local_path, remote_path):
        """Despliega el sitio web a Hostinger"""
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
            self._upload_directory(sftp, local_path, remote_path)
            return True
        except Exception as e:
            print(f"Error en el despliegue: {str(e)}")
            return False

    def _upload_directory(self, sftp, local_path, remote_path):
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

    def verify_domain_config(self):
        """Verifica la configuración del dominio"""
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(
                self.ssh_host,
                port=self.ssh_port,
                username=self.ssh_username,
                key_filename=self.ssh_key_path
            )
            
            stdin, stdout, stderr = ssh.exec_command(f"dig {self.domain}")
            return stdout.read().decode()
        except Exception as e:
            print(f"Error al verificar el dominio: {str(e)}")
            return None 