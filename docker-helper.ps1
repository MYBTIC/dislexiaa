# Script de ayuda para Docker - Proyecto Dislexia
# Ejecutar: .\docker-helper.ps1 [comando]

param(
    [Parameter(Position=0)]
    [string]$Command = "help"
)

function Show-Help {
    Write-Host "🐳 Docker Helper - Proyecto Dislexia" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Comandos disponibles:" -ForegroundColor Yellow
    Write-Host "  start        - Iniciar todos los servicios"
    Write-Host "  stop         - Detener todos los servicios"
    Write-Host "  restart      - Reiniciar todos los servicios"
    Write-Host "  logs         - Ver logs de todos los servicios"
    Write-Host "  logs-api     - Ver logs solo del backend"
    Write-Host "  logs-web     - Ver logs solo del frontend"
    Write-Host "  build        - Reconstruir las imágenes"
    Write-Host "  clean        - Detener y limpiar todo (incluye DB)"
    Write-Host "  migrate      - Aplicar migraciones de Django"
    Write-Host "  makemigrations - Crear nuevas migraciones"
    Write-Host "  createsuperuser - Crear superusuario de Django"
    Write-Host "  shell        - Abrir shell de Django"
    Write-Host "  test         - Ver URLs de acceso"
    Write-Host "  publish      - Publicar imagen en Docker Hub"
    Write-Host ""
    Write-Host "Ejemplos:" -ForegroundColor Green
    Write-Host "  .\docker-helper.ps1 start"
    Write-Host "  .\docker-helper.ps1 logs-api"
    Write-Host "  .\docker-helper.ps1 migrate"
}

function Start-Services {
    Write-Host "🚀 Iniciando servicios..." -ForegroundColor Green
    docker-compose up -d --build
    Write-Host ""
    Write-Host "✅ Servicios iniciados!" -ForegroundColor Green
    Write-Host ""
    Show-URLs
}

function Stop-Services {
    Write-Host "⏸️  Deteniendo servicios..." -ForegroundColor Yellow
    docker-compose down
    Write-Host "✅ Servicios detenidos!" -ForegroundColor Green
}

function Restart-Services {
    Write-Host "🔄 Reiniciando servicios..." -ForegroundColor Yellow
    docker-compose restart
    Write-Host "✅ Servicios reiniciados!" -ForegroundColor Green
}

function Show-Logs {
    Write-Host "📋 Mostrando logs (Ctrl+C para salir)..." -ForegroundColor Cyan
    docker-compose logs -f
}

function Show-APILogs {
    Write-Host "📋 Mostrando logs del backend (Ctrl+C para salir)..." -ForegroundColor Cyan
    docker-compose logs -f web
}

function Show-WebLogs {
    Write-Host "📋 Mostrando logs del frontend (Ctrl+C para salir)..." -ForegroundColor Cyan
    docker-compose logs -f frontend
}

function Build-Images {
    Write-Host "🔨 Reconstruyendo imágenes..." -ForegroundColor Yellow
    docker-compose build --no-cache
    Write-Host "✅ Imágenes reconstruidas!" -ForegroundColor Green
}

function Clean-All {
    Write-Host "🧹 Limpiando todo (esto eliminará la base de datos)..." -ForegroundColor Red
    $confirm = Read-Host "¿Estás seguro? (s/n)"
    if ($confirm -eq 's' -or $confirm -eq 'S') {
        docker-compose down -v
        Write-Host "✅ Todo limpio!" -ForegroundColor Green
    } else {
        Write-Host "❌ Operación cancelada" -ForegroundColor Yellow
    }
}

function Run-Migrate {
    Write-Host "🔄 Aplicando migraciones..." -ForegroundColor Cyan
    docker-compose exec web python manage.py migrate
    Write-Host "✅ Migraciones aplicadas!" -ForegroundColor Green
}

function Run-MakeMigrations {
    Write-Host "🔄 Creando migraciones..." -ForegroundColor Cyan
    docker-compose exec web python manage.py makemigrations
    Write-Host "✅ Migraciones creadas!" -ForegroundColor Green
}

function Create-Superuser {
    Write-Host "👤 Creando superusuario..." -ForegroundColor Cyan
    docker-compose exec web python manage.py createsuperuser
}

function Open-Shell {
    Write-Host "🐚 Abriendo shell de Django..." -ForegroundColor Cyan
    docker-compose exec web python manage.py shell
}

function Show-URLs {
    Write-Host "🌐 URLs de acceso:" -ForegroundColor Cyan
    Write-Host "  Frontend:  http://localhost:5173" -ForegroundColor Green
    Write-Host "  Backend:   http://localhost:8000" -ForegroundColor Green
    Write-Host "  Admin:     http://localhost:8000/admin" -ForegroundColor Green
    Write-Host "  API:       http://localhost:8000/api/" -ForegroundColor Green
    Write-Host "  PostgreSQL: localhost:5432" -ForegroundColor Green
}

function Publish-Image {
    Write-Host "📦 Publicando imagen en Docker Hub..." -ForegroundColor Cyan
    $username = Read-Host "Usuario de Docker Hub"

    Write-Host "Construyendo imagen..." -ForegroundColor Yellow
    docker build -t "$username/dislexia-backend:latest" .

    Write-Host "Publicando imagen..." -ForegroundColor Yellow
    docker push "$username/dislexia-backend:latest"

    Write-Host "✅ Imagen publicada!" -ForegroundColor Green
    Write-Host "URL: https://hub.docker.com/r/$username/dislexia-backend" -ForegroundColor Cyan
}

# Ejecutar comando
switch ($Command.ToLower()) {
    "start" { Start-Services }
    "stop" { Stop-Services }
    "restart" { Restart-Services }
    "logs" { Show-Logs }
    "logs-api" { Show-APILogs }
    "logs-web" { Show-WebLogs }
    "build" { Build-Images }
    "clean" { Clean-All }
    "migrate" { Run-Migrate }
    "makemigrations" { Run-MakeMigrations }
    "createsuperuser" { Create-Superuser }
    "shell" { Open-Shell }
    "test" { Show-URLs }
    "publish" { Publish-Image }
    "help" { Show-Help }
    default {
        Write-Host "❌ Comando no reconocido: $Command" -ForegroundColor Red
        Write-Host ""
        Show-Help
    }
}
