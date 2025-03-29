/**
 * Servidor Node.js para Radhikatmosphere
 * Configurado para ejecutarse en Amazon Lightsail
 * IP: 52.86.51.202
 * Integración con S3 bucket: s3://radhikatmosphere--use1-az6--x-s3/.nvidia-omniverse/
 */

const express = require('express');
const path = require('path');
const fs = require('fs');
const morgan = require('morgan');
const compression = require('compression');
const helmet = require('helmet');
const AWS = require('aws-sdk');
const dotenv = require('dotenv');

// Cargar variables de entorno
dotenv.config();

// Configuración de AWS S3
AWS.config.update({
  accessKeyId: process.env.AWS_ACCESS_KEY_ID,
  secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY,
  region: process.env.AWS_REGION || 'us-east-1'
});

// Inicializar cliente S3
const s3 = new AWS.S3();
const S3_BUCKET = 'radhikatmosphere--use1-az6--x-s3';
const S3_PREFIX = '.nvidia-omniverse/';

// Inicializar aplicación Express
const app = express();
const PORT = process.env.PORT || 3000;

// Middleware de seguridad y optimización
app.use(helmet({
  contentSecurityPolicy: false, // Deshabilitar CSP para permitir recursos externos
}));
app.use(compression()); // Comprimir respuestas
app.use(morgan('combined')); // Logging

// Servir archivos estáticos desde la carpeta build
app.use(express.static(path.join(__dirname, 'build')));

// API endpoints
app.get('/api/health', (req, res) => {
  res.json({ status: 'ok', server: 'Amazon Lightsail', ip: '52.86.51.202' });
});

// Endpoint para listar archivos del bucket S3
app.get('/api/s3/list', async (req, res) => {
  try {
    const params = {
      Bucket: S3_BUCKET,
      Prefix: S3_PREFIX
    };
    
    const data = await s3.listObjectsV2(params).promise();
    res.json({
      success: true,
      files: data.Contents.map(item => ({
        key: item.Key,
        size: item.Size,
        lastModified: item.LastModified
      }))
    });
  } catch (error) {
    console.error('Error al listar archivos de S3:', error);
    res.status(500).json({ success: false, error: error.message });
  }
});

// Endpoint para descargar un archivo del bucket S3
app.get('/api/s3/download/:key(*)', async (req, res) => {
  try {
    const key = S3_PREFIX + req.params.key;
    const params = {
      Bucket: S3_BUCKET,
      Key: key
    };
    
    const data = await s3.getObject(params).promise();
    res.setHeader('Content-Type', data.ContentType);
    res.setHeader('Content-Disposition', `attachment; filename=${path.basename(key)}`);
    res.send(data.Body);
  } catch (error) {
    console.error('Error al descargar archivo de S3:', error);
    res.status(500).json({ success: false, error: error.message });
  }
});

// Endpoint para subir un archivo al bucket S3
app.post('/api/s3/upload', express.raw({type: '*/*', limit: '50mb'}), async (req, res) => {
  try {
    if (!req.query.key) {
      return res.status(400).json({ success: false, error: 'Se requiere el parámetro key' });
    }
    
    const key = S3_PREFIX + req.query.key;
    const params = {
      Bucket: S3_BUCKET,
      Key: key,
      Body: req.body,
      ContentType: req.headers['content-type']
    };
    
    await s3.putObject(params).promise();
    res.json({ success: true, key: key });
  } catch (error) {
    console.error('Error al subir archivo a S3:', error);
    res.status(500).json({ success: false, error: error.message });
  }
});

// Endpoint para sincronizar archivos con S3
app.post('/api/s3/sync', async (req, res) => {
  try {
    const localDir = path.join(__dirname, req.body.localDir || 'build');
    const s3Prefix = req.body.s3Prefix || S3_PREFIX;
    
    // Función para subir un archivo a S3
    const uploadFile = async (localPath, relativePath) => {
      const fileContent = fs.readFileSync(localPath);
      const key = s3Prefix + relativePath.replace(/\\/g, '/');
      
      const params = {
        Bucket: S3_BUCKET,
        Key: key,
        Body: fileContent,
        ContentType: getContentType(localPath)
      };
      
      await s3.putObject(params).promise();
      return key;
    };
    
    // Función para obtener el tipo de contenido basado en la extensión del archivo
    const getContentType = (filePath) => {
      const ext = path.extname(filePath).toLowerCase();
      const contentTypes = {
        '.html': 'text/html',
        '.css': 'text/css',
        '.js': 'application/javascript',
        '.json': 'application/json',
        '.png': 'image/png',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.gif': 'image/gif',
        '.svg': 'image/svg+xml'
      };
      
      return contentTypes[ext] || 'application/octet-stream';
    };
    
    // Función recursiva para recorrer directorios
    const processDirectory = async (dir, baseDir) => {
      const files = fs.readdirSync(dir);
      const uploadPromises = [];
      
      for (const file of files) {
        const filePath = path.join(dir, file);
        const stat = fs.statSync(filePath);
        
        if (stat.isDirectory()) {
          // Procesar subdirectorio recursivamente
          await processDirectory(filePath, baseDir);
        } else {
          // Subir archivo a S3
          const relativePath = path.relative(baseDir, filePath);
          uploadPromises.push(uploadFile(filePath, relativePath));
        }
      }
      
      return Promise.all(uploadPromises);
    };
    
    // Iniciar sincronización
    const uploadedFiles = await processDirectory(localDir, localDir);
    
    res.json({
      success: true,
      message: `${uploadedFiles.length} archivos sincronizados con S3`,
      files: uploadedFiles
    });
  } catch (error) {
    console.error('Error al sincronizar con S3:', error);
    res.status(500).json({ success: false, error: error.message });
  }
});

// Ruta para todas las demás solicitudes - Servir la aplicación React
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'build', 'index.html'));
});

// Iniciar el servidor
app.listen(PORT, () => {
  console.log(`Servidor ejecutándose en http://localhost:${PORT}`);
  console.log(`Configurado para Amazon Lightsail (52.86.51.202)`);
});