#!/bin/bash

# Colores para mensajes
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}Iniciando proceso de despliegue...${NC}"

# Verificar variables de entorno
if [ -z "$HOSTINGER_API_KEY" ] || [ -z "$HOSTINGER_SSH_HOST" ] || [ -z "$HOSTINGER_SSH_USERNAME" ]; then
    echo -e "${RED}Error: Faltan variables de entorno necesarias${NC}"
    exit 1
fi

# 1. Construir el frontend de Unity
echo -e "${GREEN}Construyendo frontend de Unity...${NC}"
cd frontend/UnityProject
unity -batchmode -quit -projectPath . -buildWebGLPlayer ../build/WebGL
if [ $? -ne 0 ]; then
    echo -e "${RED}Error al construir el frontend de Unity${NC}"
    exit 1
fi

# 2. Construir el backend
echo -e "${GREEN}Construyendo backend...${NC}"
cd ../../backend
python3 -m pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo -e "${RED}Error al instalar dependencias del backend${NC}"
    exit 1
fi

# 3. Ejecutar pruebas
echo -e "${GREEN}Ejecutando pruebas...${NC}"
python3 -m pytest tests/
if [ $? -ne 0 ]; then
    echo -e "${RED}Error en las pruebas${NC}"
    exit 1
fi

# 4. Desplegar a Hostinger
echo -e "${GREEN}Desplegando a Hostinger...${NC}"
python3 -c "
from services.hostinger_service import HostingerService
import asyncio

async def deploy():
    hostinger = HostingerService()
    
    # Desplegar frontend
    frontend_result = await hostinger.deploy_frontend('../frontend/build/WebGL')
    print('Frontend:', frontend_result)
    
    # Desplegar backend
    backend_result = await hostinger.deploy_backend('.')
    print('Backend:', backend_result)
    
    # Configurar SSL
    ssl_result = await hostinger.configure_ssl()
    print('SSL:', ssl_result)
    
    # Obtener estadísticas
    stats = await hostinger.get_hosting_stats()
    print('Estadísticas:', stats)

asyncio.run(deploy())
"

if [ $? -ne 0 ]; then
    echo -e "${RED}Error en el despliegue a Hostinger${NC}"
    exit 1
fi

# 5. Verificar despliegue
echo -e "${GREEN}Verificando despliegue...${NC}"
curl -s https://radhikatmosphere.com/api/health > /dev/null
if [ $? -ne 0 ]; then
    echo -e "${RED}Error: El backend no está respondiendo${NC}"
    exit 1
fi

curl -s https://radhikatmosphere.com/unity > /dev/null
if [ $? -ne 0 ]; then
    echo -e "${RED}Error: El frontend no está accesible${NC}"
    exit 1
fi

echo -e "${GREEN}Despliegue completado exitosamente!${NC}"
echo -e "Frontend: https://radhikatmosphere.com/unity"
echo -e "Backend: https://radhikatmosphere.com/api" 