# Plataforma Integral Omniverse

Plataforma integral que combina Unity, DaVinci Resolve, NVIDIA NGC/NIM y Hostinger para crear experiencias interactivas y contenido multimedia avanzado.

## Características Principales

- **Frontend Interactivo**: Desarrollado en Unity (WebGL) para experiencias inmersivas
- **Backend Orquestador**: FastAPI para centralizar llamadas a servicios
- **Integración con DaVinci Resolve**: Automatización de edición de video
- **NVIDIA NGC/NIM**: Inferencia de modelos AI con aceleración GPU
- **Integración con Hostinger**: Gestión de hosting y optimización de costes

## Requisitos del Sistema

- Python 3.9+
- Node.js 14+
- NVIDIA GPU compatible con CUDA 11.8+
- DaVinci Resolve Studio
- Unity 2022.3+
- Docker y Docker Compose
- Kubernetes (opcional para despliegue)

## Estructura del Proyecto

```
/project-root
  /frontend
    ├── UnityProject/         # Proyecto Unity (WebGL)
    └── assets/              # Recursos multimedia
    
  /backend
    ├── main.py              # Servidor FastAPI
    ├── /services           # Servicios de integración
    │      ├── davinci_service.py
    │      ├── unity_service.py
    │      ├── nvidia_ngc_service.py
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