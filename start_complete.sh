#!/bin/bash

# Script di avvio completo per Comedy Club AI
echo "🎭 Comedy Club AI - Sistema Avvio Completo"
echo "=========================================="

# 1. Imposta le variabili d'ambiente
echo "🔧 Caricamento configurazione..."
source config/set_env.sh

# 2. Controlla se python-dotenv è installato
echo "📦 Controllo dipendenze..."
if ! python3 -c "import dotenv" 2>/dev/null; then
    echo "⚠️ python-dotenv non installato. Installazione..."
    pip3 install python-dotenv
fi

# 3. Test della configurazione
echo "✅ Test configurazione..."
if python3 -c "from config.orfeo_config_new import is_orfeo_available; exit(0 if is_orfeo_available() else 1)"; then
    echo "✅ Configurazione Orfeo OK"
    echo "🚀 Avvio con Orfeo..."
    python3 main_clean.py
else
    echo "⚠️ Configurazione Orfeo non valida"
    echo "🧪 Avvio in modalità mock..."
    python3 main_clean.py --mock
fi
