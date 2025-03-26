# Usar una imagen base con soporte para GPU
FROM nvidia/cuda:11.8.0-runtime-ubuntu22.04

# Establecer variables de entorno
ENV PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    python3.9 \
    python3-pip \
    nodejs \
    npm \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo
WORKDIR /app

# Copiar archivos de requisitos
COPY requirements.txt .
COPY package.json .
COPY package-lock.json .

# Instalar dependencias de Python y Node.js
RUN pip3 install --no-cache-dir -r requirements.txt
RUN npm install

# Copiar el código fuente
COPY . .

# Exponer puertos
EXPOSE 8000
EXPOSE 3000

# Script de inicio
CMD ["./scripts/start.sh"] 