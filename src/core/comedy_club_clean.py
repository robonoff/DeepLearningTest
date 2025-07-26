#!/usr/bin/env python3
"""
Comedy Club Simulator - Solo modalità Orfeo con RAG Enhancement
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

# Importa RAG system se disponibile
try:
    from src.utils.enhanced_joke_rag import EnhancedJokeRAG
    RAG_AVAILABLE = True
except ImportError:
    RAG_AVAILABLE = False
    print("⚠️ Sistema RAG non disponibile. Installa: pip install sentence-transformers scikit-learn duckduckgo-search")

class ComedyClub:
    """Simulatore comedy club - modalità Orfeo con RAG Enhancement"""
    
    def __init__(self, use_web_search: bool = True):
        """Inizializza il comedy club con supporto RAG opzionale"""
        
        if not is_orfeo_available():
            raise ValueError("⚠️ Token non configurato. Esegui: source config/set_env.sh")
        
        self.client = OrfeoClient()
        self.use_web_search = use_web_search
        
        # Inizializza sistema RAG se disponibile
        self.enhanced_rag = None
        if RAG_AVAILABLE:
            try:
                self.enhanced_rag = EnhancedJokeRAG()
                if self.enhanced_rag.is_available():
                    print("✅ Sistema RAG inizializzato")
                else:
                    print("⚠️ Sistema RAG non completamente disponibile")
                    self.enhanced_rag = None
            except Exception as e:
                print(f"⚠️ Inizializzazione RAG fallita: {e}")
                self.enhanced_rag = None
        
        self.comedians = {
            "Jerry": {
                "style": "observational humor",
                "persona": "sharp observer of everyday absurdities",
                "catchphrases": ["What's the deal with", "Have you ever noticed", "Why do we"],
                "tone": "conversational, incredulous, questioning"
            },
            "Penny": {
                "style": "wordplay and puns", 
                "persona": "clever wordsmith who loves linguistic twists",
                "catchphrases": ["What do you call", "Why did the", "How do you spell"],
                "tone": "playful, clever, punny"
            },
            "Raven": {
                "style": "dark humor",
                "persona": "sardonic comedian who finds humor in dark places",
                "catchphrases": ["Death is", "My ex", "Life's too short"],
                "tone": "cynical, witty, darkly amusing"
            },
            "Cosmic": {
                "style": "absurd and surreal humor",
                "persona": "wild comedian with bizarre observations",
                "catchphrases": ["Imagine if", "What if", "In a parallel universe"],
                "tone": "surreal, unexpected, random"
            }
        }
       
        self.topics = [
            "technology", "everyday life", "social media", "food", 
            "work", "relationships", "travel", "weather", "coffee", "smartphones"
        ]
        
        print(f"🎭 Comedy Club inizializzato con Orfeo")
        print(f"   Comici: {len(self.comedians)}")
        print(f"   RAG: {'✅ Attivo' if self.enhanced_rag else '❌ Non disponibile'}")
        print(f"   Web Search: {'✅ Attivo' if self.use_web_search else '❌ Disabilitato'}")
    
        
    def get_joke(self, comedian_name=None, topic=None):
        """Ottieni una battuta da un comico con supporto RAG opzionale"""
        
        comedian_name = comedian_name or random.choice(list(self.comedians.keys()))
        topic = topic or random.choice(self.topics)
        
        if comedian_name not in self.comedians:
            raise ValueError(f"⚠️ Comico {comedian_name} non trovato!")
        
        comedian_info = self.comedians[comedian_name]
        
        # Usa RAG migliorato se disponibile e topic fornito
        if self.enhanced_rag and topic:
            try:
                rag_result = self.enhanced_rag.retrieve_jokes_with_context(
                    comedian_info['style'], 
                    topic, 
                    use_web_search=self.use_web_search,
                    top_k=3
                )
                
                sample_jokes = rag_result["jokes"]
                web_context = rag_result["web_context"]
                
                # Prompt migliorato con personalità e esempi reali
                base_prompt = f"You are {comedian_name}, a comedian with a {comedian_info['tone']} style. "
                base_prompt += f"You specialize in {comedian_info['style']}. "
                
                # Aggiungi esempi di stile dal dataset
                if sample_jokes:
                    base_prompt += f"Here are examples of your comedy style:\n"
                    for i, joke in enumerate(sample_jokes[:3], 1):
                        base_prompt += f"{i}. {joke}\n"
                    base_prompt += "\n"
                
                # Aggiungi frasi caratteristiche
                if comedian_info.get('catchphrases'):
                    phrase = random.choice(comedian_info['catchphrases'])
                    base_prompt += f"Use your signature style (like '{phrase}...'). "
                
                base_prompt += f"Now create ONE short, funny joke about {topic}. "
                base_prompt += "Keep it under 30 words. Make it genuinely hilarious and memorable. "
                
                if web_context:
                    base_prompt += f"Current context: {web_context[:150]}. "
                    
                base_prompt += f"\nTopic: {topic}\nYour joke:"
                
                print(f"🎤 {comedian_name} sta raccontando una battuta su {topic} (con RAG)...")
                response = self.client.generate(base_prompt, max_tokens=200)
                
                return f"{comedian_name}: {response}"
                
            except Exception as e:
                print(f"⚠️ RAG retrieval fallito, uso metodo standard: {e}")
                # Fallback al metodo originale
        
        # Metodo originale come fallback migliorato
        comedian_info = self.comedians[comedian_name]
        
        # Usa frasi caratteristiche anche nel fallback
        catchphrase = ""
        if comedian_info.get('catchphrases'):
            catchphrase = f"Use your signature style (like '{random.choice(comedian_info['catchphrases'])}...'). "
        
        prompt = f"""You are {comedian_name}, a comedian with a {comedian_info['tone']} style specializing in {comedian_info['style']}.

{catchphrase}Create ONE short, hilarious joke about {topic}. Keep it under 30 words. Make it genuinely funny and memorable.

Topic: {topic}
Your joke:"""
        
        print(f"🎤 {comedian_name} sta raccontando una battuta su {topic}...")
        response = self.client.generate(prompt, max_tokens=80)  # Ancora più corto
        
        return f"{comedian_name}: {response}"
    
    def run_show(self, rounds=2):
        """Esegui uno spettacolo completo"""
        
        print("\n" + "="*60)
        print("🎭 BENVENUTI AL COMEDY CLUB AI ! 🎭")
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
        """Modalità interattiva con comandi RAG"""
        print(f"\n🎭 MODALITÀ INTERATTIVA CON ORFEO {'+ RAG' if self.enhanced_rag else ''}")
        print("Comandi disponibili:")
        print("  - Premi ENTER per una battuta casuale")
        print("  - 'show' per uno spettacolo completo")
        print("  - 'show 3' per uno spettacolo di 3 round")
        print("  - nome_comico per una battuta di quel comico")
        if self.enhanced_rag:
            print("  - 'web on/off' per abilitare/disabilitare ricerca web")
            print("  - 'rag status' per vedere lo stato del sistema RAG")
        print("  - 'quit' per uscire")
        print("-" * 50)
        
        while True:
            try:
                user_input = input(f"\n🎪 Cosa vuoi fare? {'[RAG: ON]' if self.enhanced_rag else ''} ").strip().lower()
                
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
                elif user_input == 'web on':
                    self.use_web_search = True
                    print("🌐 Ricerca web abilitata")
                elif user_input == 'web off':
                    self.use_web_search = False
                    print("🌐 Ricerca web disabilitata")
                elif user_input == 'rag status':
                    if self.enhanced_rag:
                        print(f"✅ RAG: Attivo")
                        print(f"🌐 Web Search: {'Attivo' if self.use_web_search else 'Disabilitato'}")
                        print(f"📊 Jokes caricati: {len([j for cat in self.enhanced_rag.jokes_data.values() for j in cat]) if self.enhanced_rag.jokes_data else 0}")
                    else:
                        print("❌ RAG: Non disponibile")
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
                    if self.enhanced_rag:
                        print("   Oppure 'web on/off', 'rag status'")
                    
            except KeyboardInterrupt:
                print("\n👋 Arrivederci!")
                break
            except Exception as e:
                print(f"⚠️ Errore: {e}")

if __name__ == "__main__":
    # Test con RAG
    try:
        club = ComedyClub(use_web_search=True)
        
        print("\n🧪 Test battuta singola:")
        joke = club.get_joke()
        print(joke)
        
        if club.enhanced_rag:
            print("\n🧪 Test con topic specifico:")
            joke_tech = club.get_joke(topic="technology")
            print(joke_tech)
        
    except Exception as e:
        print(f"⚠️ Errore: {e}")
        print("💡 Assicurati di aver eseguito: source config/set_env.sh")
        print("💡 Per RAG completo: python scripts/generate_embeddings.py")
