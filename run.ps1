# Script de execucao do servidor - Chale Montanha
$env:PATH += ";$env:USERPROFILE\.local\bin"

Write-Host "=============================================" -ForegroundColor Green
Write-Host " Iniciando o Servidor do Chale Montanha " -ForegroundColor Green
Write-Host " Pressione Ctrl+C para parar. " -ForegroundColor Yellow
Write-Host "=============================================" -ForegroundColor Green

uv run --with flask flask run
