#!/usr/bin/env python3
"""
Human Rating System: Sistema di rating umano per battute con apprendimento
"""

import json
import time
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
import os

@dataclass
class HumanRating:
    """Rating umano per una battuta"""
    joke: str
    comedian: str
    topic: str
    rating: str  # "like", "dislike", "love", "hate", "meh"
    rating_score: float  # -2 to +2 scale
    comment: Optional[str]
    timestamp: float
    context: Dict[str, Any]  # Contesto aggiuntivo (pubblico, mood, etc.)

@dataclass
class LearningPattern:
    """Pattern appreso dai rating umani"""
    comedian: str
    successful_elements: List[str]  # Elementi che funzionano
    failed_elements: List[str]      # Elementi che non funzionano
    preferred_topics: List[str]
    avg_rating: float
    total_ratings: int
    last_updated: float

class HumanRatingSystem:
    """Sistema per raccogliere e analizzare rating umani delle battute"""
    
    def __init__(self, data_file: str = "logs/human_ratings.json"):
        self.data_file = data_file
        self.ratings: List[HumanRating] = []
        self.patterns: Dict[str, LearningPattern] = {}
        self.load_data()
    
    def load_data(self):
        """Carica dati esistenti"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                self.ratings = [HumanRating(**rating) for rating in data.get('ratings', [])]
                
                patterns_data = data.get('patterns', {})
                self.patterns = {
                    comedian: LearningPattern(**pattern_data)
                    for comedian, pattern_data in patterns_data.items()
                }
        except Exception as e:
            print(f"⚠️ Errore caricamento dati rating: {e}")
            self.ratings = []
            self.patterns = {}
    
    def save_data(self):
        """Salva i dati su file"""
        try:
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
            
            data = {
                'ratings': [asdict(rating) for rating in self.ratings],
                'patterns': {
                    comedian: asdict(pattern)
                    for comedian, pattern in self.patterns.items()
                }
            }
            
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"⚠️ Errore salvataggio dati rating: {e}")
    
    def add_rating(self, joke: str, comedian: str, topic: str, rating: str, 
                   comment: str = None, context: Dict[str, Any] = None) -> bool:
        """Aggiunge un nuovo rating"""
        
        # Mappa rating a punteggio numerico
        rating_scores = {
            'hate': -2.0,
            'dislike': -1.0,
            'meh': 0.0,
            'like': 1.0,
            'love': 2.0
        }
        
        if rating not in rating_scores:
            return False
        
        new_rating = HumanRating(
            joke=joke,
            comedian=comedian,
            topic=topic,
            rating=rating,
            rating_score=rating_scores[rating],
            comment=comment,
            timestamp=time.time(),
            context=context or {}
        )
        
        self.ratings.append(new_rating)
        self.update_learning_patterns(new_rating)
        self.save_data()
        
        return True
    
    def update_learning_patterns(self, rating: HumanRating):
        """Aggiorna i pattern di apprendimento basati sul nuovo rating"""
        
        comedian = rating.comedian
        
        if comedian not in self.patterns:
            self.patterns[comedian] = LearningPattern(
                comedian=comedian,
                successful_elements=[],
                failed_elements=[],
                preferred_topics=[],
                avg_rating=0.0,
                total_ratings=0,
                last_updated=time.time()
            )
        
        pattern = self.patterns[comedian]
        
        # Aggiorna statistiche
        total_score = pattern.avg_rating * pattern.total_ratings + rating.rating_score
        pattern.total_ratings += 1
        pattern.avg_rating = total_score / pattern.total_ratings
        pattern.last_updated = time.time()
        
        # Analizza elementi della battuta
        joke_elements = self.extract_joke_features(rating.joke)
        
        if rating.rating_score >= 1.0:  # Like o Love
            # Aggiungi elementi di successo
            for element in joke_elements:
                if element not in pattern.successful_elements:
                    pattern.successful_elements.append(element)
            
            # Aggiungi topic preferito
            if rating.topic not in pattern.preferred_topics:
                pattern.preferred_topics.append(rating.topic)
                
        elif rating.rating_score <= -1.0:  # Dislike o Hate
            # Aggiungi elementi fallimentari
            for element in joke_elements:
                if element not in pattern.failed_elements:
                    pattern.failed_elements.append(element)
    
    def extract_joke_features(self, joke: str) -> List[str]:
        """Estrae caratteristiche dalla battuta per l'apprendimento"""
        features = []
        
        joke_lower = joke.lower()
        
        # Parole chiave emotive
        if any(word in joke_lower for word in ['morte', 'morto', 'uccidere', 'hitler', 'guerra']):
            features.append('dark_humor')
        
        if any(word in joke_lower for word in ['nonna', 'nonno', 'famiglia', 'mamma', 'papà']):
            features.append('family_reference')
        
        if any(word in joke_lower for word in ['sesso', 'fidanzata', 'moglie', 'marito']):
            features.append('relationship_humor')
        
        # Strutture linguistiche
        if '?' in joke:
            features.append('question_format')
        
        if joke.count(',') > 2:
            features.append('complex_setup')
        
        if any(word in joke_lower for word in ['perché', 'come mai', 'cosa']):
            features.append('setup_punchline')
        
        # Lunghezza
        if len(joke.split()) < 10:
            features.append('short_joke')
        elif len(joke.split()) > 30:
            features.append('long_joke')
        else:
            features.append('medium_joke')
        
        return features
    
    def get_comedian_suggestions(self, comedian: str) -> Dict[str, Any]:
        """Ottieni suggerimenti per migliorare un comico"""
        
        if comedian not in self.patterns:
            return {
                'status': 'no_data',
                'message': 'Nessun dato disponibile per questo comico'
            }
        
        pattern = self.patterns[comedian]
        
        suggestions = {
            'avg_rating': pattern.avg_rating,
            'total_ratings': pattern.total_ratings,
            'successful_elements': pattern.successful_elements[:5],  # Top 5
            'failed_elements': pattern.failed_elements[:5],
            'preferred_topics': pattern.preferred_topics[:3],
            'recommendations': []
        }
        
        # Genera raccomandazioni
        if pattern.avg_rating < 0:
            suggestions['recommendations'].append(
                f"⚠️ Performance sotto la media. Evita: {', '.join(pattern.failed_elements[:3])}"
            )
        
        if pattern.successful_elements:
            suggestions['recommendations'].append(
                f"✅ Continua a usare: {', '.join(pattern.successful_elements[:3])}"
            )
        
        if pattern.preferred_topics:
            suggestions['recommendations'].append(
                f"🎯 Topic di successo: {', '.join(pattern.preferred_topics)}"
            )
        
        return suggestions
    
    def get_global_stats(self) -> Dict[str, Any]:
        """Statistiche globali del sistema"""
        
        if not self.ratings:
            return {'total_ratings': 0}
        
        # Calcola statistiche per comico
        comedian_stats = {}
        for rating in self.ratings:
            if rating.comedian not in comedian_stats:
                comedian_stats[rating.comedian] = {'ratings': [], 'avg': 0}
            comedian_stats[rating.comedian]['ratings'].append(rating.rating_score)
        
        for comedian in comedian_stats:
            ratings = comedian_stats[comedian]['ratings']
            comedian_stats[comedian]['avg'] = sum(ratings) / len(ratings)
            comedian_stats[comedian]['count'] = len(ratings)
        
        # Top performer
        best_comedian = max(comedian_stats.keys(), 
                          key=lambda c: comedian_stats[c]['avg']) if comedian_stats else None
        
        return {
            'total_ratings': len(self.ratings),
            'comedian_stats': comedian_stats,
            'best_performer': best_comedian,
            'avg_global_rating': sum(r.rating_score for r in self.ratings) / len(self.ratings)
        }
    
    def get_recent_ratings(self, limit: int = 10) -> List[HumanRating]:
        """Ottieni i rating più recenti"""
        return sorted(self.ratings, key=lambda r: r.timestamp, reverse=True)[:limit]
