#!/usr/bin/env python3
"""
Script per generare embeddings dal dataset integrato (Jester + ShortJokes)
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
from pathlib import Path

def generate_integrated_embeddings():
    """Genera embeddings per il dataset integrato"""
    print("🔧 Generazione embeddings per il dataset integrato...")
    
    try:
        from sentence_transformers import SentenceTransformer
        import numpy as np
    except ImportError:
        print("❌ sentence-transformers non installato. Esegui: pip install sentence-transformers")
        return False
    
    base_dir = Path(__file__).parent.parent
    
    # Controlla se esiste il dataset integrato
    integrated_file = base_dir / 'datasets' / 'integrated_jokes_dataset.json'
    if not integrated_file.exists():
        print(f"⚠️ Dataset integrato non trovato in {integrated_file}")
        print("Esegui prima: python scripts/integrate_jester_dataset.py")
        return False
    
    # Carica il dataset integrato
    with open(integrated_file, 'r', encoding='utf-8') as f:
        jokes_data = json.load(f)
    
    total_jokes = sum(len(jokes) for jokes in jokes_data.values())
    print(f"📊 Caricati {total_jokes} jokes dal dataset integrato")
    
    # Inizializza il modello
    print("🧠 Caricamento modello sentence-transformers...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    enhanced_data = {}
    processed_jokes = 0
    
    for category, jokes in jokes_data.items():
        print(f"   Processando categoria: {category} ({len(jokes)} jokes)")
        enhanced_data[category] = []
        
        # Prepara tutti i testi per l'encoding batch
        joke_texts = []
        joke_metadata = []
        
        for joke_item in jokes:
            if isinstance(joke_item, dict):
                joke_text = joke_item.get('text', '')
                source = joke_item.get('source', 'unknown')
            else:
                joke_text = str(joke_item)
                source = 'legacy'
            
            if joke_text and len(joke_text.strip()) > 5:
                joke_texts.append(joke_text)
                joke_metadata.append({
                    'text': joke_text,
                    'source': source,
                    'category': category
                })
        
        if joke_texts:
            # Genera embeddings in batch per efficienza
            print(f"     Generando embeddings per {len(joke_texts)} jokes...")
            embeddings = model.encode(joke_texts, show_progress_bar=True)
            
            # Combina testi, metadati ed embeddings
            for i, (metadata, embedding) in enumerate(zip(joke_metadata, embeddings)):
                enhanced_data[category].append({
                    "text": metadata['text'],
                    "embedding": embedding.tolist(),
                    "category": category,
                    "source": metadata['source'],
                    "id": f"{category}_{i}"
                })
                processed_jokes += 1
    
    print(f"✅ Processati {processed_jokes} jokes con embeddings")
    
    # Salva i dati con embeddings
    output_file = base_dir / 'datasets' / 'integrated_jokes_with_embeddings.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(enhanced_data, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Embeddings salvati in: {output_file}")
    
    # Crea un link simbolico per compatibilità con il sistema esistente
    legacy_link = base_dir / 'logs' / 'categorized_jokes_with_embeddings.json'
    if legacy_link.exists():
        legacy_link.unlink()
    
    try:
        legacy_link.symlink_to(output_file.relative_to(base_dir))
        print(f"🔗 Creato link simbolico: {legacy_link}")
    except Exception as e:
        print(f"⚠️ Non riesco a creare link simbolico: {e}")
        # Copia il file invece
        import shutil
        shutil.copy2(output_file, legacy_link)
        print(f"📋 Copiato file per compatibilità: {legacy_link}")
    
    # Statistiche finali
    print("\n📈 Statistiche dataset integrato:")
    for category, jokes in enhanced_data.items():
        sources = {}
        for joke in jokes:
            source = joke.get('source', 'unknown')
            sources[source] = sources.get(source, 0) + 1
        
        print(f"  {category}: {len(jokes)} jokes")
        for source, count in sources.items():
            print(f"    - {source}: {count}")
    
    return True

def create_example_jokes():
    """Crea jokes di esempio se non esistono"""
    base_dir = Path(__file__).parent.parent
    jokes_file = base_dir / 'logs' / 'categorized_jokes.json'
    
    example_jokes = {
        "observational": [
            "Have you ever noticed that anyone driving slower than you is an idiot, and anyone going faster than you is a maniac?",
            "Why do they call it rush hour when nobody's moving?",
            "Ever wonder why they call it a TV set when you only get one?"
        ],
        "wordplay": [
            "I told my wife she was drawing her eyebrows too high. She looked surprised.",
            "Why don't scientists trust atoms? Because they make up everything!",
            "I used to be a banker, but I lost interest."
        ],
        "storytelling": [
            "A man walks into a library and asks for books on paranoia. The librarian whispers, 'They're right behind you!'",
            "Two fish are sitting in a tank. One looks at the other and says, 'Do you know how to drive this thing?'"
        ],
        "absurd": [
            "What if soy milk is just regular milk introducing itself in Spanish?",
            "Time travel is possible. I just went forward in time by reading this sentence.",
            "My pet snake is great at math. It's an adder."
        ]
    }
    
    os.makedirs(jokes_file.parent, exist_ok=True)
    with open(jokes_file, 'w', encoding='utf-8') as f:
        json.dump(example_jokes, f, indent=2, ensure_ascii=False)
    
    print(f"📝 Creati jokes di esempio in: {jokes_file}")

if __name__ == "__main__":
    print("🎭 Generazione embeddings dataset integrato")
    print("=" * 50)
    
    try:
        success = generate_integrated_embeddings()
        if success:
            print("\n🎉 Embeddings generati con successo!")
            print("Il sistema RAG è ora pronto per utilizzare il dataset integrato Jester + ShortJokes")
        else:
            print("\n❌ Errore nella generazione degli embeddings")
    except Exception as e:
        print(f"❌ Errore imprevisto: {e}")
        import traceback
        traceback.print_exc()
