# Plataforma Integral Omniverse

Plataforma integral que combina Unity, DaVinci Resolve y NVIDIA NGC/NIM para crear experiencias interactivas y contenido multimedia avanzado.

## Integración con S3 Bucket de NVIDIA Omniverse

Este proyecto incluye integración con el bucket S3 de NVIDIA Omniverse ubicado en:
`s3://radhikatmosphere--use1-az6--x-s3/.nvidia-omniverse/`

### Configuración de S3

Para configurar la integración con S3, sigue estos pasos:

1. Asegúrate de tener las credenciales de AWS configuradas en el archivo `.env`:

```
AWS_ACCESS_KEY_ID=TU_ACCESS_KEY_REAL_AQUI
AWS_SECRET_ACCESS_KEY=TU_SECRET_KEY_REAL_AQUI
AWS_REGION=us-east-1
```

2. Instala las dependencias del proyecto:

```bash
npm install
```

### Sincronización con S3

El proyecto incluye varios comandos para sincronizar archivos con el bucket S3:

- **Sincronización bidireccional**:
  ```bash
  npm run sync:s3:bidirectional
  ```

- **Subir archivos a S3**:
  ```bash
  npm run sync:s3:upload
  ```

- **Descargar archivos de S3**:
  ```bash
  npm run sync:s3:download
  ```

- **Sincronización personalizada**:
  ```bash
  node scripts/sync-s3.js [directorio_local] [modo_sincronización]
  ```
  Donde `modo_sincronización` puede ser: `upload`, `download` o `bidirectional`.

### API REST para S3

El servidor incluye endpoints para interactuar con el bucket S3:

- **Listar archivos**:
  ```
  GET /api/s3/list
  ```

- **Descargar archivo**:
  ```
  GET /api/s3/download/:ruta_archivo
  ```

- **Subir archivo**:
  ```
  POST /api/s3/upload?key=ruta_archivo
  ```

- **Sincronizar directorio**:
  ```
  POST /api/s3/sync
  ```
  Con body: `{ "localDir": "directorio_local", "s3Prefix": "prefijo_s3" }`

## Características Principales

- **Frontend Interactivo**: Desarrollado en Unity (WebGL) para experiencias inmersivas
- **Backend Orquestador**: FastAPI para centralizar llamadas a servicios
- **Integración con DaVinci Resolve**: Automatización de edición de video
- **NVIDIA NGC/NIM**: Inferencia de modelos AI con aceleración GPU
- **AWS Integration**: Despliegue automático en EC2, almacenamiento S3 y funciones Lambda
- **NVIDIA Omniverse**: Renderizado distribuido y gestión de assets 3D

## Requisitos del Sistema

- Python 3.9+
- Node.js 14+
- NVIDIA GPU compatible con CUDA 11.8+
- DaVinci Resolve Studio
- Unity 2022.3+
- Docker y Docker Compose
- Kubernetes (opcional para despliegue)
- AWS CLI configurado con permisos IAM
- NVIDIA Cloud Gateway para NGC/NIM
- Omniverse Cache Manager 2023.1+

## Estructura del Proyecto

```
/project-root
  /frontend
    ├── UnityProject/         # Proyecto Unity (WebGL)
    └── assets/              # Recursos multimedia
    
  /backend
    ├── main.py              # Servidor FastAPI
    ├── /routes             # Rutas de la API
    │      └── pdf_to_podcast.py
    ├── /services           # Servicios de integración
    │      ├── davinci_service.py
    │      ├── unity_service.py
    │      ├── nvidia_ngc_service.py
    │      ├── nim_service.py
    │      ├── gemini_service.py
    │      └── hostinger_service.py
    ├── /config
    │      └── .env          # Variables de entorno
    └── /utils
           └── cost_management.py

  /infrastructure
    ├── Dockerfile
    └── /kubernetes
         ├── deployment.yaml
         ├── service.yaml
         └── ingress.yaml
```

## Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/tu-usuario/omniverse-platform.git
cd omniverse-platform
```

2. Configurar variables de entorno:
```bash
cp backend/config/.env.example backend/config/.env
# Editar .env con tus credenciales
```

3. Instalar dependencias:
```bash
# Backend
pip install -r requirements.txt

# Frontend
npm install
```

## Desarrollo

1. Iniciar el backend:
```bash
python backend/main.py
```

2. Iniciar el frontend en modo desarrollo:
```bash
npm run start:dev
```

## Despliegue

### Con Docker:
```bash
docker-compose up -d
```

### En Kubernetes:
```bash
kubectl apply -f infrastructure/kubernetes/
```

## API Endpoints

- `POST /video/edit`: Edición automatizada de video
- `POST /unity/update`: Actualización de experiencias Unity
- `POST /ai/inference`: Inferencia de modelos AI
- `POST /text/generate`: Generación de texto con Gemini
- `GET /hosting/status`: Estado del hosting

## Monitoreo y Costes

- Monitoreo de recursos GPU
- Optimización automática de costes
- Métricas de rendimiento en tiempo real

## Contribuir

1. Fork el repositorio
2. Crear una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Crear un Pull Request

## Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.