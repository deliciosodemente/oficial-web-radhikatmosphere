/**
 * Script para verificar la conexión con AWS S3
 * Este script prueba las credenciales de AWS configuradas en el archivo .env
 */

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

/**
 * Función para probar la conexión con AWS S3
 */
async function testConnection() {
  console.log('Configuración actual:');
  console.log(`- AWS_ACCESS_KEY_ID: ${process.env.AWS_ACCESS_KEY_ID.substring(0, 5)}...`);
  console.log(`- AWS_SECRET_ACCESS_KEY: ${process.env.AWS_SECRET_ACCESS_KEY.substring(0, 5)}...`);
  console.log(`- AWS_REGION: ${process.env.AWS_REGION}`);
  console.log(`- S3_BUCKET: ${S3_BUCKET}`);
  console.log('\nIntentando conectar a AWS S3...');
  
  try {
    // Intentar listar objetos en el bucket
    const params = {
      Bucket: S3_BUCKET,
      Prefix: S3_PREFIX,
      MaxKeys: 5
    };
    
    const data = await s3.listObjectsV2(params).promise();
    
    console.log('✅ Conexión exitosa a AWS S3');
    console.log(`Encontrados ${data.Contents ? data.Contents.length : 0} objetos en el bucket`);
    
    if (data.Contents && data.Contents.length > 0) {
      console.log('\nPrimeros objetos:');
      data.Contents.slice(0, 3).forEach(item => {
        console.log(` - ${item.Key} (${item.Size} bytes)`);
      });
    }
    
    return true;
  } catch (error) {
    console.error('❌ Error al conectar con AWS S3:', error.message);
    console.error('Por favor, verifica tus credenciales en el archivo .env');
    return false;
  }
}

// Ejecutar la prueba
testConnection()
  .then(() => console.log('\nPrueba completada.'))
  .catch(err => console.error('Error en la prueba:', err));