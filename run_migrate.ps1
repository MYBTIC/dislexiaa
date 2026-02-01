# Script to test and run Django migrations
Write-Host "=== Testing Django Migration Fix ===" -ForegroundColor Cyan
Write-Host ""

# Set the project directory
$projectDir = "C:\Users\Maxip\OneDrive\Documentos\Prepolitecinca\SeptimoSemestre\Usabilidad y Accesibilidad\Proyecto"
Set-Location $projectDir

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& "$projectDir\.venv\Scripts\Activate.ps1"

# Test import first
Write-Host ""
Write-Host "Testing if views.py can be imported..." -ForegroundColor Yellow
& python test_import.py

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "Import test passed! Running migrations..." -ForegroundColor Green
    Write-Host ""

    # Run migrations
    & python manage.py migrate

    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "=== SUCCESS! Migrations completed ===" -ForegroundColor Green
        Write-Host ""
        Write-Host "You can now run: python manage.py runserver" -ForegroundColor Cyan
    } else {
        Write-Host ""
        Write-Host "=== Migration failed ===" -ForegroundColor Red
    }
} else {
    Write-Host ""
    Write-Host "=== Import test failed ===" -ForegroundColor Red
    Write-Host "Please check the error messages above." -ForegroundColor Red
}
