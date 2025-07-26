#!/usr/bin/env python3
"""
Enhanced Joke RAG system per Comedy Club con integrazione Orfeo
"""

import numpy as np
import json
import time
import os
from typing import List, Dict, Optional

class EnhancedJokeRAG:
    """Sistema RAG per recupero intelligente di jokes con ricerca web"""
    
    def __init__(self, jokes_file: str = "logs/categorized_jokes_with_embeddings.json"):
        self.jokes_file = jokes_file
        self.jokes_data = self._load_jokes_with_embeddings()
        self.search_cache = {}
        self.model = None
        self._init_model()
        
    def _init_model(self):
        """Inizializza il modello sentence transformer"""
        try:
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
            print("🧠 Modello RAG inizializzato")
        except ImportError:
            print("⚠️ sentence-transformers non disponibile. Installa: pip install sentence-transformers")
            self.model = None
        except Exception as e:
            print(f"⚠️ Errore inizializzazione modello RAG: {e}")
            self.model = None
        
    def _load_jokes_with_embeddings(self):
        """Carica jokes con embeddings"""
        if not os.path.exists(self.jokes_file):
            print(f"⚠️ {self.jokes_file} non trovato. Esegui: python scripts/generate_embeddings.py")
            return {}
        
        try:
            with open(self.jokes_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️ Errore caricamento jokes: {e}")
            return {}
    
    def retrieve_jokes_with_context(self, humor_style: str, topic: str, 
                                  use_web_search: bool = True, top_k: int = 3) -> Dict:
        """Enhanced retrieval con contesto web"""
        if not self.model or not self.jokes_data:
            return {
                "jokes": [],
                "web_context": "",
                "enhanced_query": f"{humor_style} about {topic}",
                "timestamp": time.time(),
                "status": "RAG not available"
            }
        
        # Ottieni contesto web se richiesto
        web_context = ""
        if use_web_search:
            web_context = self._search_current_context(topic)
        
        # Crea query migliorata
        enhanced_query = self._create_enhanced_query(humor_style, topic, web_context)
        
        # Recupera jokes rilevanti
        relevant_jokes = self._similarity_search(enhanced_query, top_k)
        
        return {
            "jokes": relevant_jokes,
            "web_context": web_context,
            "enhanced_query": enhanced_query,
            "timestamp": time.time(),
            "status": "success"
        }
    
    def _search_current_context(self, topic: str, max_results: int = 3) -> str:
        """Ricerca informazioni attuali sul topic"""
        cache_key = f"search_{topic}_{int(time.time() // 3600)}"
        if cache_key in self.search_cache:
            return self.search_cache[cache_key]
        
        try:
            from duckduckgo_search import DDGS
            
            with DDGS() as ddgs:
                search_query = f"{topic} news recent trends 2025"
                results = list(ddgs.text(search_query, max_results=max_results))
                
                context_snippets = []
                for result in results:
                    title = result.get('title', '')
                    body = result.get('body', '')[:200]
                    snippet = f"Recent: {title} - {body}..."
                    context_snippets.append(snippet)
                
                web_context = " | ".join(context_snippets)
                self.search_cache[cache_key] = web_context
                print(f"🌐 Contesto web recuperato per '{topic}': {len(web_context)} caratteri")
                return web_context
                
        except ImportError:
            print("⚠️ duckduckgo-search non installato. Esegui: pip install duckduckgo-search")
            return ""
        except Exception as e:
            print(f"⚠️ Ricerca web fallita: {e}")
            return ""
    
    def _create_enhanced_query(self, humor_style: str, topic: str, web_context: str) -> str:
        """Crea query di ricerca migliorata con contesto web"""
        style_descriptors = {
            "observational humor": "everyday situation, relatable, 'what's the deal with'",
            "dark humor": "dark humor, twisted, sarcastic, edgy",
            "wordplay and puns": "puns, word games, linguistic humor, clever words",
            "absurd and surreal humor": "weird, unexpected, surreal, random, bizarre"
        }
        
        base_query = f"{style_descriptors.get(humor_style, humor_style)} about {topic}"
        
        if web_context:
            enhanced_query = f"{base_query}. Current context: {web_context[:300]}"
            return enhanced_query
        
        return base_query
    
    def _similarity_search(self, query: str, top_k: int) -> List[str]:
        """Trova jokes più simili usando cosine similarity"""
        if not self.model or not self.jokes_data:
            return []
        
        try:
            from sklearn.metrics.pairwise import cosine_similarity
        except ImportError:
            print("⚠️ scikit-learn non disponibile. Installa: pip install scikit-learn")
            return []
        
        query_embedding = self.model.encode([query])
        
        all_jokes = []
        all_embeddings = []
        
        # Appiattisci tutti i jokes da tutte le categorie
        for category, jokes in self.jokes_data.items():
            for joke_data in jokes:
                all_jokes.append(joke_data["text"])
                all_embeddings.append(joke_data["embedding"])
        
        if not all_embeddings:
            return []
        
        # Calcola similarità
        similarities = cosine_similarity(query_embedding, all_embeddings)[0]
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        
        selected_jokes = [all_jokes[i] for i in top_indices]
        print(f"🎯 Trovati {len(selected_jokes)} jokes rilevanti")
        return selected_jokes

    def is_available(self) -> bool:
        """Controlla se il sistema RAG è disponibile"""
        return self.model is not None and bool(self.jokes_data)
