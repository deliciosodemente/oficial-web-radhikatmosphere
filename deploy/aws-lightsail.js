const AWS = require('aws-sdk');
const fs = require('fs');
const path = require('path');

// Cargar variables de entorno si existe un archivo .env
try {
    require('dotenv').config();
} catch (error) {
    console.log('dotenv no está instalado, usando variables de entorno del sistema');
}

const lightsail = new AWS.Lightsail({
    region: process.env.AWS_REGION || 'us-east-1',
    accessKeyId: process.env.AWS_ACCESS_KEY_ID,
    secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY
});

// Configuración para la instancia de Lightsail
const instanceConfig = {
    instanceName: 'radhikatmosphere-app',
    availabilityZone: 'us-east-1a', // Cambiar a tu zona preferida
    blueprintId: 'nodejs',          // Blueprint de Node.js
    bundleId: 'nano_2_0',          // Instancia más pequeña (cambiar según sea necesario)
    tags: [
        {
            key: 'Environment',
            value: 'Production'
        },
        {
            key: 'Project',
            value: 'Radhikatmosphere'
        }
    ]
};

// Configuración de DNS e IPv6
const networkConfig = {
    ipv6Addresses: [
        '2600:1f18:51b8:bc00:3c3a:4a1a:f25f:802e'
    ],
    ports: [
        { port: 80, protocol: 'tcp' },    // HTTP
        { port: 443, protocol: 'tcp' },   // HTTPS
        { port: 22, protocol: 'tcp' }     // SSH
    ]
};

async function createLightsailInstance() {
    try {
        // Crear la instancia
        const createResponse = await lightsail.createInstances({
            instanceNames: [instanceConfig.instanceName],
            availabilityZone: instanceConfig.availabilityZone,
            blueprintId: instanceConfig.blueprintId,
            bundleId: instanceConfig.bundleId,
            tags: instanceConfig.tags
        }).promise();

        console.log('Creación de instancia iniciada:', createResponse);

        // Esperar a que la instancia esté en ejecución
        await waitForInstanceRunning(instanceConfig.instanceName);

        // Crear y adjuntar IP estática
        await createAndAttachStaticIP();

        // Configurar reglas de firewall
        await configureFirewall();

        // Configurar la aplicación Node.js
        await setupNodeJsApplication();

        return createResponse;
    } catch (error) {
        console.error('Error al crear la instancia de Lightsail:', error);
        throw error;
    }
}

async function waitForInstanceRunning(instanceName) {
    console.log('Esperando a que la instancia esté en ejecución...');
    
    while (true) {
        const instance = await lightsail.getInstance({
            instanceName: instanceName
        }).promise();

        if (instance.instance.state.name === 'running') {
            console.log('La instancia está ahora en ejecución');
            break;
        }

        await new Promise(resolve => setTimeout(resolve, 5000));
    }
}

async function createAndAttachStaticIP() {
    try {
        // Crear IP estática
        const staticIpName = `${instanceConfig.instanceName}-ip`;
        await lightsail.allocateStaticIp({
            staticIpName: staticIpName
        }).promise();

        // Adjuntar IP estática a la instancia
        await lightsail.attachStaticIp({
            staticIpName: staticIpName,
            instanceName: instanceConfig.instanceName
        }).promise();

        console.log('IP estática creada y adjuntada');
    } catch (error) {
        console.error('Error al gestionar la IP estática:', error);
        throw error;
    }
}

async function configureFirewall() {
    try {
        // Configurar puertos IPv4
        for (const portConfig of networkConfig.ports) {
            await lightsail.openInstancePublicPorts({
                instanceName: instanceConfig.instanceName,
                portInfo: {
                    fromPort: portConfig.port,
                    toPort: portConfig.port,
                    protocol: portConfig.protocol
                }
            }).promise();
        }

        // Configurar direcciones IPv6
        const ipv6Cidrs = networkConfig.ipv6Addresses.map(ip => `${ip}/128`);
        for (const portConfig of networkConfig.ports) {
            await lightsail.openInstancePublicPorts({
                instanceName: instanceConfig.instanceName,
                portInfo: {
                    fromPort: portConfig.port,
                    toPort: portConfig.port,
                    protocol: portConfig.protocol,
                    cidrs: ipv6Cidrs
                }
            }).promise();
        }

        console.log('Reglas de firewall configuradas');
    } catch (error) {
        console.error('Error al configurar el firewall:', error);
        throw error;
    }
}

async function setupNodeJsApplication() {
    try {
        // Obtener información de la instancia para obtener la IP pública
        const instance = await lightsail.getInstance({
            instanceName: instanceConfig.instanceName
        }).promise();

        const publicIp = instance.instance.publicIpAddress;
        console.log(`IP pública de la instancia: ${publicIp}`);

        // Generar script de datos de usuario para la configuración de Node.js
        const userData = `#!/bin/bash
# Actualizar sistema
sudo apt-get update
sudo apt-get upgrade -y

# Instalar Node.js 16.x y npm
curl -fsSL https://deb.nodesource.com/setup_16.x | sudo -E bash -
sudo apt-get install -y nodejs

# Instalar PM2 globalmente
sudo npm install -g pm2

# Crear directorio de aplicación
mkdir -p /home/bitnami/app

# Crear una aplicación básica Express.js
cat > /home/bitnami/app/package.json << 'EOL'
{
  "name": "radhikatmosphere-app",
  "version": "1.0.0",
  "main": "app.js",
  "dependencies": {
    "express": "^4.17.1"
  }
}
EOL

# Crear app.js
cat > /home/bitnami/app/app.js << 'EOL'
const express = require('express');
const path = require('path');
const app = express();
const port = process.env.PORT || 3000;

// Servir archivos estáticos
app.use(express.static(path.join(__dirname, 'public')));

// Ruta principal
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Iniciar servidor
app.listen(port, () => {
  console.log(\`Servidor ejecutándose en el puerto \${port}\`);
});
EOL

# Crear directorio public y archivo index.html
mkdir -p /home/bitnami/app/public
cat > /home/bitnami/app/public/index.html << 'EOL'
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Radhikatmosphere</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      margin: 0;
      padding: 0;
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 100vh;
      background: linear-gradient(135deg, #6e8efb, #a777e3);
      color: white;
      text-align: center;
    }
    .container {
      max-width: 800px;
      padding: 2rem;
      background: rgba(0, 0, 0, 0.2);
      border-radius: 10px;
      box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    h1 {
      font-size: 2.5rem;
      margin-bottom: 1rem;
    }
    p {
      font-size: 1.2rem;
      margin-bottom: 2rem;
    }
    .loading-bar {
      width: 100%;
      height: 8px;
      background: rgba(255, 255, 255, 0.2);
      border-radius: 4px;
      overflow: hidden;
      position: relative;
      margin: 2rem 0;
    }
    .loading-progress {
      position: absolute;
      top: 0;
      left: 0;
      height: 100%;
      width: 30%;
      background: #ffffff;
      border-radius: 4px;
      animation: loading 1.5s infinite ease-in-out;
    }
    @keyframes loading {
      0% { left: -30%; }
      100% { left: 100%; }
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>Radhikatmosphere</h1>
    <p>Bienvenido a nuestra experiencia inmersiva. Sitio en construcción.</p>
    <div class="loading-bar">
      <div class="loading-progress"></div>
    </div>
    <p>Próximamente: Una experiencia única en un entorno inmersivo.</p>
  </div>
</body>
</html>
EOL

# Instalar dependencias
cd /home/bitnami/app
npm install

# Iniciar aplicación con PM2
pm2 start app.js
pm2 save
pm2 startup

# Configurar nginx como proxy inverso
sudo tee /opt/bitnami/nginx/conf/server_blocks/nodejs.conf << 'EOL'
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_cache_bypass \$http_upgrade;
    }
}
EOL

# Reiniciar nginx
sudo /opt/bitnami/ctlscript.sh restart nginx`;

        // Ejecutar script de datos de usuario en la instancia
        await lightsail.putInstancePublicPorts({
            instanceName: instanceConfig.instanceName,
            portInfos: networkConfig.ports
        }).promise();

        // Nota: En un escenario real, necesitaríamos usar SSH para ejecutar el script userData
        // Aquí solo mostramos el script que se ejecutaría
        console.log('Script de configuración de la aplicación Node.js generado');
        console.log('Para ejecutar el script en la instancia, conéctate por SSH y ejecútalo manualmente');

        return {
            publicIp,
            userData
        };
    } catch (error) {
        console.error('Error al configurar la aplicación Node.js:', error);
        throw error;
    }
}

// Función principal para ejecutar todo el proceso
async function main() {
    try {
        console.log('Iniciando despliegue de Radhikatmosphere en AWS Lightsail...');
        await createLightsailInstance();
        console.log('Despliegue completado con éxito!');
        
        // Obtener información de la instancia para mostrar detalles finales
        const instance = await lightsail.getInstance({
            instanceName: instanceConfig.instanceName
        }).promise();
        
        console.log('\nDetalles de la instancia:');
        console.log(`Nombre: ${instance.instance.name}`);
        console.log(`Estado: ${instance.instance.state.name}`);
        console.log(`IP pública: ${instance.instance.publicIpAddress}`);
        console.log(`IP estática: ${instance.instance.staticIpName || 'No asignada'}`);
        console.log('\nPara acceder a la aplicación, visita:');
        console.log(`http://${instance.instance.publicIpAddress}`);
    } catch (error) {
        console.error('Error en el proceso de despliegue:', error);
    }
}

// Ejecutar el script si se llama directamente
if (require.main === module) {
    main();
}

// Exportar funciones para uso en otros scripts
module.exports = {
    createLightsailInstance,
    setupNodeJsApplication,
    main
};