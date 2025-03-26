#!/bin/bash

# Generar clave SSH si no existe
if [ ! -f ~/.ssh/hostinger_key ]; then
    echo "Generando nueva clave SSH para Hostinger..."
    ssh-keygen -t rsa -b 4096 -f ~/.ssh/hostinger_key -N ""
fi

# Mostrar la clave pública para agregar a Hostinger
echo "Tu clave pública SSH es:"
cat ~/.ssh/hostinger_key.pub

# Verificar la conexión
echo "Verificando conexión con Hostinger..."
python3 -c "
from backend.config.hostinger_config import HostingerConfig
config = HostingerConfig()
if config.verify_connection():
    print('Conexión exitosa con Hostinger')
else:
    print('Error al conectar con Hostinger')
"

# Verificar configuración del dominio
echo "Verificando configuración del dominio..."
python3 -c "
from backend.config.hostinger_config import HostingerConfig
config = HostingerConfig()
domain_info = config.verify_domain_config()
print(domain_info)
" 