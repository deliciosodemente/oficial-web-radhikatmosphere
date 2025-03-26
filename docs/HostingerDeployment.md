# Guía de Despliegue a Hostinger

Este documento contiene instrucciones detalladas para desplegar correctamente el menú 3D inmersivo en el servidor de Hostinger para el dominio `new.radhikatmosphere.com`.

## Índice

1. [Requisitos Previos](#requisitos-previos)
2. [Configuración Inicial](#configuración-inicial)
3. [Despliegue del Menú](#despliegue-del-menú)
   - [Usando el Script de PowerShell (Windows)](#usando-el-script-de-powershell-windows)
   - [Usando el Script de Python (Multiplataforma)](#usando-el-script-de-python-multiplataforma)
   - [Despliegue Manual](#despliegue-manual)
4. [Verificación del Despliegue](#verificación-del-despliegue)
5. [Resolución de Problemas](#resolución-de-problemas)
6. [Actualización del Menú](#actualización-del-menú)
7. [Referencias y Recursos Adicionales](#referencias-y-recursos-adicionales)

## Requisitos Previos

Antes de comenzar el despliegue, asegúrate de tener:

- **Credenciales de Hostinger**:
  - Usuario: `u547715306`
  - Contraseña: (Solicita al administrador)
  - Host: `82.29.157.155`
  - Puerto SSH: `65002`

- **Herramientas necesarias**:
  - **Para Windows**: PowerShell y WinSCP
  - **Para todas las plataformas**: Python 3.6+ con las librerías paramiko y tqdm
  - Node.js y npm para compilar el proyecto

- **Código fuente del menú 3D inmersivo**:
  - Asegúrate de tener la versión más reciente desde el repositorio Git
  - Verifica que la configuración apunta a `new.radhikatmosphere.com`

## Configuración Inicial

1. **Configurar el archivo `.env`** en la raíz del proyecto:

   ```
   HOSTINGER_HOST=82.29.157.155
   HOSTINGER_USER=u547715306
   HOSTINGER_PORT=65002
   HOSTINGER_KEY_PATH=~/.ssh/hostinger_key
   HOSTINGER_REMOTE_DIR=/home/u547715306/domains/new.radhikatmosphere.com/public_html/immersive-menu
   LOCAL_MENU_DIR=./build
   ```

2. **Generar una clave SSH** (opcional pero recomendado):

   ```bash
   # En Windows (PowerShell):
   ssh-keygen -t rsa -b 4096 -f "$env:USERPROFILE\.ssh\hostinger_key" -C "despliegue_menu_inmersivo"

   # En Linux/Mac:
   ssh-keygen -t rsa -b 4096 -f ~/.ssh/hostinger_key -C "despliegue_menu_inmersivo"
   ```

3. **Configurar la clave en Hostinger**:

   - Copia el contenido de `~/.ssh/hostinger_key.pub`
   - Accede al panel de control de Hostinger
   - Ve a "Avanzado" > "Acceso SSH" > "Claves SSH"
   - Agrega la clave pública

4. **Compilar el menú 3D inmersivo**:

   ```bash
   npm install
   npm run build
   ```

## Despliegue del Menú

### Usando el Script de PowerShell (Windows)

Este método es el más recomendado para usuarios de Windows:

1. Abre PowerShell como administrador
2. Ejecuta:

   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
   cd /ruta/a/tu/proyecto
   .\scripts\deploy_menu.ps1
   ```

3. Sigue las instrucciones en pantalla

### Usando el Script de Python (Multiplataforma)

Este método funciona en Windows, Linux y Mac:

1. Instala las dependencias necesarias:

   ```bash
   pip install paramiko tqdm python-dotenv
   ```

2. Ejecuta el script de despliegue:

   ```bash
   python scripts/deploy_menu.py
   ```

   Opciones disponibles:
   - `--force` o `-f`: Fuerza la subida de todos los archivos
   - `--build` o `-b`: Recompila el menú antes de desplegar
   - `--password` o `-p`: Especifica la contraseña SSH (no recomendado)

### Despliegue Manual

Si prefieres hacer el despliegue manualmente:

1. **Con WinSCP (Windows)**:
   - Instala WinSCP desde [https://winscp.net](https://winscp.net)
   - Conéctate usando los siguientes parámetros:
     - Protocolo: SFTP
     - Host: 82.29.157.155
     - Puerto: 65002
     - Usuario: u547715306
     - Contraseña: (la proporcionada por el administrador)
     - Clave privada: ~/.ssh/hostinger_key (opcional)
   - Copia los archivos de la carpeta `build/` a `/home/u547715306/domains/new.radhikatmosphere.com/public_html/immersive-menu/`

2. **Con FileZilla (Multiplataforma)**:
   - Instala FileZilla desde [https://filezilla-project.org](https://filezilla-project.org)
   - Conéctate usando SFTP con los mismos parámetros anteriores
   - Copia los archivos de manera similar

3. **Con comandos SSH (Avanzado)**:
   ```bash
   # Conectar al servidor
   ssh -i ~/.ssh/hostinger_key -p 65002 u547715306@82.29.157.155

   # Crear directorio si no existe
   mkdir -p /home/u547715306/domains/new.radhikatmosphere.com/public_html/immersive-menu

   # Salir del servidor
   exit

   # Copiar archivos usando scp
   scp -i ~/.ssh/hostinger_key -P 65002 -r ./build/* u547715306@82.29.157.155:/home/u547715306/domains/new.radhikatmosphere.com/public_html/immersive-menu/
   ```

## Verificación del Despliegue

1. **Accede al menú en el navegador**:
   [https://new.radhikatmosphere.com/immersive-menu/](https://new.radhikatmosphere.com/immersive-menu/)

2. **Ejecuta el script de verificación**:
   [https://new.radhikatmosphere.com/immersive-menu/verify.php](https://new.radhikatmosphere.com/immersive-menu/verify.php)

3. **Prueba la funcionalidad**:
   - Verifica que todos los botones dirigen a las páginas correctas
   - Comprueba que la interfaz 3D carga correctamente
   - Confirma que la conexión con el sitio principal funciona

## Resolución de Problemas

### Problema 1: Error de conexión SSH

**Síntomas**:
- "Connection refused" o "Authentication failed"

**Soluciones**:
1. Verifica que la dirección IP y puerto son correctos
2. Asegúrate de que la contraseña es correcta
3. Si usas clave SSH, verifica que:
   - Los permisos de la clave son correctos (600)
   - La clave pública está registrada en Hostinger
   - La ruta a la clave privada es correcta

```bash
# Corregir permisos de clave
chmod 600 ~/.ssh/hostinger_key
```

4. Ejecuta el script de diagnóstico:

```bash
powershell.exe -ExecutionPolicy Bypass -File scripts/fix_hostinger_connection.ps1
```

### Problema 2: Archivos no visibles después del despliegue

**Síntomas**:
- El sitio muestra "Not Found" o una página en blanco
- No se pueden ver los archivos subidos

**Soluciones**:
1. Verifica que la ruta de despliegue es correcta
2. Comprueba los permisos de los archivos:

```bash
ssh -i ~/.ssh/hostinger_key -p 65002 u547715306@82.29.157.155 "chmod -R 755 /home/u547715306/domains/new.radhikatmosphere.com/public_html/immersive-menu"
```

3. Asegúrate de que existe un archivo `index.html` en el directorio

### Problema 3: El menú no se conecta al sitio principal

**Síntomas**:
- El indicador de conexión muestra "Sin conexión"
- Los enlaces no funcionan correctamente

**Soluciones**:
1. Verifica que el sitio principal está en línea
2. Comprueba que la configuración del menú apunta a las URLs correctas:
   - Edita `src/components/ImmersiveMenu.js`
   - Asegúrate de que todas las URLs contienen `new.radhikatmosphere.com`
3. Revisa las políticas CORS del servidor principal

### Problema 4: WinSCP no está instalado

**Síntomas**:
- El script de PowerShell falla al cargar WinSCP

**Soluciones**:
1. Descarga e instala WinSCP desde [https://winscp.net](https://winscp.net)
2. Asegúrate de que está instalado en la ubicación estándar
3. Alternativamente, usa el método de despliegue con Python

### Problema 5: Errores de compilación

**Síntomas**:
- `npm run build` falla
- La carpeta `build` no se genera correctamente

**Soluciones**:
1. Asegúrate de que todas las dependencias están instaladas:
```bash
npm install
```

2. Verifica que tienes una versión compatible de Node.js (v14+)
3. Comprueba los errores específicos en la consola y resuelve problemas de código

## Actualización del Menú

Para actualizar el menú a una nueva versión:

1. **Actualiza el código fuente**:
   ```bash
   git pull origin main
   ```

2. **Implementa los cambios necesarios** para `new.radhikatmosphere.com`

3. **Recompila el proyecto**:
   ```bash
   npm run build
   ```

4. **Despliega la nueva versión** usando cualquiera de los métodos anteriores

5. **Verifica la actualización** comprobando la nueva versión en:
   [https://new.radhikatmosphere.com/immersive-menu/](https://new.radhikatmosphere.com/immersive-menu/)

## Referencias y Recursos Adicionales

- [Documentación del Menú 3D Inmersivo](./ImmersiveMenu.md)
- [Documentación de Hostinger](https://www.hostinger.es/tutoriales/como-usar-ssh)
- [WinSCP - Cliente SFTP para Windows](https://winscp.net)
- [Paramiko - Biblioteca SSH para Python](http://www.paramiko.org/)

## Despliegue Automático con GitHub Actions

Esta sección explica cómo utilizar GitHub Actions para automatizar el despliegue del Menú 3D Inmersivo a Hostinger.

### Configuración de GitHub

1. **Crea un repositorio en GitHub** para el proyecto (si aún no lo has hecho)
2. **Clona el repositorio** a tu máquina local:
   ```bash
   git clone https://github.com/tu-usuario/tu-repo.git
   cd tu-repo
   ```

3. **Ejecuta el script de configuración** para preparar el entorno:
   ```powershell
   .\scripts\setup_github.ps1
   ```
   Este script verificará tu configuración de Git, creará la estructura necesaria para GitHub Actions, y te guiará para configurar los secretos necesarios.

### Archivos de Configuración

El despliegue automático utiliza un archivo de flujo de trabajo ubicado en `.github/workflows/deploy.yml`. Este archivo define los pasos que se ejecutan cada vez que hay un push al repositorio:

1. Checkout del código desde GitHub
2. Configuración de Node.js
3. Instalación de dependencias
4. Compilación del proyecto
5. Despliegue a Hostinger

### Secretos Requeridos

Para que el despliegue funcione, debes configurar los siguientes secretos en tu repositorio de GitHub:

- **HOSTINGER_SERVER**: 82.29.157.155
- **HOSTINGER_USERNAME**: u547715306
- **HOSTINGER_PASSWORD**: Tu contraseña de Hostinger
- **HOSTINGER_PORT**: 65002

### Uso del Despliegue Automático

Una vez configurado, el despliegue se realizará automáticamente cada vez que hagas push a la rama principal del repositorio:

1. Realiza cambios en el código
2. Haz commit de los cambios:
   ```bash
   git add .
   git commit -m "Descripción de los cambios"
   ```
3. Sube los cambios a GitHub:
   ```bash
   git push origin main
   ```
4. GitHub Actions ejecutará automáticamente el flujo de trabajo y desplegará los cambios en Hostinger
5. Puedes verificar el estado del despliegue en la pestaña "Actions" de tu repositorio en GitHub

### Solución de Problemas

Si el despliegue automático falla, puedes verificar los logs en GitHub:

1. Ve a tu repositorio en GitHub
2. Haz clic en la pestaña "Actions"
3. Selecciona el workflow "Deploy to Hostinger" más reciente
4. Revisa los logs para identificar el problema

Problemas comunes incluyen credenciales incorrectas, problemas de permisos en el servidor o errores en la compilación del proyecto.

---

Para asistencia adicional, contacta con el equipo de desarrollo enviando un correo a support@radhikatmosphere.com o abriendo un ticket en el sistema de soporte.

**Última actualización**: Junio 2023 