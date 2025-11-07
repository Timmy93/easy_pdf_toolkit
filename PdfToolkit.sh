#!/bin/bash

# Spostati nella directory dello script
cd "$(dirname "$0")"

# Crea l'ambiente virtuale se non esiste
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    /usr/bin/python3 -m venv venv
fi

# Attiva l'ambiente virtuale
echo "Activating virtual environment..."
source venv/bin/activate

# Installa i pacchetti richiesti se il file requirements.txt esiste
if [ -f "requirements.txt" ]; then
    echo "Installing requirements..."
    pip install -r requirements.txt --disable-pip-version-check
fi

# Esegui lo script Python in background (senza terminale)
echo "Running main.py..."
nohup python3 main.py > /dev/null 2>&1 &

# Disattiva l'ambiente virtuale
deactivate

