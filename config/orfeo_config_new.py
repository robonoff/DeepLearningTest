#!/usr/bin/env python3
"""
Configurazione per il cluster Orfeo con llama3.3:latest
Usa le variabili d'ambiente impostate da set_env.sh
"""

import os

# Recupera le variabili d'ambiente (impostate da source config/set_env.sh)
token = os.getenv("TOKEN")
model = os.getenv("ORFEO_MODEL")
base_url = os.getenv("ORFEO_BASE_URL")

if not token:
    raise ValueError("TOKEN non definito. Esegui: source config/set_env.sh")
if not model:
    raise ValueError("ORFEO_MODEL non definito. Esegui: source config/set_env.sh")
if not base_url:
    raise ValueError("ORFEO_BASE_URL non definito. Esegui: source config/set_env.sh")
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

# Configurazione RAG
RAG_CONFIG = {
    "USE_WEB_SEARCH": True,
    "SEARCH_CACHE_DURATION": 3600,  # 1 ora
    "MAX_SEARCH_RESULTS": 8,
    "WEB_CONTEXT_MAX_LENGTH": 400,
    "SEARCH_TIMEOUT": 10,
    "EMBEDDING_MODEL": "all-MiniLM-L6-v2", #hugging face embbeddings
    "TOP_K_JOKES": 10 # Numero di battute recuperate dai dataset
}

def get_rag_config():
    """Get RAG configuration"""
    return RAG_CONFIG
