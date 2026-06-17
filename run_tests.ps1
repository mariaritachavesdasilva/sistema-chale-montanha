# Script de execucao dos testes - Chale Montanha
$env:PATH += ";$env:USERPROFILE\.local\bin"
$env:PYTHONPATH = $PSScriptRoot

Write-Host "=============================================" -ForegroundColor Cyan
Write-Host " Chale Montanha - Suite de Testes " -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan

uv run --with flask --with pytest pytest tests/test_app.py -v