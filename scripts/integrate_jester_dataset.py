#!/usr/bin/env python3
"""
Script per integrare il dataset Jester con il sistema RAG esistente
Combina shortjokes.csv e jester_items.csv per creare un dataset completo
"""

import pandas as pd
import json
import re
import os
from pathlib import Path

def clean_joke_text(text):
    """Pulisce il testo delle battute"""
    if pd.isna(text):
        return ""
    
    # Rimuove caratteri di escape e newline multipli
    text = text.replace('\\n', ' ').replace('\n', ' ')
    text = text.replace('\\"', '"').replace("\\'", "'")
    
    # Rimuove spazi multipli
    text = re.sub(r'\s+', ' ', text)
    
    # Rimuove virgolette all'inizio e fine se presenti
    text = text.strip().strip('"').strip("'")
    
    return text.strip()

def categorize_joke_by_content(joke_text):
    """Categorizza una battuta basandosi sul contenuto"""
    joke_lower = joke_text.lower()
    
    # Keywords per ogni categoria
    observational_keywords = [
        'have you ever noticed', 'why do', 'what\'s the deal', 'ever wonder',
        'isn\'t it funny', 'you know what', 'speaking of', 'the other day'
    ]
    
    wordplay_keywords = [
        'pun', 'what do you call', 'why did', 'knock knock', 'what\'s the difference',
        'how many', 'what do you get when', 'why doesn\'t', 'why can\'t'
    ]
    
    absurd_keywords = [
        'aliens', 'time travel', 'parallel universe', 'dimension', 'quantum',
        'what if', 'imagine if', 'in an alternate', 'cosmic', 'universe'
    ]
    
    # Conteggio delle keywords per categoria
    observational_count = sum(1 for keyword in observational_keywords if keyword in joke_lower)
    wordplay_count = sum(1 for keyword in wordplay_keywords if keyword in joke_lower)
    absurd_count = sum(1 for keyword in absurd_keywords if keyword in joke_lower)
    
    # Classificazione basata su contenuto e struttura
    if any(keyword in joke_lower for keyword in wordplay_keywords):
        return "wordplay"
    elif any(keyword in joke_lower for keyword in observational_keywords):
        return "observational"
    elif any(keyword in joke_lower for keyword in absurd_keywords):
        return "absurd"
    elif 'q:' in joke_lower and 'a:' in joke_lower:
        return "wordplay"
    elif '?' in joke_text and len(joke_text.split('?')) >= 2:
        return "wordplay"
    elif len(joke_text.split()) > 50:  # Battute lunghe tendono ad essere narrative
        return "storytelling"
    else:
        return "observational"  # Default

def integrate_datasets():
    """Integra i dataset shortjokes e jester_items"""
    base_dir = Path(__file__).parent.parent
    datasets_dir = base_dir / "datasets"
    
    print("📚 Caricamento dei dataset...")
    
    # Carica shortjokes.csv
    shortjokes_path = datasets_dir / "shortjokes.csv"
    if shortjokes_path.exists():
        print(f"Caricamento shortjokes da: {shortjokes_path}")
        shortjokes_df = pd.read_csv(shortjokes_path)
        print(f"Trovate {len(shortjokes_df)} battute in shortjokes")
    else:
        print("⚠️ shortjokes.csv non trovato, creo dataset vuoto")
        shortjokes_df = pd.DataFrame(columns=['Joke'])
    
    # Carica jester_items.csv
    jester_path = datasets_dir / "jester_items.csv"
    if jester_path.exists():
        print(f"Caricamento jester_items da: {jester_path}")
        jester_df = pd.read_csv(jester_path)
        print(f"Trovate {len(jester_df)} battute in jester_items")
    else:
        print("❌ jester_items.csv non trovato!")
        return
    
    # Prepara i dati in formato uniforme
    combined_jokes = []
    
    # Aggiungi battute da shortjokes
    if not shortjokes_df.empty:
        for _, row in shortjokes_df.iterrows():
            joke_text = clean_joke_text(str(row['Joke']))
            if joke_text and len(joke_text.strip()) > 10:  # Filtra battute troppo corte
                combined_jokes.append({
                    'text': joke_text,
                    'source': 'shortjokes',
                    'category': categorize_joke_by_content(joke_text)
                })
    
    # Aggiungi battute da jester_items
    for _, row in jester_df.iterrows():
        joke_text = clean_joke_text(str(row['jokeText']))
        if joke_text and len(joke_text.strip()) > 10:  # Filtra battute troppo corte
            combined_jokes.append({
                'text': joke_text,
                'source': 'jester',
                'category': categorize_joke_by_content(joke_text)
            })
    
    print(f"📊 Totale battute combinate: {len(combined_jokes)}")
    
    # Conta per categoria
    category_counts = {}
    for joke in combined_jokes:
        category = joke['category']
        category_counts[category] = category_counts.get(category, 0) + 1
    
    print("📈 Distribuzione per categoria:")
    for category, count in sorted(category_counts.items()):
        print(f"  {category}: {count} battute")
    
    # Seleziona le migliori battute per categoria (max 100 per categoria)
    categorized_jokes = {
        'observational': [],
        'wordplay': [],
        'storytelling': [],
        'absurd': []
    }
    
    # Distribuisci le battute per categoria
    for joke in combined_jokes:
        category = joke['category']
        if category in categorized_jokes and len(categorized_jokes[category]) < 100:
            categorized_jokes[category].append(joke)
    
    # Se una categoria ha poche battute, riempila con battute di altre categorie
    min_jokes_per_category = 50
    for category in categorized_jokes:
        while len(categorized_jokes[category]) < min_jokes_per_category and len(combined_jokes) > 0:
            # Trova una battuta non ancora usata
            for joke in combined_jokes:
                if joke not in [j for cat_jokes in categorized_jokes.values() for j in cat_jokes]:
                    categorized_jokes[category].append(joke)
                    break
            else:
                break
    
    print("\n📝 Battute selezionate per categoria:")
    for category, jokes in categorized_jokes.items():
        print(f"  {category}: {len(jokes)} battute")
    
    # Salva il dataset combinato
    output_file = datasets_dir / "integrated_jokes_dataset.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(categorized_jokes, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Dataset integrato salvato in: {output_file}")
    
    # Crea anche un file CSV per compatibilità
    csv_output = datasets_dir / "integrated_jokes.csv"
    all_jokes_for_csv = []
    for category, jokes in categorized_jokes.items():
        for joke in jokes:
            all_jokes_for_csv.append({
                'text': joke['text'],
                'category': category,
                'source': joke['source']
            })
    
    df_output = pd.DataFrame(all_jokes_for_csv)
    df_output.to_csv(csv_output, index=False, encoding='utf-8')
    print(f"✅ Dataset CSV salvato in: {csv_output}")
    
    return categorized_jokes

if __name__ == "__main__":
    print("🎭 Integrazione dataset Jester con sistema RAG")
    print("=" * 50)
    
    try:
        jokes_data = integrate_datasets()
        print("\n🎉 Integrazione completata con successo!")
        print(f"Totale battute integrate: {sum(len(jokes) for jokes in jokes_data.values())}")
        
    except Exception as e:
        print(f"❌ Errore durante l'integrazione: {e}")
        import traceback
        traceback.print_exc()
