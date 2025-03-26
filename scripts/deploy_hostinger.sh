#!/bin/bash

# Colores para mensajes
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}Iniciando despliegue en Hostinger...${NC}"

# Verificar variables de entorno
if [ -z "$HOSTINGER_USER" ] || [ -z "$HOSTINGER_HOST" ] || [ -z "$HOSTINGER_PORT" ]; then
    echo -e "${RED}Error: Variables de entorno no configuradas${NC}"
    exit 1
fi

# Crear directorio temporal
TEMP_DIR="temp_deploy"
mkdir -p $TEMP_DIR

# Copiar archivos necesarios
echo "Copiando archivos..."
cp -r backend $TEMP_DIR/
cp -r frontend $TEMP_DIR/
cp requirements.txt $TEMP_DIR/
cp Dockerfile $TEMP_DIR/
cp docker-compose.yml $TEMP_DIR/

# Crear archivo .env en el servidor
cat > $TEMP_DIR/backend/.env << EOL
NVIDIA_NGC_API_KEY=${NVIDIA_NGC_API_KEY}
UNITY_API_KEY=${UNITY_API_KEY}
GEMINI_API_KEY=${GEMINI_API_KEY}
HOSTINGER_API_KEY=${HOSTINGER_API_KEY}
EOL

# Comprimir archivos
echo "Comprimiendo archivos..."
tar -czf deploy.tar.gz -C $TEMP_DIR .

# Copiar al servidor
echo "Copiando al servidor..."
scp -P $HOSTINGER_PORT deploy.tar.gz $HOSTINGER_USER@$HOSTINGER_HOST:~

# Ejecutar comandos en el servidor
echo "Ejecutando despliegue en el servidor..."
ssh -p $HOSTINGER_PORT $HOSTINGER_USER@$HOSTINGER_HOST << 'ENDSSH'
    # Detener contenedores existentes
    docker-compose down

    # Extraer archivos
    tar -xzf deploy.tar.gz

    # Construir y levantar contenedores
    docker-compose up -d --build

    # Limpiar archivos temporales
    rm -rf deploy.tar.gz temp_deploy
ENDSSH

# Limpiar archivos locales
echo "Limpiando archivos temporales..."
rm -rf $TEMP_DIR deploy.tar.gz

echo -e "${GREEN}Despliegue completado exitosamente${NC}" 