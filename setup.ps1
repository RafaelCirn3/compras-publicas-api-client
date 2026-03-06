# Script de Setup do Projeto
# Execute este script para configurar o ambiente

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  Sistema de Busca de Processos de Compras Publicas" -ForegroundColor White
Write-Host "  Setup e Instalacao" -ForegroundColor White
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Verifica Python
Write-Host "[1/4] Verificando Python..." -ForegroundColor Yellow
$pythonExists = $false
try {
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  [OK] $pythonVersion encontrado" -ForegroundColor Green
        $pythonExists = $true
    }
}
catch {
    Write-Host "  [ERRO] Python nao encontrado. Por favor, instale Python 3.8+" -ForegroundColor Red
    exit 1
}

if (-not $pythonExists) {
    Write-Host "  [ERRO] Python nao encontrado. Por favor, instale Python 3.8+" -ForegroundColor Red
    exit 1
}

# Cria ambiente virtual
Write-Host ""
Write-Host "[2/4] Criando ambiente virtual..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "  Ambiente virtual ja existe" -ForegroundColor Gray
}
else {
    python -m venv venv
    Write-Host "  [OK] Ambiente virtual criado" -ForegroundColor Green
}

# Ativa ambiente virtual e instala dependencias
Write-Host ""
Write-Host "[3/4] Instalando dependencias..." -ForegroundColor Yellow
& "venv\Scripts\python.exe" -m pip install --upgrade pip --quiet
& "venv\Scripts\pip.exe" install -r requirements.txt --quiet
Write-Host "  [OK] Dependencias instaladas" -ForegroundColor Green

# Verifica .env
Write-Host ""
Write-Host "[4/4] Verificando configuracao..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "  [OK] Arquivo .env encontrado" -ForegroundColor Green
}
else {
    Write-Host "  [AVISO] Arquivo .env nao encontrado" -ForegroundColor Yellow
    Write-Host "  Criando .env a partir de .env.example..." -ForegroundColor Gray
    Copy-Item .env.example .env
    Write-Host "  [OK] Arquivo .env criado" -ForegroundColor Green
    Write-Host ""
    Write-Host "  [ATENCAO] Configure sua PUBLIC_KEY no arquivo .env" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  Setup concluido!" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan

Write-Host ""
Write-Host "Proximos passos:" -ForegroundColor White
Write-Host "  1. Edite o arquivo .env e configure sua PUBLIC_KEY" -ForegroundColor Gray
Write-Host "  2. Ative o ambiente virtual: venv\Scripts\activate" -ForegroundColor Gray
Write-Host "  3. Execute o programa: python main.py" -ForegroundColor Gray
Write-Host ""
