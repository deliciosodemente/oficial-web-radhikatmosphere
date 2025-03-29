# Guía de Despliegue a AWS

Este documento contiene instrucciones detalladas para desplegar correctamente la aplicación en AWS para el dominio `radhikatmosphere.com`.

## Requisitos Previos

- Cuenta de AWS activa
- AWS CLI instalado y configurado
- Node.js y npm instalados
- Python 3.8+ instalado

## Configuración Inicial

### 1. Configuración de AWS

#### Crear recursos necesarios en AWS

1. **Crear un bucket S3 para el frontend**:
   - Accede a la consola de AWS y navega a S3
   - Crea un nuevo bucket (ej. `radhikatmosphere-assets`)
   - Habilita el alojamiento de sitios web estáticos
   - Configura la política de bucket para permitir acceso público

2. **Crear una distribución CloudFront**:
   - Navega a CloudFront en la consola de AWS
   - Crea una nueva distribución
   - Selecciona el bucket S3 como origen
   - Configura el comportamiento de caché según necesites

3. **Lanzar una instancia EC2 para el backend** (opcional si usas servicios serverless):
   - Navega a EC2 en la consola de AWS
   - Lanza una nueva instancia (recomendado: Amazon Linux 2 o Ubuntu)
   - Configura el grupo de seguridad para permitir tráfico HTTP/HTTPS y SSH
   - Crea o selecciona un par