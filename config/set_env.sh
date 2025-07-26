#!/bin/bash

# Script per impostare le variabili d'ambiente per Orfeo
# Esegui: source set_env.sh

echo "🔧 Impostazione variabili d'ambiente per Orfeo..."

# Imposta il token JWT
export TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImZhM2IxMDAyLThjMDUtNGIzNy05MWY2LTRiYjJhZmNlODEyZiJ9.RNBz5tslyWSW15Xuc3SsWDTPmwv37ZLYY2GftWo2GAw"
export ORFEO_MODEL="llama3.3:latest"
export ORFEO_BASE_URL="http://10.128.2.165:8080/api"