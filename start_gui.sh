#!/bin/bash

# Script per avviare la GUI del Comedy Club con Orfeo
# Esegui: bash start_gui.sh

echo "🎭 Avvio Comedy Club GUI con Orfeo..."

# Carica le variabili d'ambiente
source config/set_env.sh

# Avvia la GUI
python3 src/gui/comedy_club_gui.py
