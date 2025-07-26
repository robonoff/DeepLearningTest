#!/usr/bin/env python3
"""
Comedy Club Simulator - Versione semplificata e funzionante
"""

import sys
import os
import random
import time

# Aggiungi path per imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, '..', '..'))

try:
    from src.core.orfeo_client_new import OrfeoClient, MockClient
    from config.orfeo_config_new import is_orfeo_available
except ImportError as e:
    print(f"Import error: {e}")
    # Fallback semplice
    class MockClient:
        def generate(self, prompt, **kwargs):
            return "Mock joke: Why did the AI cross the road? To get to the other dataset!"
    
    def is_orfeo_available():
        return False

class ComedyClub:
    """Simulatore comedy club"""
    
    def __init__(self, use_mock=False):
        """Inizializza il comedy club"""
        
        try:
            if use_mock or not is_orfeo_available():
                self.client = MockClient()
                self.mode = "Mock"
            else:
                from src.core.orfeo_client_new import OrfeoClient
                self.client = OrfeoClient()
                self.mode = "Orfeo"
        except:
            self.client = MockClient()
            self.mode = "Mock"
        
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
        
        print(f"🎭 Comedy Club inizializzato")
        print(f"   Modalità: {self.mode}")
        print(f"   Comici: {len(self.comedians)}")
    
    def get_joke(self, comedian_name=None, topic=None):
        """Ottieni una battuta da un comico"""
        
        comedian_name = comedian_name or random.choice(list(self.comedians.keys()))
        topic = topic or random.choice(self.topics)
        
        if comedian_name not in self.comedians:
            return f"⚠️ Comico {comedian_name} non trovato!"
        
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
        print("🎭 BENVENUTI AL COMEDY CLUB AI! 🎭")
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
                joke = self.get_joke(comedian, topic)
                print(f"   {joke}")
                
                # Reazione del pubblico
                reactions = ["👏 Grandi risate!", "🎉 Applausi!", "⭐ Fantastico!", "😂 Il pubblico impazzisce!"]
                print(f"   {random.choice(reactions)}")
                
                time.sleep(1)  # Pausa tra performance
        
        print(f"\n" + "="*60)
        print("🎭 Grazie a tutti! Spettacolo terminato!")
        print("="*60)

    def interactive_mode(self):
        """Modalità interattiva"""
        print("\n🎭 MODALITÀ INTERATTIVA")
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
                    joke = self.get_joke()
                    print(f"🎤 {joke}")
                elif user_input.startswith('show'):
                    # Spettacolo
                    parts = user_input.split()
                    rounds = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 2
                    self.run_show(rounds)
                elif user_input.capitalize() in self.comedians:
                    # Battuta di un comico specifico
                    comedian = user_input.capitalize()
                    joke = self.get_joke(comedian)
                    print(f"🎤 {joke}")
                else:
                    print("⚠️ Comando non riconosciuto. Prova 'quit', 'show', o il nome di un comico.")
                    
            except KeyboardInterrupt:
                print("\n👋 Arrivederci!")
                break
            except Exception as e:
                print(f"⚠️ Errore: {e}")

if __name__ == "__main__":
    # Test veloce
    club = ComedyClub(use_mock=True)  # Usa mock per test veloce
    
    print("\n🧪 Test battuta singola:")
    joke = club.get_joke()
    print(joke)
    
    print("\n🧪 Test spettacolo breve:")
    club.run_show(rounds=1)
