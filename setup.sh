#!/usr/bin/env bash
# Script di setup per il progetto Python
# Autore: Valerio Molinari
# Versione: 1.0
# Data: 14/06/2025
# Descrizione: Questo script 


# Script di setup per il progetto Python
echo "Inizio il setup di Guibot..."

# Entrare nella directory dove si trova lo script
echo "Entrando nella directory del progetto..."
cd "$(cd "$(dirname "$0")" && pwd)" || {
    echo "Errore nell'entrare nella directory del progetto."
    exit 1
}
echo "OK"

# Controllo dipendenze di sistema (solo Linux)
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo -n "Controllo pacchetti di sistema richiesti... "

    PY_VER=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
    DEV_PKG="python${PY_VER}-dev"

    MISSING=""
    for pkg in build-essential $DEV_PKG; do
        dpkg -s "$pkg" >/dev/null 2>&1
        if [ $? -ne 0 ]; then
            MISSING="$MISSING $pkg"
        fi
    done

    if [ -n "$MISSING" ]; then
        echo "Pacchetti mancanti: $MISSING"
        echo "Installazione in corso..."
        sudo apt update && sudo apt install -y $MISSING
        if [ $? -eq 0 ]; then
            echo "OK"
        else
            echo "Errore nell'installazione dei pacchetti richiesti."
            exit 1
        fi
    else
        echo "OK"
    fi
fi


# Creazione ambiente virtuale
echo -n "Creazione ambiente virtuale... "
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "OK"
else
    echo "Ambiente virtuale già esistente."
fi

# Attivazione ambiente virtuale
echo -n "Attivazione ambiente virtuale... "
# Controllo se è Unix o Windows
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" || "$OSTYPE" == "cygwin" ]]; then
    # Windows
    source venv/Scripts/activate
else
    # Unix
    source venv/bin/activate
fi

if [ $? -eq 0 ]; then
    echo "OK"
else
    echo "Errore nell'attivazione dell'ambiente virtuale."
    exit 1
fi

# Installazione dipendenze
echo -n "Installazione dipendenze... "
pip install .
if [ $? -eq 0 ]; then
    echo "OK"
else
    echo "Errore nell'installazione delle dipendenze."
    exit 1
fi

# Assicura il riconoscimento del modulo src
echo -n "Assicurando il riconoscimento del modulo src... "
export PYTHONPATH=.

if [ $? -eq 0 ]; then
    echo "OK"
else
    echo "Errore nell'impostazione del PYTHONPATH."
    exit 1
fi


echo -e "\nSetup completato. Ora attiva il venv locale con e il PYTHONPATH:"
echo -e "\t\x1b[36msource venv/bin/activate\n"
echo -e "\t\x1b[36mexport PYTHONPATH=.\n"
echo -e "\x1b[0m"
