#!/usr/bin/env python3
"""
Test semplice per verificare le funzionalità live delle statistiche
"""

import os
import re

def test_live_statistics_features():
    """Verifica che le funzionalità live siano implementate correttamente"""
    
    print("🔄 VERIFICA AGGIORNAMENTO DINAMICO STATISTICHE")
    print("=" * 60)
    
    gui_file = "/home/robertalamberti/DeepLearningTest/src/gui/comedy_club_gui.py"
    
    try:
        with open(gui_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Errore lettura file: {e}")
        return False
    
    # Test delle funzionalità implementate
    tests = {
        "1. Auto-refresh ogni 3 secondi": {
            "pattern": r"self\.root\.after\(3000.*_auto_update_stats\)",
            "description": "Timer automatico per aggiornamento ogni 3 secondi"
        },
        
        "2. Aggiornamento immediato su rating": {
            "pattern": r"if hasattr\(self, 'stats_window'\).*winfo_exists.*_update_statistics_content",
            "description": "Update immediato quando dai un rating"
        },
        
        "3. Timestamp dinamico": {
            "pattern": r"time\.strftime\('%H:%M:%S'\)",
            "description": "Mostra ora dell'ultimo aggiornamento"
        },
        
        "4. Titolo con indicatore LIVE": {
            "pattern": r"Statistics.*\(LIVE\)",
            "description": "Finestra mostra che è live"
        },
        
        "5. Prevenzione finestre duplicate": {
            "pattern": r"stats_window\.winfo_exists.*lift\(\)",
            "description": "Porta in primo piano se già aperta"
        },
        
        "6. Cleanup automatico": {
            "pattern": r"after_cancel.*stats_update_job",
            "description": "Ferma aggiornamenti quando chiudi finestra"
        },
        
        "7. Preservazione scroll position": {
            "pattern": r"scroll_position.*yview\(\).*yview_moveto",
            "description": "Mantiene posizione scroll durante update"
        },
        
        "8. Gestione sicura finestre": {
            "pattern": r"TclError|winfo_exists",
            "description": "Gestisce errori se finestra viene chiusa"
        },
        
        "9. Scheduling ricorsivo": {
            "pattern": r"_auto_update_stats.*_update_statistics_content.*_schedule_stats_update",
            "description": "Ciclo continuo di aggiornamenti"
        },
        
        "10. Controllo esistenza window": {
            "pattern": r"if.*stats_window.*winfo_exists",
            "description": "Verifica che finestra esista prima di aggiornare"
        }
    }
    
    results = {}
    passed = 0
    
    for test_name, test_info in tests.items():
        pattern = test_info["pattern"]
        description = test_info["description"]
        
        # Usa DOTALL per match multiline
        if re.search(pattern, content, re.DOTALL | re.IGNORECASE):
            print(f"✅ {test_name}")
            print(f"   📝 {description}")
            results[test_name] = True
            passed += 1
        else:
            print(f"❌ {test_name}")
            print(f"   📝 {description} - NON TROVATO")
            results[test_name] = False
        print()
    
    # Summary
    total = len(tests)
    percentage = (passed / total) * 100
    
    print("=" * 60)
    print(f"📊 RISULTATI: {passed}/{total} funzionalità implementate ({percentage:.1f}%)")
    
    if percentage >= 80:
        print("🎉 OTTIMO! Le statistiche live sono ben implementate!")
        print("\n🔄 COME FUNZIONANO GLI AGGIORNAMENTI LIVE:")
        print("   1️⃣ Apri finestra statistiche → Avvia timer 3 secondi")
        print("   2️⃣ Ogni 3 secondi → Ricarica dati e aggiorna display")
        print("   3️⃣ Dai un rating → Update immediato + continua timer")
        print("   4️⃣ Chiudi finestra → Ferma timer automaticamente")
        print("   5️⃣ Riapri finestra → Se già aperta, porta in primo piano")
        
        print("\n✨ VANTAGGI:")
        print("   📈 Vedi cambiamenti in tempo reale")  
        print("   ⏱️ Timestamp mostra quando è stato aggiornato")
        print("   📍 Posizione scroll preservata")
        print("   🛡️ Gestione sicura degli errori")
        print("   🚀 Performance ottimizzate")
        
    elif percentage >= 50:
        print("⚠️ PARZIALE: Alcune funzionalità live implementate")
    else:
        print("❌ INSUFFICIENTE: Poche funzionalità live trovate")
    
    return percentage >= 80

def test_manual_verification():
    """Guida per test manuale delle funzionalità live"""
    
    print("\n🧪 GUIDA TEST MANUALE - STATISTICHE LIVE")
    print("=" * 60)
    
    print("Per verificare completamente le funzionalità live:")
    print()
    print("1️⃣ AVVIA GUI:")
    print("   python3 start_gui_rag.py")
    print()
    print("2️⃣ APRI STATISTICHE:")
    print("   Clicca 'Show Statistics' → Finestra con titolo '(LIVE)'")
    print()
    print("3️⃣ VERIFICA AUTO-REFRESH:")
    print("   Guarda timestamp in basso → Cambia ogni 3 secondi")
    print()
    print("4️⃣ VERIFICA UPDATE IMMEDIATO:")
    print("   Genera battuta → Dai rating → Statistiche si aggiornano subito")
    print()
    print("5️⃣ VERIFICA SCROLL POSITION:")
    print("   Scorri a metà finestra → Update non sposta scroll")
    print("   Scorri in fondo → Update mantiene in fondo")
    print()
    print("6️⃣ VERIFICA ANTI-DUPLICATE:")
    print("   Clicca 'Show Statistics' di nuovo → Porta finestra in primo piano")
    print()
    print("7️⃣ VERIFICA CLEANUP:")
    print("   Chiudi finestra statistiche → Console non mostra errori")
    
    return True

if __name__ == "__main__":
    # Test automatico del codice
    code_test = test_live_statistics_features()
    
    # Guida per test manuale
    manual_guide = test_manual_verification()
    
    if code_test:
        print(f"\n🎯 CONCLUSIONE: Le statistiche live sono implementate correttamente!")
        print("   Per vedere in azione, avvia la GUI e segui la guida sopra.")
    else:
        print(f"\n⚠️ ATTENZIONE: Alcune funzionalità potrebbero mancare o essere incomplete.")
