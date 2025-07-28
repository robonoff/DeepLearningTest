#!/usr/bin/env python3
"""
Script migliorato per categorizzare e preparare jokes dal dataset
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import json
import random

def categorize_jokes_improved():
    """Categorizza i jokes dal CSV usando criteri migliorati"""
    print("🔧 Categorizzazione migliorata dei jokes...")
    
    # Carica il dataset
    df = pd.read_csv('datasets/shortjokes.csv')
    print(f"📊 Dataset caricato: {len(df)} jokes")
    
    # Categorie migliorate con parole chiave più specifiche
    categories = {
        "observational humor": {
            "keywords": ["ever notice", "what's the deal", "why do we", "have you ever", 
                        "you know what", "isn't it weird", "why is it", "anyone else", 
                        "facebook", "social media", "phone", "technology", "work", "monday"],
            "jokes": []
        },
        "dark humor": {
            "keywords": ["death", "died", "kill", "murder", "suicide", "funeral", "grave", 
                        "dead", "corpse", "hell", "devil", "depression", "divorce", "ex"],
            "jokes": []
        },
        "wordplay and puns": {
            "keywords": ["pun", "sounds like", "spell", "word", "letter", "grammar",
                        "why did", "what do you call", "knock knock", "play on words"],
            "jokes": []
        },
        "absurd and surreal humor": {
            "keywords": ["alien", "space", "weird", "strange", "random", "wtf", "bizarre",
                        "surreal", "unicorn", "dragon", "magic", "impossible", "stupid"],
            "jokes": []
        }
    }
    
    # Categorizza jokes (prendi campioni bilanciati)
    sample_size = 50  # Più esempi per categoria
    
    for joke_text in df['Joke'].dropna().sample(n=min(5000, len(df))):  # Campiona per performance
        joke_lower = str(joke_text).lower()
        
        # Skip jokes troppo lunghe o inappropriate
        if len(joke_text) > 200 or len(joke_text) < 10:
            continue
            
        categorized = False
        for category, data in categories.items():
            if any(keyword in joke_lower for keyword in data["keywords"]):
                if len(data["jokes"]) < sample_size:
                    data["jokes"].append(joke_text)
                    categorized = True
                    break
        
        # Se non categorizzato, aggiungi agli osservazionali
        if not categorized and len(categories["observational humor"]["jokes"]) < sample_size:
            categories["observational humor"]["jokes"].append(joke_text)
    
    # Rimuovi le keywords e mantieni solo i jokes
    clean_categories = {}
    for category, data in categories.items():
        clean_categories[category] = data["jokes"]
        print(f"   {category}: {len(data['jokes'])} jokes")
    
    # Salva
    with open('logs/categorized_jokes.json', 'w', encoding='utf-8') as f:
        json.dump(clean_categories, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Categorizzazione completata! Total jokes: {sum(len(jokes) for jokes in clean_categories.values())}")
    return clean_categories

if __name__ == "__main__":
    categorize_jokes_improved()
