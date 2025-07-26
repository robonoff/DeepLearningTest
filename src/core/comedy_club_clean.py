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
    
    def __init__(self, use_web_search: bool = True, use_rag: bool = True):
        """Inizializza il comedy club con supporto RAG opzionale"""
        
        if not is_orfeo_available():
            raise ValueError("⚠️ Token non configurato. Esegui: source config/set_env.sh")
        
        self.client = OrfeoClient()
        self.use_web_search = use_web_search
        
        # Inizializza sistema RAG se disponibile
        self.enhanced_rag = None
        # RAG Enhancement (opzionale)
        if use_rag:
            try:
                sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
                from src.utils.enhanced_joke_rag import EnhancedJokeRAG
                self.enhanced_rag = EnhancedJokeRAG()
                print("🧠 RAG system caricato per recupero intelligente jokes")
            except ImportError as e:
                print(f"⚠️ RAG non disponibile: {e}")
                self.enhanced_rag = None
            except Exception as e:
                print(f"⚠️ Errore caricamento RAG: {e}")
                self.enhanced_rag = None
        
        # Comedy Tools per ragionamento avanzato
        try:
            from src.utils.comedy_tools import ComedyTools
            self.comedy_tools = ComedyTools()
            print("🎭 Comedy Tools caricati per ragionamento avanzato")
        except ImportError as e:
            print(f"⚠️ Comedy Tools non disponibili: {e}")
            self.comedy_tools = None
        except Exception as e:
            print(f"⚠️ Errore caricamento Comedy Tools: {e}")
            self.comedy_tools = None
        
        # Sistema di Feedback per miglioramento iterativo
        try:
            from src.utils.comedy_feedback import ComedyFeedbackSystem
            self.feedback_system = ComedyFeedbackSystem()
            print("📊 Sistema di Feedback caricato per miglioramento iterativo")
        except ImportError as e:
            print(f"⚠️ Sistema di Feedback non disponibile: {e}")
            self.feedback_system = None
        except Exception as e:
            print(f"⚠️ Errore caricamento Sistema di Feedback: {e}")
            self.feedback_system = None
        
        self.comedians = {
            "Dave": {
                "name": "Dave",
                "style": "observational humor",
                "persona": "brutally honest social critic who exposes human hypocrisy",
                "catchphrases": ["You know what really pisses me off", "Let's be honest here", "Nobody wants to admit this but"],
                "tone": "edgy, unfiltered, provocative",
                "signature_style": "Takes normal situations and reveals the uncomfortable truth everyone ignores",
                "audience_connection": "Makes people laugh then feel guilty about laughing"
            },
            "Sarah": {
                "name": "Sarah", 
                "style": "wordplay and puns",
                "persona": "razor-sharp feminist comedian who weaponizes wit",
                "catchphrases": ["Men always say", "Dating apps are like", "My therapist says"],
                "tone": "sarcastic, intelligent, cutting",
                "signature_style": "Combines clever wordplay with savage social commentary",
                "audience_connection": "Makes women cheer and men nervous"
            },
            "Mike": {
                "name": "Mike",
                "style": "dark humor", 
                "persona": "everyman comedian who finds darkness in mundane life",
                "catchphrases": ["My wife thinks", "Kids today", "You know you're old when"],
                "tone": "relatable, dark, surprisingly deep",
                "signature_style": "Starts with normal family stuff then goes to unexpected dark places",
                "audience_connection": "Makes parents realize they're not alone in their dark thoughts"
            },
            "Lisa": {
                "name": "Lisa",
                "style": "absurd and surreal humor",
                "persona": "intellectually twisted comedian who makes smart people laugh uncomfortably", 
                "catchphrases": ["According to my research", "Scientifically speaking", "In my professional opinion"],
                "tone": "academic, weird, disturbingly logical",
                "signature_style": "Uses scientific facts and logic to reach completely insane conclusions",
                "audience_connection": "Makes educated people question their sanity"
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
    
        
    def get_joke(self, comedian_name=None, topic=None, enhanced_tv_search=False):
        """Get a joke from a comedian with RAG and advanced reasoning support
        
        Args:
            comedian_name: Name of the comedian
            topic: Topic for the joke
            enhanced_tv_search: Use specialized search for TV shows, memes, debates
        """
        
        comedian_name = comedian_name or random.choice(list(self.comedians.keys()))
        topic = topic or random.choice(self.topics)
        
        if comedian_name not in self.comedians:
            raise ValueError(f"⚠️ Comedian {comedian_name} not found!")
        
        comedian_info = self.comedians[comedian_name]
        
        # Use RAG enhanced if available and topic provided
        if self.enhanced_rag and topic:
            try:
                rag_result = self.enhanced_rag.retrieve_jokes_with_context(
                    comedian_info['style'], 
                    topic, 
                    use_web_search=self.use_web_search,
                    top_k=3,
                    enhanced_tv_search=enhanced_tv_search
                )
                
                sample_jokes = rag_result["jokes"]
                web_context = rag_result["web_context"]
                tv_meme_context = rag_result.get("tv_meme_context", {})
                
                # Use advanced reasoning system if available
                if self.comedy_tools:
                    comedy_prompt = self.comedy_tools.generate_comedy_prompt(
                        topic, comedian_info['style'], comedian_info, tv_meme_context
                    )
                    base_prompt = comedy_prompt
                    
                    # Add examples from dataset
                    if sample_jokes:
                        base_prompt += f"\n\nEXAMPLES FROM DATASET for inspiration:\n"
                        for i, joke in enumerate(sample_jokes[:2], 1):  # Only 2 examples to avoid overloading
                            base_prompt += f"{i}. {joke}\n"
                    
                    base_prompt += f"\nNow generate YOUR original joke about '{topic}' following the process above. RESPOND ONLY IN ENGLISH:"
                    
                else:
                    # Fallback to improved traditional prompt
                    base_prompt = f"You are {comedian_name}, a comedian with a {comedian_info['tone']} style. "
                    base_prompt += f"You specialize in {comedian_info['style']}. "
                    
                    # Add style examples from dataset
                    if sample_jokes:
                        base_prompt += f"Here are examples of your comedy style:\n"
                        for i, joke in enumerate(sample_jokes[:3], 1):
                            base_prompt += f"{i}. {joke}\n"
                        base_prompt += "\n"
                    
                    # Add characteristic phrases
                    if comedian_info.get('catchphrases'):
                        phrase = random.choice(comedian_info['catchphrases'])
                        base_prompt += f"Use your signature style (like '{phrase}...'). "
                    
                    base_prompt += f"Now create ONE short, funny joke about {topic}. "
                    base_prompt += "Keep it under 30 words. Make it genuinely hilarious and memorable. "
                    base_prompt += "RESPOND ONLY IN ENGLISH. "
                    
                    if web_context:
                        base_prompt += f"Current context: {web_context[:150]}. "
                        
                    base_prompt += f"\nTopic: {topic}\nYour joke:"
                
                print(f"🎤 {comedian_name} sta raccontando una battuta su {topic} (con RAG)...")
                response = self.client.generate(base_prompt, max_tokens=200)
                
                # Valuta la qualità della battuta se gli strumenti sono disponibili
                if self.comedy_tools and response:
                    analysis = self.comedy_tools.analyze_joke_quality(response)
                    print(f"🎯 Qualità battuta: {analysis.overall_score:.2f}/1.0")
                    print(f"   Tipo: {analysis.humor_type}")
                    print(f"   Setup: {analysis.setup_strength:.2f}, Punchline: {analysis.punchline_impact:.2f}")
                    
                    # Sistema di feedback per apprendimento
                    if self.feedback_system:
                        feedback = self.feedback_system.provide_feedback(response, comedian_name, topic, analysis)
                        print(f"👥 Reazione pubblico: {feedback.audience_score:.2f}/1.0")
                        if feedback.feedback_notes:
                            print(f"💡 {feedback.feedback_notes[0]}")  # Mostra solo il primo feedback
                    
                    # Se la qualità è bassa, suggerisci miglioramenti
                    if analysis.overall_score < 0.6:
                        suggestions = self.comedy_tools.suggest_improvements(response, analysis)
                        print(f"� Suggerimenti: {', '.join(suggestions[:2])}")
                
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
        
        # Valuta la qualità anche nel fallback
        if self.comedy_tools and response:
            analysis = self.comedy_tools.analyze_joke_quality(response)
            print(f"🎯 Qualità battuta: {analysis.overall_score:.2f}/1.0 (fallback)")
        
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
        
        # Mostra statistiche se disponibili
        if self.feedback_system:
            print("\n📊 STATISTICHE DELLA SERATA:")
            top_performers = self.feedback_system.get_top_performers()
            for i, performer in enumerate(top_performers, 1):
                print(f"   {i}° {performer['comedian']}: {performer['average_score']:.2f}/1.0 "
                      f"({performer['performances']} performance)")

    def show_comedian_stats(self, comedian_name: str = None):
        """Mostra statistiche dettagliate di un comico"""
        if not self.feedback_system:
            print("⚠️ Sistema di feedback non disponibile")
            return
        
        if comedian_name:
            stats = self.feedback_system.get_comedian_stats(comedian_name)
            print(f"\n📊 STATISTICHE - {comedian_name.upper()}")
            print("-" * 40)
            
            if "message" in stats:
                print(f"   {stats['message']}")
            else:
                print(f"   Performance totali: {stats['total_performances']}")
                print(f"   Qualità media: {stats['average_quality']:.2f}/1.0")
                print(f"   Gradimento pubblico: {stats['average_audience_score']:.2f}/1.0")
                print(f"   Miglior battuta: {stats['best_joke'][:80]}...")
                print(f"   Topic preferito: {stats['best_topic']}")
                print(f"   Trend: {stats['improvement_trend']}")
        else:
            # Mostra classifica generale
            print("\n🏆 CLASSIFICA GENERALE COMICI")
            print("-" * 40)
            top_performers = self.feedback_system.get_top_performers(len(self.comedians))
            for i, performer in enumerate(top_performers, 1):
                print(f"   {i}° {performer['comedian']}: {performer['average_score']:.2f}/1.0 "
                      f"({performer['performances']} performance)")

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
        if self.feedback_system:
            print("  - 'stats' per classifica generale")
            print("  - 'stats nome_comico' per statistiche specifiche")
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
