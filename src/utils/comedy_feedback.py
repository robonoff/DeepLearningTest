#!/usr/bin/env python3
"""
Comedy Feedback System: Sistema di feedback iterativo per migliorare le battute
"""

import json
import time
from typing import List, Dict, Any
from dataclasses import dataclass, asdict

@dataclass
class JokeFeedback:
    """Feedback per una battuta"""
    joke: str
    comedian: str
    topic: str
    quality_score: float
    audience_score: float  # Simulato basato su parametri
    feedback_notes: List[str]
    timestamp: float
    
class ComedyFeedbackSystem:
    """Sistema di feedback per migliorare le performance comiche"""
    
    def __init__(self, feedback_file: str = "logs/comedy_feedback.json"):
        self.feedback_file = feedback_file
        self.feedback_history = self._load_feedback_history()
        self.audience_preferences = self._load_audience_preferences()
        
    def _load_feedback_history(self) -> List[Dict]:
        """Carica lo storico dei feedback"""
        try:
            with open(self.feedback_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
        except Exception as e:
            print(f"Errore caricamento feedback: {e}")
            return []
    
    def _save_feedback_history(self):
        """Salva lo storico dei feedback"""
        try:
            with open(self.feedback_file, 'w', encoding='utf-8') as f:
                json.dump(self.feedback_history, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Errore salvataggio feedback: {e}")
    
    def _load_audience_preferences(self) -> Dict[str, float]:
        """Carica le preferenze simulate del pubblico"""
        return {
            "observational": 0.6,  # Più realistico
            "wordplay": 0.5,      # Più difficile da apprezzare
            "storytelling": 0.7,   # Storie coinvolgenti
            "absurd": 0.4,        # Umorismo assurdo di nicchia
            "relatable_topics": ["work", "technology", "food", "relationships"],
            "timing_preference": 0.6,  # Più selettivo
            "originality_weight": 0.7   # Meno generoso
        }
    
    def simulate_audience_reaction(self, joke: str, comedian: str, topic: str, 
                                 comedy_analysis: Any) -> float:
        """Simula la reazione del pubblico basata su vari fattori"""
        
        # Score base dalla qualità della battuta (più critico)
        base_score = max(0.2, comedy_analysis.overall_score * 0.7)  # Range 0.2-0.7 invece di 0-1
        
        # Bonus per stile preferito dal pubblico (ridotto)
        style_bonus = self.audience_preferences.get(comedy_analysis.humor_type, 0.3) * 0.15
        
        # Bonus per topic relatable (ridotto)
        topic_bonus = 0.05 if topic.lower() in self.audience_preferences["relatable_topics"] else 0
        
        # Bonus per originalità (più selettivo)
        originality_bonus = comedy_analysis.originality * self.audience_preferences["originality_weight"] * 0.1
        
        # Penalità per battute troppo lunghe o troppo corte (più severa)
        length_penalty = 0
        word_count = len(joke.split())
        if word_count > 40:
            length_penalty = -0.2
        elif word_count < 8:
            length_penalty = -0.1
            
        # Bonus per comedian familiare (storico positivo)
        comedian_bonus = self._get_comedian_historical_bonus(comedian)
        
        audience_score = min(1.0, max(0.0, 
            base_score + style_bonus + topic_bonus + originality_bonus + comedian_bonus + length_penalty
        ))
        
        return audience_score
    
    def _get_comedian_historical_bonus(self, comedian: str) -> float:
        """Calcola bonus basato sulla performance storica del comico"""
        comedian_history = [f for f in self.feedback_history if f.get('comedian') == comedian]
        
        if not comedian_history:
            return 0.0
            
        # Media degli score del pubblico per questo comico
        avg_audience_score = sum(f.get('audience_score', 0.5) for f in comedian_history) / len(comedian_history)
        
        # Bonus/penalità basata sulla performance storica
        if avg_audience_score > 0.7:
            return 0.1  # Bonus per comedian che piace al pubblico
        elif avg_audience_score < 0.4:
            return -0.05  # Leggera penalità per comedian che fatica
        else:
            return 0.0
    
    def provide_feedback(self, joke: str, comedian: str, topic: str, 
                        comedy_analysis: Any) -> JokeFeedback:
        """Fornisce feedback completo su una battuta"""
        
        # Simula reazione del pubblico
        audience_score = self.simulate_audience_reaction(joke, comedian, topic, comedy_analysis)
        
        # Genera note di feedback
        feedback_notes = self._generate_feedback_notes(joke, comedy_analysis, audience_score)
        
        # Crea oggetto feedback
        feedback = JokeFeedback(
            joke=joke,
            comedian=comedian,
            topic=topic,
            quality_score=comedy_analysis.overall_score,
            audience_score=audience_score,
            feedback_notes=feedback_notes,
            timestamp=time.time()
        )
        
        # Salva nel database di feedback
        self.feedback_history.append(asdict(feedback))
        self._save_feedback_history()
        
        return feedback
    
    def _generate_feedback_notes(self, joke: str, analysis: Any, audience_score: float) -> List[str]:
        """Genera note di feedback specifiche"""
        notes = []
        
        # Feedback sulla qualità tecnica
        if analysis.overall_score > 0.8:
            notes.append("🌟 Eccellente qualità tecnica!")
        elif analysis.overall_score > 0.6:
            notes.append("👍 Buona struttura comica")
        else:
            notes.append("💡 La struttura può essere migliorata")
        
        # Feedback sull'audience
        if audience_score > 0.8:
            notes.append("🎉 Il pubblico è impazzito!")
        elif audience_score > 0.6:
            notes.append("😊 Buone risate dal pubblico")
        elif audience_score > 0.4:
            notes.append("🤔 Reazione tiepida del pubblico")
        else:
            notes.append("😐 Il pubblico non ha reagito bene")
        
        # Feedback specifico sui componenti
        if analysis.setup_strength < 0.5:
            notes.append("🎯 Migliora il setup per creare più aspettativa")
        
        if analysis.punchline_impact < 0.5:
            notes.append("💥 La punchline ha bisogno di più sorpresa")
        
        if analysis.timing_score < 0.6:
            notes.append("⏰ Lavora sul timing - più conciso o più sviluppato")
        
        if analysis.relatability < 0.5:
            notes.append("🤝 Rendi la battuta più universale e relatable")
        
        if analysis.originality < 0.5:
            notes.append("✨ Cerca un angolo più originale per il topic")
        
        return notes
    
    def get_comedian_stats(self, comedian: str) -> Dict[str, Any]:
        """Ottieni statistiche per un comico specifico"""
        comedian_jokes = [f for f in self.feedback_history if f.get('comedian') == comedian]
        
        if not comedian_jokes:
            return {"message": f"Nessuna performance registrata per {comedian}"}
        
        avg_quality = sum(j.get('quality_score', 0) for j in comedian_jokes) / len(comedian_jokes)
        avg_audience = sum(j.get('audience_score', 0) for j in comedian_jokes) / len(comedian_jokes)
        
        # Trova la battuta migliore
        best_joke = max(comedian_jokes, key=lambda j: j.get('audience_score', 0))
        
        # Analizza i topic preferiti
        topics = [j.get('topic', '') for j in comedian_jokes]
        topic_counts = {}
        for topic in topics:
            topic_counts[topic] = topic_counts.get(topic, 0) + 1
        
        best_topic = max(topic_counts.items(), key=lambda x: x[1])[0] if topic_counts else "N/A"
        
        return {
            "comedian": comedian,
            "total_performances": len(comedian_jokes),
            "average_quality": avg_quality,
            "average_audience_score": avg_audience,
            "best_joke": best_joke.get('joke', ''),
            "best_topic": best_topic,
            "improvement_trend": self._calculate_improvement_trend(comedian_jokes)
        }
    
    def _calculate_improvement_trend(self, jokes: List[Dict]) -> str:
        """Calcola il trend di miglioramento di un comico"""
        if len(jokes) < 3:
            return "Dati insufficienti"
        
        # Ordina per timestamp
        sorted_jokes = sorted(jokes, key=lambda j: j.get('timestamp', 0))
        
        # Confronta prima metà con seconda metà
        mid = len(sorted_jokes) // 2
        first_half_avg = sum(j.get('audience_score', 0) for j in sorted_jokes[:mid]) / mid
        second_half_avg = sum(j.get('audience_score', 0) for j in sorted_jokes[mid:]) / (len(sorted_jokes) - mid)
        
        if second_half_avg > first_half_avg + 0.1:
            return "📈 In miglioramento!"
        elif second_half_avg < first_half_avg - 0.1:
            return "📉 In calo, serve lavoro"
        else:
            return "📊 Stabile"
    
    def get_top_performers(self, limit: int = 3) -> List[Dict[str, Any]]:
        """Ottieni i migliori performer"""
        comedian_stats = {}
        
        for feedback in self.feedback_history:
            comedian = feedback.get('comedian', 'Unknown')
            if comedian not in comedian_stats:
                comedian_stats[comedian] = []
            comedian_stats[comedian].append(feedback.get('audience_score', 0))
        
        # Calcola medie e ordina
        averages = []
        for comedian, scores in comedian_stats.items():
            avg_score = sum(scores) / len(scores)
            averages.append({
                'comedian': comedian,
                'average_score': avg_score,
                'performances': len(scores)
            })
        
        return sorted(averages, key=lambda x: x['average_score'], reverse=True)[:limit]

def create_feedback_system():
    """Factory per creare il sistema di feedback"""
    return ComedyFeedbackSystem()

# Test del sistema
if __name__ == "__main__":
    feedback_system = ComedyFeedbackSystem()
    print("🎭 Sistema di Feedback Comedy Club inizializzato!")
    
    # Test con dati fake
    class FakeAnalysis:
        overall_score = 0.7
        humor_type = "observational"
        setup_strength = 0.8
        punchline_impact = 0.6
        timing_score = 0.7
        relatability = 0.9
        originality = 0.5
    
    fake_analysis = FakeAnalysis()
    feedback = feedback_system.provide_feedback(
        "Why do programmers prefer dark mode? Because light attracts bugs!",
        "Jerry",
        "technology",
        fake_analysis
    )
    
    print(f"Feedback: {feedback}")
    print(f"Stats Jerry: {feedback_system.get_comedian_stats('Jerry')}")
