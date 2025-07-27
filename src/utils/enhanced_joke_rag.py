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
    
    def __init__(self, jokes_file: str = "datasets/integrated_jokes_with_embeddings.json"):
        self.jokes_file = jokes_file
        # Prova prima il dataset integrato, poi fallback al vecchio
        if not os.path.exists(jokes_file) and os.path.exists("logs/categorized_jokes_with_embeddings.json"):
            self.jokes_file = "logs/categorized_jokes_with_embeddings.json"
            print("📚 Usando dataset legacy, considera di rigenerare gli embeddings per il dataset integrato")
        
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
                                  use_web_search: bool = True, top_k: int = 3, 
                                  enhanced_tv_search: bool = False,
                                  comedian_name: str = None) -> Dict:
        """Enhanced retrieval con contesto web e ricerca specializzata TV/meme"""
        if not self.model or not self.jokes_data:
            return {
                "jokes": [],
                "web_context": "",
                "tv_meme_context": {},
                "enhanced_query": f"{humor_style} about {topic}",
                "timestamp": time.time(),
                "status": "RAG not available"
            }
        
        # Ottieni contesto web generale
        web_context = ""
        tv_meme_context = {}
        
        if use_web_search:
            if enhanced_tv_search:
                # Use specialized TV/meme search
                tv_meme_context = self.search_tv_and_meme_context(topic)
                # Combine all contexts for web_context
                all_contexts = []
                for context_type, content in tv_meme_context.items():
                    if content:
                        all_contexts.append(f"{context_type.upper()}: {content}")
                web_context = " | ".join(all_contexts)
            else:
                # Use general web search
                web_context = self._search_current_context(topic)
        
        # Crea query migliorata personalizzata per il comico
        enhanced_query = self._create_personalized_query(humor_style, topic, web_context, comedian_name)
        
        # Recupera jokes rilevanti con filtri per personalità
        relevant_jokes = self._personality_filtered_search(enhanced_query, top_k, comedian_name)
        
        return {
            "jokes": relevant_jokes,
            "web_context": web_context,
            "tv_meme_context": tv_meme_context,
            "enhanced_query": enhanced_query,
            "timestamp": time.time(),
            "status": "success",
            "comedian_filter": comedian_name
        }
    
    def _search_current_context(self, topic: str, max_results: int = 5) -> str:
        """Enhanced search for current context including TV shows, memes, and debates"""
        cache_key = f"search_{topic}_{int(time.time() // 3600)}"
        if cache_key in self.search_cache:
            return self.search_cache[cache_key]
        
        try:
            from duckduckgo_search import DDGS
            
            # Create multiple search queries for different types of content
            search_queries = [
                f"{topic} latest episode recap reaction 2025",
                f"{topic} memes viral funny tweets reddit 2025", 
                f"{topic} controversy debate discussion online 2025",
                f"{topic} news trending social media 2025"
            ]
            
            all_context_snippets = []
            
            with DDGS() as ddgs:
                for query in search_queries:
                    try:
                        results = list(ddgs.text(query, max_results=max_results//len(search_queries) + 1))
                        
                        for result in results:
                            title = result.get('title', '')
                            body = result.get('body', '')[:200]
                            snippet = f"{title} - {body}..."
                            all_context_snippets.append(snippet)
                            
                    except Exception as e:
                        print(f"⚠️ Search query failed: {query} - {e}")
                        continue
                
                # Limit total context length
                web_context = " | ".join(all_context_snippets[:6])  # Max 6 snippets
                self.search_cache[cache_key] = web_context
                print(f"🌐 Enhanced context retrieved for '{topic}': {len(web_context)} chars")
                return web_context
                
        except ImportError:
            print("⚠️ duckduckgo-search not installed. Run: pip install duckduckgo-search")
            return ""
        except Exception as e:
            print(f"⚠️ Web search failed: {e}")
            return ""
    
    def search_tv_and_meme_context(self, topic: str) -> Dict[str, str]:
        """Specialized search for TV shows, memes, viral content, politics, gossip, and science"""
        try:
            from duckduckgo_search import DDGS
            
            contexts = {
                "tv_episodes": "",
                "memes_viral": "",
                "debates_discussions": "",
                "social_reactions": "",
                "political_scandals": "",
                "celebrity_gossip": "",
                "science_weird": "",
                "trending_news": ""
            }
            
            # Expanded specialized search queries
            search_configs = [
                ("tv_episodes", f"{topic} episode recap review latest season 2025"),
                ("memes_viral", f"{topic} memes funny viral TikTok Twitter Reddit 2025"),
                ("debates_discussions", f"{topic} controversy debate opinions reactions 2025"),
                ("social_reactions", f"{topic} fans reaction Twitter Instagram comments 2025"),
                ("political_scandals", f"{topic} political scandal controversy gaffe mistake 2025"),
                ("celebrity_gossip", f"{topic} celebrity gossip drama relationship breakup 2025"),
                ("science_weird", f"{topic} science discovery weird funny bizarre research 2025"),
                ("trending_news", f"{topic} trending news viral story unusual bizarre 2025")
            ]
            
            with DDGS() as ddgs:
                for context_type, query in search_configs:
                    try:
                        results = list(ddgs.text(query, max_results=2))
                        snippets = []
                        
                        for result in results:
                            title = result.get('title', '')
                            body = result.get('body', '')[:150]
                            snippets.append(f"{title}: {body}")
                        
                        contexts[context_type] = " | ".join(snippets)
                        
                    except Exception as e:
                        print(f"⚠️ Failed to search {context_type}: {e}")
                        continue
            
            # Print what we found for debugging
            found_contexts = [k for k, v in contexts.items() if v]
            if found_contexts:
                print(f"🔍 Found context types: {', '.join(found_contexts)}")
            
            return contexts
            
        except ImportError:
            print("⚠️ duckduckgo-search not installed")
            return {}
        except Exception as e:
            print(f"⚠️ TV/Meme search failed: {e}")
            return {}
    
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

    def _create_personalized_query(self, humor_style: str, topic: str, web_context: str, comedian_name: str = None) -> str:
        """Crea query personalizzata per specifici comici"""
        
        # Personalizzazioni per comico
        personality_keywords = {
            "Dave": ["cynical", "brutal honesty", "uncomfortable truth", "social hypocrisy", "perverted psychology"],
            "Sarah": ["wordplay", "linguistic", "clever", "savage wit", "alliteration", "metaphor"],
            "Mike": ["family horror", "parenting nightmare", "domestic terror", "marriage survival", "dark family"],
            "Lisa": ["academic", "scientific", "research", "study", "intellectual", "fake statistics"]
        }
        
        base_query = f"{humor_style} comedy about {topic}"
        
        if comedian_name and comedian_name in personality_keywords:
            keywords = " ".join(personality_keywords[comedian_name])
            enhanced_query = f"{base_query} {keywords}"
        else:
            enhanced_query = base_query
            
        if web_context:
            enhanced_query += f" current context: {web_context[:200]}"
            
        return enhanced_query

    def _personality_filtered_search(self, query: str, top_k: int, comedian_name: str = None) -> List[Dict]:
        """Ricerca jokes con filtri personalizzati per comico"""
        if not self.model:
            return []
            
        # Prima fai la ricerca standard
        standard_results = self._similarity_search(query, top_k * 2)  # Prendi più risultati
        
        if not comedian_name:
            return standard_results[:top_k]
        
        # Applica filtri personalizzati
        personality_filters = {
            "Dave": ["relationship", "technology", "social", "people", "society"],
            "Sarah": ["dating", "men", "relationship", "women", "social"],
            "Mike": ["family", "kids", "marriage", "parent", "children"],
            "Lisa": ["people", "behavior", "psychology", "social", "modern"]
        }
        
        if comedian_name in personality_filters:
            keywords = personality_filters[comedian_name]
            filtered_results = []
            
            for joke in standard_results:
                joke_text = joke.get('joke', '').lower()
                # Score based on personality keywords
                personality_score = sum(1 for keyword in keywords if keyword in joke_text)
                joke['personality_score'] = personality_score
                filtered_results.append(joke)
            
            # Sort by personality score, then by original order
            filtered_results.sort(key=lambda x: x.get('personality_score', 0), reverse=True)
            return filtered_results[:top_k]
        
        return standard_results[:top_k]

    def is_available(self) -> bool:
        """Controlla se il sistema RAG è disponibile"""
        return self.model is not None and bool(self.jokes_data)
