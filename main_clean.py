#!/usr/bin/env python3
"""
Comedy Club AI - Main Entry Point
Versione semplificata e funzionante
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
    parser = argparse.ArgumentParser(description='Comedy Club AI Simulator')
    parser.add_argument('--mode', choices=['interactive', 'show', 'test'], default='interactive',
                        help='Modalità di esecuzione')
    parser.add_argument('--mock', action='store_true',
                        help='Usa modalità mock (non si connette a Orfeo)')
    parser.add_argument('--rounds', type=int, default=2,
                        help='Numero di round per lo spettacolo')
    
    args = parser.parse_args()
    
    # Controlla configurazione Orfeo
    if not args.mock and not is_orfeo_available():
        print("⚠️ Configurazione Orfeo non trovata!")
        print(f"📡 Per usare Orfeo, esegui prima: {get_ssh_command()}")
        print("🧪 Uso modalità mock...")
        args.mock = True
    
    # Crea il comedy club
    club = ComedyClub(use_mock=args.mock)
    
    try:
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
            
    except KeyboardInterrupt:
        print("\n👋 Arrivederci!")
    except Exception as e:
        print(f"⚠️ Errore: {e}")

if __name__ == "__main__":
    main()
