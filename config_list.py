from dotenv import load_dotenv
import os
import json


import os
from dotenv import load_dotenv

# Carica le variabili d'ambiente dal file .env
load_dotenv()

# Recupera il token JWT dal file .env
token = os.getenv("TOKEN")
if not token:
    raise ValueError("TOKEN non definito. Esegui: export TOKEN='...'")

config_list = [
    {
        "model": "llama3.3:latest", 
        "api_key": token,
        "base_url": "http://10.128.2.165:8080/api"
    }
]



