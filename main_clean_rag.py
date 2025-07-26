#!/usr/bin/env python3
"""
Comedy Club AI - Modalità Orfeo con RAG Enhancement
"""

import argparse
import sys
import os

# Aggiungi src al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
sys.path.append(os.path.dirname(__file__))

from src.core.comedy_club_clean import ComedyClub
from config.orfeo_config_new import get_ssh_command, is_orfeo_available

def main():
    parser = argparse.ArgumentParser(description='Comedy Club AI con Orfeo + RAG')
    parser.add_argument('--mode', choices=['interactive', 'show', 'test', 'joke'], default='interactive',
                        help='Modalità di esecuzione')
    parser.add_argument('--rounds', type=int, default=2,
                        help='Numero di round per lo spettacolo')
    parser.add_argument('--comedian', 
                        help='Comico specifico (Jerry, Penny, Raven, Cosmic)')
    parser.add_argument('--topic', 
                        help='Topic specifico per la battuta')
    parser.add_argument('--no-web-search', action='store_true',
                        help='Disabilita ricerca web per contesto attuale')
    parser.add_argument('--offline', action='store_true',
                        help='Disabilita tutte le funzionalità web (equivale a --no-web-search)')
    
    args = parser.parse_args()
    
    # Controlla configurazione Orfeo
    if not is_orfeo_available():
        print("❌ Configurazione Orfeo non trovata!")
        print(f"💡 Esegui prima: source config/set_env.sh")
        print(f"📡 Poi assicurati che sia attivo: {get_ssh_command()}")
        return 1
    
    try:
        # Determina impostazioni web search (default: True, disabilita con --no-web-search o --offline)
        use_web_search = not (args.offline or args.no_web_search)
        
        # Crea il comedy club con configurazione RAG
        club = ComedyClub(use_web_search=use_web_search)
        
        print(f"🌐 Web search: {'✅ Abilitato' if use_web_search else '❌ Disabilitato'}")
        
        if args.mode == 'interactive':
            print("\n🎭 Avvio modalità interattiva...")
            club.interactive_mode()
            
        elif args.mode == 'show':
            print(f"\n🎪 Avvio spettacolo di {args.rounds} round...")
            club.run_show(args.rounds)
            
        elif args.mode == 'test':
            print("\n🧪 Modalità test - battuta singola:")
            joke = club.get_joke()
            print(f"🎤 {joke}")
            
        elif args.mode == 'joke':
            print("\n🎤 Generazione battuta specifica:")
            joke = club.get_joke(comedian_name=args.comedian, topic=args.topic)
            print(f"🎤 {joke}")
            
    except KeyboardInterrupt:
        print("\n👋 Arrivederci!")
    except Exception as e:
        print(f"❌ Errore: {e}")
        print("💡 Controlla che:")
        print("   1. Hai eseguito: source config/set_env.sh")
        print("   2. Il port forwarding SSH è attivo")
        print("   3. Orfeo è raggiungibile")
        print("   4. Per RAG: python scripts/generate_embeddings.py")
        return 1

if __name__ == "__main__":
    exit(main() or 0)
