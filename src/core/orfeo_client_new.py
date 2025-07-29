"""
Client per comunicare con llama3.3:latest su cluster Orfeo
"""

import requests
import json
import sys
import os

# Aggiungi config al path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from config.orfeo_config_new import get_config_list, is_orfeo_available

class OrfeoClient:
    """Client per comunicare con il modello llama3.3:latest su cluster Orfeo"""
    
    def __init__(self):
        """Inizializza il client Orfeo"""
        
        if not is_orfeo_available():
            raise ValueError("⚠️ Orfeo non configurato correttamente - controlla TOKEN in .env")
            
        self.config = get_config_list()[0]
        
        print("🚀 OrfeoClient inizializzato:")
        print(f"   Modello: {self.config['model']}")
        print(f"   URL: {self.config['base_url']}")
        print(f"   SSH: {self.config['ssh_command']}")
    
    def generate(self, prompt, max_tokens=None, temperature=None):
        """Genera una risposta usando il modello su Orfeo via Open WebUI"""
        
        try:
            # Prepara payload nel formato Open WebUI standard
            data = {
                "model": self.config["model"],
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "temperature": temperature or self.config.get("temperature", 0.7),
                "max_tokens": max_tokens or 150
            }
            
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.config['api_key']}"
            }
            
            print(f"🔄 Invio richiesta a Orfeo (Open WebUI standard)...")
            
            # Usa l'endpoint Open WebUI standard per chat completions
            endpoint = f"{self.config['base_url']}/chat/completions"
            print(f"🔄 Endpoint: {endpoint}")
            
            response = requests.post(
                endpoint,
                json=data,
                headers=headers,
                timeout=30  # Ridotto da 120 a 30 secondi per maggiore reattività
            )
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Risposta ricevuta da Orfeo")
                
                # Formato standard OpenAI-compatible
                if "choices" in result and len(result["choices"]) > 0:
                    return result["choices"][0]["message"]["content"]
                elif "response" in result:
                    return result["response"]
                else:
                    return str(result)
            
            # Fallback: prova endpoint Ollama diretto se disponibile
            print(f"🔄 Fallback: provo endpoint Ollama diretto...")
            
            data_direct = {
                "model": self.config["model"],
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": temperature or self.config.get("temperature", 0.7),
                    "num_predict": max_tokens or 150
                }
            }
            
            response = requests.post(
                f"{self.config['base_url']}/generate",
                json=data_direct,
                headers=headers,
                timeout=30  # Ridotto da 120 a 30 secondi per maggiore reattività
            )
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Risposta ricevuta da Orfeo (Ollama)")
                
                if "response" in result:
                    return result["response"]
                else:
                    return str(result)
            else:
                error_msg = f"⚠️ Errore API Orfeo: {response.status_code} - {response.text}"
                print(f"❌ {error_msg}")
                raise Exception(error_msg)
                
        except requests.exceptions.ConnectionError:
            error_msg = "⚠️ Impossibile connettersi a Orfeo - verifica connessione di rete"
            print(f"❌ {error_msg}")
            raise Exception(error_msg)
        except requests.exceptions.Timeout:
            error_msg = "⚠️ Timeout connessione Orfeo"
            print(f"❌ {error_msg}")
            raise Exception(error_msg)
        except Exception as e:
            print(f"❌ Errore: {e}")
            raise
