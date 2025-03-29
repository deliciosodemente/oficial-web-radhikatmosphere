/**
 * Script para sincronizar archivos con el bucket S3 de NVIDIA Omniverse
 * Bucket: s3://radhikatmosphere--use1-az6--x-s3/.nvidia-omniverse/
 */

const AWS = require('aws-sdk');
const fs = require('fs');
const path = require('path');
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

// Directorios para sincronización
const LOCAL_DIR = process.argv[2] || path.join(__dirname, '..', 'build');
const SYNC_MODE = process.argv[3] || 'upload'; // 'upload', 'download', 'bidirectional'

/**
 * Función para obtener el tipo de contenido basado en la extensión del archivo
 */
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
    '.svg': 'image/svg+xml',
    '.usd': 'model/vnd.usd',
    '.usda': 'model/vnd.usd+ascii',
    '.usdz': 'model/vnd.usd+zip',
    '.gltf': 'model/gltf+json',
    '.glb': 'model/gltf-binary'
  };
  
  return contentTypes[ext] || 'application/octet-stream';
};

/**
 * Función para subir un archivo a S3
 */
const uploadFile = async (localPath, relativePath) => {
  try {
    const fileContent = fs.readFileSync(localPath);
    const key = S3_PREFIX + relativePath.replace(/\\/g, '/');
    
    const params = {
      Bucket: S3_BUCKET,
      Key: key,
      Body: fileContent,
      ContentType: getContentType(localPath)
    };
    
    await s3.putObject(params).promise();
    console.log(`✅ Subido: ${relativePath} -> s3://${S3_BUCKET}/${key}`);
    return key;
  } catch (error) {
    console.error(`❌ Error al subir ${localPath}:`, error.message);
    throw error;
  }
};

/**
 * Función para descargar un archivo de S3
 */
const downloadFile = async (s3Key, localPath) => {
  try {
    const params = {
      Bucket: S3_BUCKET,
      Key: s3Key
    };
    
    const data = await s3.getObject(params).promise();
    
    // Asegurar que el directorio existe
    const dir = path.dirname(localPath);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
    
    fs.writeFileSync(localPath, data.Body);
    console.log(`✅ Descargado: s3://${S3_BUCKET}/${s3Key} -> ${localPath}`);
    return localPath;
  } catch (error) {
    console.error(`❌ Error al descargar ${s3Key}:`, error.message);
    throw error;
  }
};

/**
 * Función recursiva para procesar directorios locales (subida)
 */
const processLocalDirectory = async (dir, baseDir) => {
  const files = fs.readdirSync(dir);
  const uploadPromises = [];
  
  for (const file of files) {
    const filePath = path.join(dir, file);
    const stat = fs.statSync(filePath);
    
    if (stat.isDirectory()) {
      // Procesar subdirectorio recursivamente
      const subDirPromises = await processLocalDirectory(filePath, baseDir);
      uploadPromises.push(...subDirPromises);
    } else {
      // Subir archivo a S3
      const relativePath = path.relative(baseDir, filePath);
      uploadPromises.push(uploadFile(filePath, relativePath));
    }
  }
  
  return uploadPromises;
};

/**
 * Función para listar objetos en S3
 */
const listS3Objects = async () => {
  try {
    const params = {
      Bucket: S3_BUCKET,
      Prefix: S3_PREFIX
    };
    
    const data = await s3.listObjectsV2(params).promise();
    return data.Contents || [];
  } catch (error) {
    console.error('Error al listar objetos de S3:', error.message);
    throw error;
  }
};

/**
 * Función para sincronizar desde S3 a local (descarga)
 */
const syncFromS3 = async () => {
  try {
    const s3Objects = await listS3Objects();
    console.log(`Encontrados ${s3Objects.length} objetos en S3`);
    
    const downloadPromises = [];
    
    for (const obj of s3Objects) {
      // Ignorar el prefijo como directorio
      if (obj.Key.endsWith('/')) continue;
      
      // Obtener la ruta relativa eliminando el prefijo
      const relativePath = obj.Key.substring(S3_PREFIX.length);
      const localPath = path.join(LOCAL_DIR, relativePath);
      
      downloadPromises.push(downloadFile(obj.Key, localPath));
    }
    
    await Promise.all(downloadPromises);
    console.log(`✅ Sincronización completada: ${downloadPromises.length} archivos descargados`);
  } catch (error) {
    console.error('Error en la sincronización desde S3:', error.message);
  }
};

/**
 * Función para sincronizar desde local a S3 (subida)
 */
const syncToS3 = async () => {
  try {
    console.log(`Sincronizando desde ${LOCAL_DIR} a s3://${S3_BUCKET}/${S3_PREFIX}`);
    
    // Verificar que el directorio local existe
    if (!fs.existsSync(LOCAL_DIR)) {
      console.error(`❌ El directorio local ${LOCAL_DIR} no existe`);
      return;
    }
    
    const uploadPromises = await processLocalDirectory(LOCAL_DIR, LOCAL_DIR);
    await Promise.all(uploadPromises);
    
    console.log(`✅ Sincronización completada: ${uploadPromises.length} archivos subidos`);
  } catch (error) {
    console.error('Error en la sincronización a S3:', error.message);
  }
};

/**
 * Función para sincronización bidireccional
 */
const syncBidirectional = async () => {
  try {
    // Primero descargamos de S3 a local
    await syncFromS3();
    
    // Luego subimos de local a S3
    await syncToS3();
    
    console.log('✅ Sincronización bidireccional completada');
  } catch (error) {
    console.error('Error en la sincronización bidireccional:', error.message);
  }
};

// Ejecutar la sincronización según el modo especificado
const runSync = async () => {
  console.log(`Modo de sincronización: ${SYNC_MODE}`);
  
  switch (SYNC_MODE.toLowerCase()) {
    case 'download':
      await syncFromS3();
      break;
    case 'upload':
      await syncToS3();
      break;
    case 'bidirectional':
      await syncBidirectional();
      break;
    default:
      console.error(`❌ Modo de sincronización no válido: ${SYNC_MODE}`);
      console.log('Modos válidos: upload, download, bidirectional');
  }
};

// Iniciar sincronización
runSync().catch(error => {
  console.error('Error en la sincronización:', error);
  process.exit(1);
});