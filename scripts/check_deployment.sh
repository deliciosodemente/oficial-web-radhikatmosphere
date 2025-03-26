#!/bin/bash

# Colores para mensajes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}Verificando estado del despliegue...${NC}"

# Cargar variables de entorno
if [ -f "../backend/config/.env" ]; then
    source "../backend/config/.env"
else
    echo -e "${RED}Error: No se encontró el archivo .env${NC}"
    exit 1
fi

# Verificar conexión SSH
echo -e "${YELLOW}Verificando conexión SSH con Hostinger...${NC}"
ssh -i "$HOSTINGER_SSH_KEY_PATH" -p "$HOSTINGER_SSH_PORT" "$HOSTINGER_SSH_USERNAME@$HOSTINGER_SSH_HOST" "echo 'Conexión SSH exitosa'" > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo -e "${RED}Error: No se pudo establecer conexión SSH con Hostinger${NC}"
    exit 1
fi

# Verificar frontend
echo -e "${YELLOW}Verificando frontend...${NC}"
frontend_status=$(curl -s -o /dev/null -w "%{http_code}" "https://$HOSTINGER_DOMAIN/unity")
if [ "$frontend_status" = "200" ]; then
    echo -e "${GREEN}Frontend está funcionando correctamente${NC}"
else
    echo -e "${RED}Error: Frontend no está respondiendo (código: $frontend_status)${NC}"
fi

# Verificar backend
echo -e "${YELLOW}Verificando backend...${NC}"
backend_status=$(curl -s -o /dev/null -w "%{http_code}" "https://$HOSTINGER_DOMAIN/api/health")
if [ "$backend_status" = "200" ]; then
    echo -e "${GREEN}Backend está funcionando correctamente${NC}"
else
    echo -e "${RED}Error: Backend no está respondiendo (código: $backend_status)${NC}"
fi

# Verificar SSL
echo -e "${YELLOW}Verificando certificado SSL...${NC}"
ssl_check=$(openssl s_client -connect "$HOSTINGER_DOMAIN:443" -servername "$HOSTINGER_DOMAIN" </dev/null 2>/dev/null | openssl x509 -noout -dates)
if [ $? -eq 0 ]; then
    echo -e "${GREEN}Certificado SSL válido${NC}"
    echo "$ssl_check"
else
    echo -e "${RED}Error: No se pudo verificar el certificado SSL${NC}"
fi

# Verificar espacio en disco
echo -e "${YELLOW}Verificando espacio en disco...${NC}"
disk_usage=$(ssh -i "$HOSTINGER_SSH_KEY_PATH" -p "$HOSTINGER_SSH_PORT" "$HOSTINGER_SSH_USERNAME@$HOSTINGER_SSH_HOST" "df -h /public_html")
echo "$disk_usage"

# Verificar logs
echo -e "${YELLOW}Verificando logs recientes...${NC}"
recent_logs=$(ssh -i "$HOSTINGER_SSH_KEY_PATH" -p "$HOSTINGER_SSH_PORT" "$HOSTINGER_SSH_USERNAME@$HOSTINGER_SSH_HOST" "tail -n 50 /public_html/api/logs/app.log")
echo "$recent_logs"

# Verificar servicios
echo -e "${YELLOW}Verificando servicios...${NC}"
services_status=$(ssh -i "$HOSTINGER_SSH_KEY_PATH" -p "$HOSTINGER_SSH_PORT" "$HOSTINGER_SSH_USERNAME@$HOSTINGER_SSH_HOST" "systemctl status nginx | grep Active")
echo "$services_status"

echo -e "${GREEN}Verificación completada${NC}" 