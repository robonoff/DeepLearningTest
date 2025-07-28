#!/usr/bin/env python3
"""
Script per generare embeddings dai jokes esistenti
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json

def generate_joke_embeddings():
    """One-time preprocessing to generate embeddings for all jokes"""
    print("🔧 Generazione embeddings per i jokes...")
    
    try:
        from sentence_transformers import SentenceTransformer
    except ImportError:
        print("❌ sentence-transformers non installato. Esegui: pip install sentence-transformers")
        return False
    
    # Controlla se esiste il file dei jokes categorizzati
    jokes_file = 'logs/categorized_jokes.json'
    if not os.path.exists(jokes_file):
        print(f"⚠️ File {jokes_file} non trovato. Creo dei jokes di esempio...")
        create_example_jokes()
    
    # Carica i jokes esistenti
    with open(jokes_file, 'r', encoding='utf-8') as f:
        jokes_data = json.load(f)
    
    print(f"📊 Caricati {sum(len(jokes) for jokes in jokes_data.values())} jokes")
    
    # Inizializza il modello
    print("🧠 Caricamento modello sentence-transformers...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    enhanced_data = {}
    total_jokes = 0
    
    for category, jokes in jokes_data.items():
        print(f"   Processando categoria: {category} ({len(jokes)} jokes)")
        enhanced_data[category] = []
        
        for joke in jokes:
            try:
                embedding = model.encode([joke])[0].tolist()
                enhanced_data[category].append({
                    "text": joke,
                    "embedding": embedding,
                    "category": category
                })
                total_jokes += 1
            except Exception as e:
                print(f"⚠️ Errore processando joke: {e}")
                continue
    
    # Salva i dati con embeddings
    output_file = 'logs/categorized_jokes_with_embeddings.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(enhanced_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Generati embeddings per {total_jokes} jokes")
    print(f"💾 Salvati in: {output_file}")
    return True

def create_example_jokes():
    """Crea un set di jokes di esempio se non esiste il file"""
    example_jokes = {
        "observational humor": [
            "What's the deal with people who say 'money can't buy happiness'? Have they seen the smile on someone's face at the Apple Store?",
            "I love how we call it 'fast food' when it takes 20 minutes in the drive-through. That's like calling traffic a 'moving experience'.",
            "Social media is like that friend who never stops talking about themselves. Except now there's a like button."
        ],
        "dark humor": [
            "I told my wife she was drawing her eyebrows too high. She looked surprised.",
            "My therapist says I have a preoccupation with vengeance. We'll see about that.",
            "I have a lot of growing up to do. I realized that the other day inside my fort."
        ],
        "wordplay and puns": [
            "I wondered why the baseball kept getting bigger. Then it hit me.",
            "Did you hear about the mathematician who's afraid of negative numbers? He'll stop at nothing to avoid them.",
            "I used to hate facial hair, but then it grew on me."
        ],
        "absurd and surreal humor": [
            "I bought a thesaurus yesterday, but when I got home I discovered all the pages were blank. I have no words to describe how angry I am.",
            "My dog is a magician. He's a labracadabrador.",
            "I told my cat a joke about dogs, but he didn't find it a-mew-sing."
        ]
    }
    
    os.makedirs('logs', exist_ok=True)
    with open('logs/categorized_jokes.json', 'w', encoding='utf-8') as f:
        json.dump(example_jokes, f, indent=2, ensure_ascii=False)
    
    print("📝 Creato file di esempio con jokes categorizzati")

if __name__ == "__main__":
    success = generate_joke_embeddings()
    sys.exit(0 if success else 1)
