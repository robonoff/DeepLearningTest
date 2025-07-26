#!/usr/bin/env python3
"""
Configurazione per il cluster Orfeo con llama3.3:latest
Usa dotenv per gestire il token JWT in modo sicuro
"""

import os
from dotenv import load_dotenv

# Carica le variabili d'ambiente dal file .env
load_dotenv()

# Recupera il token JWT dal file .env
token = os.getenv("TOKEN")
model = os.getenv("ORFEO_MODEL")
base_url = os.getenv("ORFEO_BASE_URL")

if not token:
    raise ValueError("TOKEN non definito. Esegui: export TOKEN='...' o crea file .env")
if not model:
    raise ValueError("ORFEO_MODEL non definito. Esegui: export ORFEO_MODEL='...' o crea file .env")
if not base_url:
    raise ValueError("ORFEO_BASE_URL non definito. Esegui: export ORFEO_BASE_URL='...' o crea file .env")
# Configurazione per cluster Orfeo con llama3.3:latest
config_list = [
    {
        "model": model,
        "api_key": token,
        "base_url": base_url,
        "temperature": 0.7,
        "ssh_command": "ssh -L 8080:10.128.2.165:8080 orfeo"
    }
]

def get_config_list():
    """Restituisce la lista di configurazioni per AutoGen"""
    return config_list

def is_orfeo_available():
    """Verifica se Orfeo è configurato correttamente"""
    return token is not None

def get_ssh_command():
    """Restituisce il comando SSH per il port forwarding"""
    return config_list[0]["ssh_command"]
