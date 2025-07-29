"""
Adaptive Comedy System: Sistema di apprendimento per migliorare i comici
"""

import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import os
import time

@dataclass
class ComedyImprovement:
    """Suggerimento di miglioramento per un comico"""
    comedian: str
    improvement_type: str  # 'style', 'topic', 'structure', 'timing'
    suggestion: str
    confidence: float  # 0-1
    based_on_ratings: int
    timestamp: float

class AdaptiveComedySystem:
    """Sistema che apprende dai rating umani e migliora i prompt dei comici"""
    
    def __init__(self, improvements_file: str = "logs/comedy_improvements.json"):
        self.improvements_file = improvements_file
        self.improvements: List[ComedyImprovement] = []
        self.learned_patterns: Dict[str, Dict[str, Any]] = {}
        self.load_data()
    
    def load_data(self):
        """Carica miglioramenti e pattern esistenti"""
        try:
            if os.path.exists(self.improvements_file):
                with open(self.improvements_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                self.improvements = [
                    ComedyImprovement(**imp) for imp in data.get('improvements', [])
                ]
                self.learned_patterns = data.get('learned_patterns', {})
        except Exception as e:
            print(f"⚠️ Errore caricamento miglioramenti: {e}")
            self.improvements = []
            self.learned_patterns = {}
    
    def save_data(self):
        """Salva i dati"""
        try:
            os.makedirs(os.path.dirname(self.improvements_file), exist_ok=True)
            
            data = {
                'improvements': [asdict(imp) for imp in self.improvements],
                'learned_patterns': self.learned_patterns
            }
            
            with open(self.improvements_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"⚠️ Errore salvataggio miglioramenti: {e}")
    
    def analyze_comedian_performance(self, rating_system) -> Dict[str, List[ComedyImprovement]]:
        """Analizza le performance e genera miglioramenti"""
        
        improvements_by_comedian = {}
        
        # Controlla se il rating_system è disponibile
        if not rating_system or not hasattr(rating_system, 'patterns'):
            print("⚠️ Rating system non disponibile per l'analisi delle performance")
            return improvements_by_comedian
        
        for comedian, pattern in rating_system.patterns.items():
            improvements = []
            
            # Analisi rating medio
            if pattern.avg_rating < -0.5:
                improvements.append(ComedyImprovement(
                    comedian=comedian,
                    improvement_type='style',
                    suggestion=f"Il tuo stile attuale non sta funzionando (rating medio: {pattern.avg_rating:.2f}). "
                              f"Prova un approccio più leggero e evita: {', '.join(pattern.failed_elements[:3])}",
                    confidence=0.8,
                    based_on_ratings=pattern.total_ratings,
                    timestamp=time.time()
                ))
            
            elif pattern.avg_rating > 1.0:
                improvements.append(ComedyImprovement(
                    comedian=comedian,
                    improvement_type='style',
                    suggestion=f"Ottimo lavoro! (rating medio: {pattern.avg_rating:.2f}). "
                              f"Continua con: {', '.join(pattern.successful_elements[:3])}",
                    confidence=0.9,
                    based_on_ratings=pattern.total_ratings,
                    timestamp=time.time()
                ))
            
            # Analisi topic
            if pattern.preferred_topics:
                improvements.append(ComedyImprovement(
                    comedian=comedian,
                    improvement_type='topic',
                    suggestion=f"I tuoi topic di maggior successo sono: {', '.join(pattern.preferred_topics)}. "
                              f"Concentrati su questi argomenti.",
                    confidence=0.7,
                    based_on_ratings=len([r for r in rating_system.ratings if r.comedian == comedian]),
                    timestamp=time.time()
                ))
            
            # Analisi struttura
            successful_structures = [elem for elem in pattern.successful_elements 
                                   if elem in ['setup_punchline', 'question_format', 'short_joke', 'long_joke']]
            
            if successful_structures:
                improvements.append(ComedyImprovement(
                    comedian=comedian,
                    improvement_type='structure',
                    suggestion=f"Le strutture che funzionano per te: {', '.join(successful_structures)}",
                    confidence=0.6,
                    based_on_ratings=pattern.total_ratings,
                    timestamp=time.time()
                ))
            
            improvements_by_comedian[comedian] = improvements
            
            # Salva i miglioramenti
            self.improvements.extend(improvements)
        
        self.save_data()
        return improvements_by_comedian
    
    def get_enhanced_prompt(self, comedian: str, base_prompt: str, rating_system) -> str:
        """Migliora il prompt di un comico basandosi sui rating"""
        
        # Controlla se il rating_system è disponibile
        if not rating_system or not hasattr(rating_system, 'patterns'):
            return base_prompt
            
        if comedian not in rating_system.patterns:
            return base_prompt
        
        pattern = rating_system.patterns[comedian]
        enhancements = []
        
        # Aggiungi elementi di successo
        if pattern.successful_elements:
            successful = ', '.join(pattern.successful_elements[:3])
            enhancements.append(f"ELEMENTI CHE FUNZIONANO: {successful}")
        
        # Evita elementi fallimentari
        if pattern.failed_elements:
            failed = ', '.join(pattern.failed_elements[:3])
            enhancements.append(f"EVITA ASSOLUTAMENTE: {failed}")
        
        # Topic preferiti
        if pattern.preferred_topics:
            topics = ', '.join(pattern.preferred_topics[:2])
            enhancements.append(f"TOPIC DI SUCCESSO: {topics}")
        
        # Rating feedback
        if pattern.avg_rating > 0.5:
            enhancements.append("Il pubblico apprezza il tuo stile, continua così!")
        elif pattern.avg_rating < -0.5:
            enhancements.append("Il pubblico non sta ridendo. Cambia approccio, sii più leggero.")
        
        if enhancements:
            enhanced_prompt = f"{base_prompt}\n\n--- FEEDBACK DAL PUBBLICO ---\n" + "\n".join(enhancements)
            return enhanced_prompt
        
        return base_prompt
    
    def get_comedian_insights(self, comedian: str) -> Dict[str, Any]:
        """Ottieni insights dettagliati su un comico"""
        
        comedian_improvements = [imp for imp in self.improvements if imp.comedian == comedian]
        
        # Raggruppa per tipo
        insights = {
            'total_improvements': len(comedian_improvements),
            'by_type': {},
            'latest_suggestions': [],
            'confidence_avg': 0.0
        }
        
        if not comedian_improvements:
            return insights
        
        # Raggruppa per tipo
        for imp in comedian_improvements:
            if imp.improvement_type not in insights['by_type']:
                insights['by_type'][imp.improvement_type] = []
            insights['by_type'][imp.improvement_type].append(imp.suggestion)
        
        # Ultime 3 suggestions
        insights['latest_suggestions'] = sorted(
            comedian_improvements, 
            key=lambda x: x.timestamp, 
            reverse=True
        )[:3]
        
        # Confidence media
        insights['confidence_avg'] = sum(imp.confidence for imp in comedian_improvements) / len(comedian_improvements)
        
        return insights
