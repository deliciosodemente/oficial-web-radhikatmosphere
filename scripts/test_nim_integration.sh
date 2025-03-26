#!/bin/bash

# Colores para los mensajes
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}Iniciando pruebas de integración con NIM...${NC}"

# Verificar que la variable de entorno está configurada
if [ -z "$NVIDIA_NGC_API_KEY" ]; then
    echo -e "${RED}Error: NVIDIA_NGC_API_KEY no está configurada${NC}"
    exit 1
fi

# Crear directorio temporal si no existe
mkdir -p temp

# Crear un PDF de prueba
echo "Este es un documento de prueba para la conversión a podcast." > temp/test.txt
pandoc temp/test.txt -o temp/test.pdf

# Probar la conversión de PDF a podcast
echo -e "${GREEN}Probando conversión de PDF a podcast...${NC}"
curl -X POST \
  -H "Authorization: Bearer $NVIDIA_NGC_API_KEY" \
  -F "file=@temp/test.pdf" \
  -F "voice_id=default" \
  -F "speaking_rate=1.0" \
  -F "pitch=1.0" \
  http://localhost:8000/api/pdf-to-podcast/convert

# Probar obtención de voces disponibles
echo -e "\n${GREEN}Probando obtención de voces disponibles...${NC}"
curl -H "Authorization: Bearer $NVIDIA_NGC_API_KEY" \
  http://localhost:8000/api/pdf-to-podcast/voices

# Probar obtención de historial
echo -e "\n${GREEN}Probando obtención de historial...${NC}"
curl -H "Authorization: Bearer $NVIDIA_NGC_API_KEY" \
  http://localhost:8000/api/pdf-to-podcast/history

# Limpiar archivos temporales
rm -f temp/test.txt temp/test.pdf

echo -e "\n${GREEN}Pruebas completadas${NC}" 