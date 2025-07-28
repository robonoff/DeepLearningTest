#!/usr/bin/env python3
"""
Launcher per la GUI Comedy Club con supporto RAG
"""

import sys
import os

# Aggiungi src al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
sys.path.append(os.path.dirname(__file__))

try:
    import tkinter as tk
    from src.gui.comedy_club_gui import ComedyClubGUI
    from config.orfeo_config_new import is_orfeo_available
    
    def main():
        # Verifica configurazione Orfeo
        if not is_orfeo_available():
            print("❌ Configurazione Orfeo non trovata!")
            print("💡 Esegui prima: source config/set_env.sh")
            return 1
        
        print("🎭 Avvio Comedy Club GUI - Modalità Completa...")
        print("   ✅ RAG: ATTIVO per battute intelligenti")
        print("   ✅ Web Search: ATTIVO per contenuti freschi")
        print("   ✅ Rating System: Attivo per apprendimento")
        print("   🎪 GUI: Interfaccia visuale completa")
        
        # Crea e avvia la GUI
        root = tk.Tk()
        app = ComedyClubGUI(root)
        
        # Aggiungi informazioni RAG al titolo
        root.title("🎭 AI Comedy Club Simulation - RAG Enhanced")
        
        print("🚀 GUI avviata! Usa i controlli RAG per personalizzare l'esperienza.")
        root.mainloop()
        
        return 0
    
    if __name__ == "__main__":
        exit(main())
        
except ImportError as e:
    print(f"❌ Errore import: {e}")
    print("💡 Installa tkinter: sudo apt-get install python3-tk")
    sys.exit(1)
except Exception as e:
    print(f"❌ Errore: {e}")
    sys.exit(1)
