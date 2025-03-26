# Script para configurar la integración con GitHub
# Autor: Ben10

# Colores para mensajes
function Write-Green($text) { Write-Host $text -ForegroundColor Green }
function Write-Yellow($text) { Write-Host $text -ForegroundColor Yellow }
function Write-Red($text) { Write-Host $text -ForegroundColor Red }
function Write-Cyan($text) { Write-Host $text -ForegroundColor Cyan }
function Write-Magenta($text) { Write-Host $text -ForegroundColor Magenta }

# Mostrar encabezado
Clear-Host
Write-Magenta "===== CONFIGURACIÓN DE GITHUB PARA DESPLIEGUE AUTOMÁTICO ====="
Write-Host ""

# Verificar si Git está instalado
try {
    $gitVersion = git --version
    Write-Green "Git detectado: $gitVersion"
} catch {
    Write-Red "Error: Git no está instalado o no está en el PATH"
    Write-Yellow "Por favor, descarga e instala Git desde https://git-scm.com/downloads"
    exit 1
}

# Verificar si el directorio actual es un repositorio Git
if (-not (Test-Path ".git")) {
    Write-Yellow "No se detectó un repositorio Git en el directorio actual."
    $inicializar = Read-Host "¿Deseas inicializar un repositorio Git? (S/N)"
    
    if ($inicializar -eq "S" -or $inicializar -eq "s") {
        git init
        Write-Green "Repositorio Git inicializado correctamente"
    } else {
        Write-Red "No se puede continuar sin un repositorio Git"
        exit 1
    }
}

# Obtener URL del repositorio remoto si existe
$remoteUrl = git remote get-url origin 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Yellow "No se encontró un repositorio remoto configurado."
    $githubRepo = Read-Host "Por favor, introduce la URL de tu repositorio en GitHub (ej: https://github.com/usuario/repo.git)"
    
    if ($githubRepo) {
        git remote add origin $githubRepo
        Write-Green "Repositorio remoto configurado: $githubRepo"
    } else {
        Write-Red "No se proporcionó una URL de repositorio válida"
        exit 1
    }
} else {
    Write-Green "Repositorio remoto ya configurado: $remoteUrl"
}

# Verificar y crear estructura de directorios para GitHub Actions
$workflowsDir = ".github/workflows"
if (-not (Test-Path $workflowsDir)) {
    New-Item -ItemType Directory -Path $workflowsDir -Force | Out-Null
    Write-Cyan "Directorio para flujos de trabajo de GitHub creado: $workflowsDir"
}

# Verificar si el archivo de workflow ya existe
$workflowFile = "$workflowsDir/deploy.yml"
if (Test-Path $workflowFile) {
    Write-Yellow "El archivo de configuración de GitHub Actions ya existe: $workflowFile"
    $sobrescribir = Read-Host "¿Deseas sobrescribirlo? (S/N)"
    
    if ($sobrescribir -ne "S" -and $sobrescribir -ne "s") {
        Write-Cyan "Se mantendrá la configuración existente"
    }
}

# Mostrar información de secretos requeridos
Write-Cyan "`nPara completar la configuración, necesitarás añadir los siguientes secretos en GitHub:"
Write-Host "1. HOSTINGER_SERVER: 82.29.157.155"
Write-Host "2. HOSTINGER_USERNAME: u547715306"
Write-Host "3. HOSTINGER_PASSWORD: (tu contraseña de Hostinger)"
Write-Host "4. HOSTINGER_PORT: 65002"

Write-Host "`nPara añadir estos secretos:"
Write-Host "1. Ve a tu repositorio en GitHub"
Write-Host "2. Navega a Settings > Secrets and variables > Actions"
Write-Host "3. Haz clic en 'New repository secret' y añade cada uno de los secretos anteriores"

# Opciones para finalizar
Write-Host "`n¿Qué deseas hacer ahora?"
Write-Host "1. Abrir GitHub en el navegador"
Write-Host "2. Hacer commit y push de los cambios actuales"
Write-Host "3. Salir"

$opcion = Read-Host "`nSelecciona una opción (1-3)"

switch ($opcion) {
    "1" {
        Start-Process "https://github.com"
        Write-Green "Navegador abierto. Inicia sesión en GitHub para continuar la configuración."
    }
    "2" {
        $commitMessage = Read-Host "Introduce un mensaje para el commit"
        if (-not $commitMessage) {
            $commitMessage = "Configuración inicial para despliegue automático a Hostinger"
        }
        
        git add .
        git commit -m $commitMessage
        git push -u origin main
        
        Write-Green "Cambios enviados a GitHub correctamente"
    }
    "3" {
        Write-Cyan "Configuración finalizada. Recuerda configurar los secretos en GitHub."
    }
    default {
        Write-Red "Opción no válida"
    }
}

Write-Host "`nPresiona cualquier tecla para salir..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") 