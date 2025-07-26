#!/usr/bin/env python3
"""
Client per comunicare con llama3.3:latest su cluster Orfeo
Usa la nuova configurazione con dotenv
"""

import requests
import json
import uuid
import time
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
            print("⚠️ Orfeo non configurato correttamente")
            self.available = False
            return
            
        self.config = get_config_list()[0]  # Usa la nuova configurazione
        self.available = True
        
        print("🚀 OrfeoClient inizializzato:")
        print(f"   Modello: {self.config['model']}")
        print(f"   URL: {self.config['base_url']}")
        print(f"   SSH: {self.config['ssh_command']}")
    
    def generate(self, prompt, max_tokens=None, temperature=None):
        """Genera una risposta usando il modello su Orfeo"""
        
        if not self.available:
            return "⚠️ Orfeo non disponibile - controlla token e configurazione"
        
        try:
            # Payload semplice per test
            data = {
                "model": self.config["model"],
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": temperature or self.config.get("temperature", 0.7),
                    "num_predict": max_tokens or 150
                }
            }
            
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.config['api_key']}"
            }
            
            print(f"🔄 Invio richiesta a Orfeo...")
            response = requests.post(
                f"{self.config['base_url']}/generate",
                json=data,
                headers=headers,
                timeout=120
            )
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Risposta ricevuta da Orfeo")
                
                # Gestisci diversi formati di risposta
                if "response" in result:
                    return result["response"]
                elif "choices" in result and len(result["choices"]) > 0:
                    return result["choices"][0]["message"]["content"]
                else:
                    return str(result)
            else:
                print(f"❌ Errore API: {response.status_code}")
                return f"⚠️ Errore API Orfeo: {response.status_code} - {response.text}"
                
        except requests.exceptions.ConnectionError:
            return "⚠️ Impossibile connettersi a Orfeo - verifica connessione"
        except requests.exceptions.Timeout:
            return "⚠️ Timeout connessione Orfeo"
        except Exception as e:
            return f"⚠️ Errore inaspettato: {str(e)}"


class MockClient:
    """Client di test per sviluppo"""
    
    def __init__(self):
        print("🧪 MockClient inizializzato - modalità sviluppo")
    
    def generate(self, prompt, max_tokens=None, temperature=None):
        """Genera risposte di test"""
        import random
        
        jokes = [
            "Why do programmers prefer dark mode? Because light attracts bugs!",
            "I told my computer a joke about UDP... but I'm not sure if it got it.",
            "Why do Python programmers prefer snakes? Because they don't like Java!",
            "There are only 10 types of people: those who understand binary and those who don't.",
            "Why did the developer go broke? Because he used up all his cache!",
            "I would tell you a joke about REST APIs, but you'd have to GET it yourself.",
            "Why do we tell actors to break a leg? Because every play has a cast!",
            "I'm reading a book about anti-gravity. It's impossible to put down!"
        ]
        return f"{random.choice(jokes)}"
