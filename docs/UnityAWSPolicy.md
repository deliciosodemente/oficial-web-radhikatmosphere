# Política de Unity para AWS S3

Este documento describe la política de acceso para Unity en AWS que permite la integración segura con el servicio S3.

## Descripción General

La política `unity_s3_policy.json` define los permisos necesarios para que Unity pueda compilar, desplegar y acceder a los recursos en AWS, específicamente para el almacenamiento de experiencias WebGL compiladas en buckets S3 y la invalidación de caché en CloudFront.

## Estructura de la Política

La política contiene tres declaraciones principales:

1. **UnityWebGLDeployment**: Permite a Unity desplegar builds WebGL en el bucket S3 principal.
2. **UnityCloudFrontInvalidation**: Permite a Unity crear invalidaciones en CloudFront para actualizar el contenido en caché.
3. **UnityAssetAccess**: Permite a Unity acceder a los assets almacenados en el bucket de Omniverse.

## Implementación

Para implementar esta política, sigue estos pasos:

1. Accede a la consola de AWS y navega a IAM (Identity and Access Management).
2. Selecciona "Políticas" en el menú lateral y haz clic en "Crear política".
3. Selecciona la pestaña JSON y pega el contenido del archivo `backend/config/unity_s3_policy.json`.
4. Revisa y crea la política con un nombre descriptivo como "UnityS3AccessPolicy".
5. Crea un rol de IAM para Unity y adjunta esta política al rol.

## Configuración en Unity

Para configurar Unity para usar esta política:

1. En el editor de Unity, ve a Edit > Project Settings > Services.
2. Configura las credenciales de AWS utilizando el rol IAM creado.
3. En la configuración de WebGL, especifica el bucket S3 como destino de despliegue.

## Variables de Entorno Requeridas

Asegúrate de que las siguientes variables de entorno estén configuradas en el archivo `.env`:

```
UNITY_API_KEY=tu_api_key_de_unity
AWS_ACCESS_KEY_ID=tu_access_key_id
AWS_SECRET_ACCESS_KEY=tu_secret_access_key
AWS_REGION=us-east-1
AWS_S3_BUCKET=radhikatmosphere-frontend-production
```

## Integración con el Servicio de Unity

El servicio de Unity (`unity_service.py`) ya está configurado para utilizar estas credenciales y desplegar builds WebGL en el bucket S3 configurado. La función `deploy_experience()` se encarga de subir los archivos compilados al bucket S3.

## Seguridad

Esta política sigue el principio de privilegio mínimo, otorgando solo los permisos necesarios para que Unity funcione correctamente con AWS S3. Se recomienda revisar periódicamente estos permisos y ajustarlos según sea necesario.

## Solución de Problemas

Si encuentras problemas con el despliegue de Unity a S3, verifica:

1. Que las credenciales de AWS sean válidas y estén correctamente configuradas.
2. Que el bucket S3 exista y sea accesible.
3. Que la política IAM esté correctamente adjunta al rol utilizado por Unity.
4. Los logs de Unity para mensajes de error específicos relacionados con AWS.