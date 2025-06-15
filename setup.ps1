# setup.ps1
# Script di setup per il progetto Python
# Autore: Valerio Molinari
# Versione: 1.0
# Data: 14/06/2025

# se powershell non lo esegue attiva i permessi con
# Set-ExecutionPolicy RemoteSigned -Scope Process

Write-Host "Inizio setup del progetto Guibot..." -ForegroundColor Cyan

# Controllo se Python è installato
$pythonPath = Get-Command python -ErrorAction SilentlyContinue
if (-Not $pythonPath) {
    Write-Host "Python non è installato o non è nel PATH. Assicurati di aver installato Python 3.x." -ForegroundColor Red
    exit 1
} else {
    Write-Host "Python trovato: $($pythonPath.Path)" -ForegroundColor Green
}
# Controllo se pip è installato
$pipPath = Get-Command pip -ErrorAction SilentlyContinue
if (-Not $pipPath) {
    Write-Host "pip non è installato o non è nel PATH. Assicurati di aver installato pip." -ForegroundColor Red
    exit 1
} else {
    Write-Host "pip trovato: $($pipPath.Path)" -ForegroundColor Green
}


# Ottieni la directory dello script
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
Write-Host "Entrando nella directory del progetto... " -NoNewline
Set-Location $ScriptDir
if ($?) {
    Write-Host "OK"
} else {
    Write-Host "Errore nell'entrare nella directory del progetto."
    exit 1
}

# Creazione ambiente virtuale
Write-Host "Creazione ambiente virtuale... " -NoNewline
if (-Not (Test-Path "$ScriptDir\venv")) {
    python -m venv venv
    if ($?) {
        Write-Host "OK"
    } else {
        Write-Host "Errore nella creazione dell'ambiente virtuale."
        exit 1
    }
} else {
    Write-Host "Ambiente virtuale già esistente."
}

# Attivazione ambiente virtuale
Write-Host "Attivazione ambiente virtuale... " -NoNewline
$ActivateScript = "$ScriptDir\venv\Scripts\Activate.ps1"
if (Test-Path $ActivateScript) {
    . $ActivateScript
    if ($?) {
        Write-Host "OK"
    } else {
        Write-Host "Errore nell'attivazione dell'ambiente virtuale."
        exit 1
    }
} else {
    Write-Host "Script di attivazione non trovato: $ActivateScript"
    exit 1
}

# Installazione dipendenze
Write-Host "Installazione dipendenze... " -NoNewline
pip install .
if ($?) {
    Write-Host "OK"
} else {
    Write-Host "Errore nell'installazione delle dipendenze."
    exit 1
}


# Impostazione PYTHONPATH per permettere import di src.*
Write-Host "Impostazione PYTHONPATH... " -NoNewline
$env:PYTHONPATH = (Get-Location).Path
if ($env:PYTHONPATH) {
    Write-Host "OK"
} else {
    Write-Host "Errore nella definizione del PYTHONPATH."
    exit 1
}
