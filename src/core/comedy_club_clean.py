#!/usr/bin/env python3
"""
Comedy Club Simulator - Solo modalità Orfeo
"""

import sys
import os
import random
import time

# Aggiungi path per imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, '..', '..'))

from src.core.orfeo_client_new import OrfeoClient
from config.orfeo_config_new import is_orfeo_available

class ComedyClub:
    """Simulatore comedy club - solo modalità Orfeo"""
    
    def __init__(self):
        """Inizializza il comedy club"""
        
        if not is_orfeo_available():
            raise ValueError("⚠️ Token non configurato. Esegui: source config/set_env.sh")
        
        self.client = OrfeoClient()
        
        self.comedians = {
            "Jerry": {
                "style": "observational humor",
                "persona": "keen observer of everyday life"
            },
            "Penny": {
                "style": "wordplay and puns", 
                "persona": "witty wordsmith who loves clever puns"
            },
            "Raven": {
                "style": "dark humor",
                "persona": "mysterious comedian with dark wit"
            },
            "Cosmic": {
                "style": "absurd and surreal humor",
                "persona": "cosmic jester with surreal observations"
            }
        }
        
        self.topics = [
            "technology", "everyday life", "social media", "food", 
            "work", "relationships", "travel", "weather", "coffee", "smartphones"
        ]
        
        print(f"🎭 Comedy Club inizializzato con Orfeo")
        print(f"   Comici: {len(self.comedians)}")
    
    def get_joke(self, comedian_name=None, topic=None):
        """Ottieni una battuta da un comico"""
        
        comedian_name = comedian_name or random.choice(list(self.comedians.keys()))
        topic = topic or random.choice(self.topics)
        
        if comedian_name not in self.comedians:
            raise ValueError(f"⚠️ Comico {comedian_name} non trovato!")
        
        comedian = self.comedians[comedian_name]
        
        prompt = f"""You are {comedian_name}, a comedian who is a {comedian['persona']} and specializes in {comedian['style']}.

Create a short, funny joke or observation about {topic}. Keep it to 1-2 sentences and make it genuinely funny.

Topic: {topic}
Your comedy style: {comedian['style']}

Your joke:"""
        
        print(f"🎤 {comedian_name} sta raccontando una battuta su {topic}...")
        response = self.client.generate(prompt, max_tokens=150)
        
        return f"{comedian_name}: {response}"
    
    def run_show(self, rounds=2):
        """Esegui uno spettacolo completo"""
        
        print("\n" + "="*60)
        print("🎭 BENVENUTI AL COMEDY CLUB AI CON ORFEO! 🎭")
        print("   Stasera abbiamo 4 fantastici comici AI!")
        print("="*60)
        
        for round_num in range(1, rounds + 1):
            print(f"\n🎪 ROUND {round_num}")
            print("-" * 40)
            
            topic = random.choice(self.topics)
            print(f"🎯 Tema di stasera: {topic.upper()}")
            
            # Mescola i comici per questo round
            comedians_order = list(self.comedians.keys())
            random.shuffle(comedians_order)
            
            for comedian in comedians_order:
                print(f"\n🎤 Sul palco: {comedian}!")
                try:
                    joke = self.get_joke(comedian, topic)
                    print(f"   {joke}")
                    
                    # Reazione del pubblico
                    reactions = ["👏 Grandi risate!", "🎉 Applausi!", "⭐ Fantastico!", "😂 Il pubblico impazzisce!"]
                    print(f"   {random.choice(reactions)}")
                    
                except Exception as e:
                    print(f"   ⚠️ {comedian} ha avuto problemi tecnici: {e}")
                
                time.sleep(1)  # Pausa tra performance
        
        print(f"\n" + "="*60)
        print("🎭 Grazie a tutti! Spettacolo terminato!")
        print("="*60)

    def interactive_mode(self):
        """Modalità interattiva"""
        print("\n🎭 MODALITÀ INTERATTIVA CON ORFEO")
        print("Comandi disponibili:")
        print("  - Premi ENTER per una battuta casuale")
        print("  - 'show' per uno spettacolo completo")
        print("  - 'show 3' per uno spettacolo di 3 round")
        print("  - nome_comico per una battuta di quel comico")
        print("  - 'quit' per uscire")
        print("-" * 50)
        
        while True:
            try:
                user_input = input("\n🎪 Cosa vuoi fare? ").strip().lower()
                
                if user_input == 'quit':
                    print("👋 Arrivederci!")
                    break
                elif user_input == '':
                    # Battuta casuale
                    try:
                        joke = self.get_joke()
                        print(f"🎤 {joke}")
                    except Exception as e:
                        print(f"⚠️ Errore: {e}")
                elif user_input.startswith('show'):
                    # Spettacolo
                    parts = user_input.split()
                    rounds = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 2
                    try:
                        self.run_show(rounds)
                    except Exception as e:
                        print(f"⚠️ Errore durante lo spettacolo: {e}")
                elif user_input.capitalize() in self.comedians:
                    # Battuta di un comico specifico
                    comedian = user_input.capitalize()
                    try:
                        joke = self.get_joke(comedian)
                        print(f"🎤 {joke}")
                    except Exception as e:
                        print(f"⚠️ Errore: {e}")
                else:
                    print("⚠️ Comando non riconosciuto. Prova 'quit', 'show', o il nome di un comico.")
                    
            except KeyboardInterrupt:
                print("\n👋 Arrivederci!")
                break
            except Exception as e:
                print(f"⚠️ Errore: {e}")

if __name__ == "__main__":
    # Test
    try:
        club = ComedyClub()
        
        print("\n🧪 Test battuta singola:")
        joke = club.get_joke()
        print(joke)
        
    except Exception as e:
        print(f"⚠️ Errore: {e}")
        print("💡 Assicurati di aver eseguito: source config/set_env.sh")
