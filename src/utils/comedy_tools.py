#!/usr/bin/env python3
"""
Comedy Tools: Strumenti avanzati per il ragionamento comico degli agenti  
Implementa tecniche di analisi e generazione dell'umorismo
"""

import random
import re
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass

@dataclass
class ComedyAnalysis:
    """Analisi di una battuta"""
    humor_type: str
    setup_strength: float
    punchline_impact: float
    timing_score: float
    relatability: float
    originality: float
    overall_score: float

class ComedyTools:
    """Toolkit avanzato per il ragionamento comico"""
    
    def __init__(self):
        self.humor_patterns = self._load_humor_patterns()
        self.comedy_techniques = self._load_comedy_techniques()
        self.setup_templates = self._load_setup_templates()
        
    def _load_humor_patterns(self) -> Dict[str, List[str]]:
        """Carica pattern di umorismo riconosciuti"""
        return {
            "incongruity": [
                "setup normale + twist inaspettato",
                "aspettativa + sovversione",
                "contesto familiare + elemento assurdo"
            ],
            "superiority": [
                "confronto intelligente vs stupido",
                "osservazione critica sociale",
                "ironia sulla condizione umana"
            ],
            "relief": [
                "tensione + rilascio",
                "tabù affrontato con leggerezza",
                "ansia trasformata in risata"
            ],
            "wordplay": [
                "doppio significato",
                "suono simile + significato diverso",
                "gioco fonetico + semantico"
            ]
        }
    
    def _load_comedy_techniques(self) -> Dict[str, str]:
        """Tecniche specifiche per ogni stile comico"""
        return {
            "exaggeration": "Amplifica un aspetto normale fino all'assurdo",
            "misdirection": "Guida il pubblico verso una conclusione, poi sorprendi",
            "callback": "Richiama un elemento precedente in modo inaspettato",
            "rule_of_three": "Stabilisci pattern con 2 elementi, rompi con il 3°",
            "juxtaposition": "Metti insieme elementi che normalmente non stanno insieme",
            "self_deprecation": "Prendi in giro te stesso prima che lo facciano altri",
            "observation": "Trova l'assurdo nel quotidiano",
            "timing": "Il momento giusto può rendere tutto più divertente"
        }
    
    def _load_setup_templates(self) -> Dict[str, List[str]]:
        """Template per setup efficaci"""
        return {
            "observational": [
                "Have you ever noticed that {observation}?",
                "Why is it that {situation}?",
                "What's the deal with {topic}?",
                "Isn't it weird how {contradiction}?"
            ],
            "storytelling": [
                "So I was {situation} the other day, and {unexpected_event}",
                "My {relationship} told me {statement}, and I thought {reaction}",
                "You know what happened to me {timeframe}? {story_setup}"
            ],
            "wordplay": [
                "What do you call {description}? {pun_answer}",
                "Why did the {subject} {action}? Because {pun_reason}",
                "I used to {activity}, but {wordplay_twist}"
            ],
            "absurd": [
                "What if {normal_thing} were actually {absurd_alternative}?",
                "In a parallel universe where {absurd_rule}, {consequence}",
                "Scientists discovered that {ridiculous_finding}"
            ]
        }

    def analyze_joke_quality(self, joke: str) -> ComedyAnalysis:
        """Analizza la qualità di una battuta"""
        
        # Analizza setup e punchline
        setup_strength = self._analyze_setup(joke)
        punchline_impact = self._analyze_punchline(joke)
        timing_score = self._analyze_timing(joke)
        relatability = self._analyze_relatability(joke)
        originality = self._analyze_originality(joke)
        
        # Identifica tipo di umorismo
        humor_type = self._identify_humor_type(joke)
        
        # Calcola score complessivo
        overall_score = (setup_strength + punchline_impact + timing_score + 
                        relatability + originality) / 5.0
        
        return ComedyAnalysis(
            humor_type=humor_type,
            setup_strength=setup_strength,
            punchline_impact=punchline_impact,
            timing_score=timing_score,
            relatability=relatability,
            originality=originality,
            overall_score=overall_score
        )
    
    def _analyze_setup(self, joke: str) -> float:
        """Analyze the quality of the setup"""
        setup_indicators = [
            "have you ever noticed",
            "what's the deal with",
            "why is it that",
            "you know what i hate",
            "i was thinking about"
        ]
        
        joke_lower = joke.lower()
        setup_score = 0.3  # Base score
        
        # Bonus for setup indicators
        for indicator in setup_indicators:
            if indicator in joke_lower:
                setup_score += 0.3
                break
        
        # Penalize if too long
        if len(joke.split()) > 30:
            setup_score -= 0.2
        
        # Bonus for questions
        if "?" in joke:
            setup_score += 0.2
            
        return min(setup_score, 1.0)
    
    def _analyze_punchline(self, joke: str) -> float:
        """Analyze the impact of the punchline"""
        score = 0.5
        
        # Look for surprise elements
        surprise_words = ["but", "however", "actually", "turns out", "except", "until"]
        if any(word in joke.lower() for word in surprise_words):
            score += 0.3
        
        # Bonus for wordplay
        if self._contains_wordplay(joke):
            score += 0.2
        
        return min(score, 1.0)
    
    def _analyze_timing(self, joke: str) -> float:
        """Analyze the timing of the joke"""
        words = joke.split()
        
        # Jokes that are too long lose punch
        if len(words) > 50:
            return 0.3
        elif len(words) > 30:
            return 0.6
        elif 10 <= len(words) <= 25:
            return 0.9
        else:
            return 0.7
    
    def _analyze_relatability(self, joke: str) -> float:
        """Analyze relatability"""
        relatable_topics = [
            "work", "family", "food", "technology", "traffic", "sleep",
            "money", "relationships", "social media", "shopping", "weather"
        ]
        
        score = 0.4
        for topic in relatable_topics:
            if topic in joke.lower():
                score += 0.1
        
        return min(score, 1.0)
    
    def _analyze_originality(self, joke: str) -> float:
        """Analyze originality"""
        # Simple check for common cliches
        cliches = [
            "walked into a bar", "your mama", "that's what she said",
            "chicken cross the road", "lightbulb"
        ]
        
        joke_lower = joke.lower()
        score = 0.8
        for cliche in cliches:
            if cliche in joke_lower:
                score -= 0.3
        
        return max(score, 0.2)
    
    def _identify_humor_type(self, joke: str) -> str:
        """Identify the predominant humor type"""
        joke_lower = joke.lower()
        
        if any(pattern in joke_lower for pattern in ["what do you call", "why did", "pun"]):
            return "wordplay"
        elif any(pattern in joke_lower for pattern in ["have you noticed", "why is it"]):
            return "observational"
        elif "what if" in joke_lower or "imagine" in joke_lower:
            return "absurd"
        elif len(joke.split()) > 30:
            return "storytelling"
        else:
            return "mixed"
    
    def _contains_wordplay(self, joke: str) -> bool:
        """Detect wordplay"""
        # Simple heuristic for wordplay
        words = joke.lower().split()
        
        # Look for words with similar sounds
        for i, word in enumerate(words):
            for j, other_word in enumerate(words):
                if i != j and len(word) > 3 and len(other_word) > 3:
                    if self._sound_similar(word, other_word):
                        return True
        return False
    
    def _sound_similar(self, word1: str, word2: str) -> bool:
        """Basic check for phonetic similarity"""
        # Remove vowels and compare consonants
        consonants1 = re.sub(r'[aeiou]', '', word1)
        consonants2 = re.sub(r'[aeiou]', '', word2)
        
        return consonants1 == consonants2 and word1 != word2

    def suggest_improvements(self, joke: str, analysis: ComedyAnalysis) -> List[str]:
        """Suggest improvements for a joke"""
        suggestions = []
        
        if analysis.setup_strength < 0.6:
            suggestions.append("Make the setup clearer and more intriguing")
            suggestions.append("Create more anticipation before the punchline")
        
        if analysis.punchline_impact < 0.6:
            suggestions.append("Add an element of surprise")
            suggestions.append("Try a more unexpected twist")
        
        if analysis.timing_score < 0.6:
            suggestions.append("Shorten the joke for more impact")
            suggestions.append("Remove non-essential words")
        
        if analysis.relatability < 0.6:
            suggestions.append("Use more universal situations")
            suggestions.append("Reference common experiences")
        
        if analysis.originality < 0.6:
            suggestions.append("Avoid overused cliches")
            suggestions.append("Find a new angle for the topic")
        
        return suggestions

    def generate_comedy_prompt(self, topic: str, style: str, comedian_persona: Dict, 
                              tv_meme_context: Dict = None, adaptive_system=None) -> str:
        """Generate an advanced prompt for joke creation with TV/meme context, strong personality, and adaptive learning"""
        
        # Select appropriate technique
        techniques = list(self.comedy_techniques.keys())
        chosen_technique = random.choice(techniques)
        
        # Select template
        templates = self.setup_templates.get(style, self.setup_templates["observational"])
        template = random.choice(templates)
        
        # Build context section with expanded categories
        context_section = ""
        if tv_meme_context:
            context_parts = []
            for context_type, content in tv_meme_context.items():
                if content:
                    context_display_names = {
                        "tv_episodes": "📺 TV EPISODES",
                        "memes_viral": "🔥 VIRAL MEMES", 
                        "debates_discussions": "💬 DEBATES",
                        "social_reactions": "📱 SOCIAL REACTIONS",
                        "political_scandals": "🏛️ POLITICAL SCANDALS",
                        "celebrity_gossip": "⭐ CELEBRITY GOSSIP",
                        "science_weird": "🧪 WEIRD SCIENCE",
                        "trending_news": "📰 TRENDING NEWS"
                    }
                    display_name = context_display_names.get(context_type, context_type.upper())
                    context_parts.append(f"{display_name}: {content}")
            
            if context_parts:
                context_section = f"""
🌐 CURRENT HOT CONTEXT FROM INTERNET:
{' | '.join(context_parts[:3])}  # Limit to avoid prompt overflow

💡 USE THIS CONTEXT TO MAKE TIMELY, EDGY, RELEVANT JOKES ABOUT WHAT'S HAPPENING NOW!
"""
        
        # Enhanced personality traits based on comedian
        personality_boost = ""
        comedian_name = comedian_persona.get('name', 'Comedian')
        
        if 'Dave' in comedian_name:
            personality_boost = """
🎭 DAVE PERSONALITY AMPLIFIER:
- Be EDGY and push boundaries (but stay clever)
- Use unexpected perspectives that shock then make people think
- Reference personal experiences with a dark twist
- Master of the unexpected callback and misdirection
- Don't just observe - JUDGE and be brutally honest about human nature
"""
        elif 'Sarah' in comedian_name:
            personality_boost = """
🎭 SARAH PERSONALITY AMPLIFIER:
- Be RAZOR SHARP with wit - cut through BS instantly  
- Use self-deprecating humor but from a position of strength
- Master of one-liners that hit like a slap
- Reference dating, relationships, and modern life with brutal honesty
- Don't just make jokes - make POINTS about society
"""
        elif 'Mike' in comedian_name:
            personality_boost = """
🎭 MIKE PERSONALITY AMPLIFIER:
- Be the EVERYMAN but with surprising depth
- Find the absurd in the mundane with perfect timing
- Use physical comedy in your language (describe gestures, reactions)
- Master of building tension then releasing it unexpectedly
- Connect with the audience like you're talking to friends at a bar
"""
        elif 'Lisa' in comedian_name:
            personality_boost = """
🎭 LISA PERSONALITY AMPLIFIER:
- Be INTELLECTUALLY TWISTED - smart humor with dark edges
- Use scientific/academic references in unexpected ways
- Master of wordplay and linguistic manipulation
- Find humor in things others find disturbing or weird
- Don't explain the joke - let smart people get it
"""
        
        # Adaptive learning feedback section
        adaptive_feedback = ""
        if adaptive_system and hasattr(adaptive_system, 'get_enhanced_prompt'):
            # Use the adaptive system to get personalized feedback
            base_for_feedback = f"You are {comedian_name}, performing {style} comedy about {topic}."
            enhanced = adaptive_system.get_enhanced_prompt(comedian_name, base_for_feedback, adaptive_system.rating_system if hasattr(adaptive_system, 'rating_system') else None)
            if enhanced != base_for_feedback:
                adaptive_feedback = f"""
🎯 AUDIENCE FEEDBACK & LEARNING:
{enhanced.replace(base_for_feedback, '').strip()}
"""

        # Build advanced prompt with personality boost
        prompt = f"""
🎪 ADVANCED COMEDY REASONING SYSTEM WITH PERSONALITY INJECTION

👤 PERSONA: {comedian_name} - {comedian_persona.get('tone', 'neutral')} comedian
🎨 STYLE: {style}
⚡ TECHNIQUE: {chosen_technique} - {self.comedy_techniques[chosen_technique]}
🎯 TOPIC: {topic}

{personality_boost}

{context_section}

{adaptive_feedback}

🧠 CREATIVE PROCESS:
1. 🔍 OBSERVATION: What's the most interesting/absurd/controversial aspect of "{topic}"?
2. 🌶️ CURRENT RELEVANCE: How does the current context make this topic EXPLOSIVE?
3. 🎭 CHARACTER ANGLE: How does YOUR specific comedic personality attack this topic?
4. 🎪 SETUP: Use template "{template}" but TWIST it with your personality
5. 💥 TWIST: Apply "{chosen_technique}" to create genuine surprise/shock/laughter
6. ⏰ TIMING: Keep under 25 words but make every word COUNT

🎯 SPECIFIC OBJECTIVES:
- BE ORIGINAL: Avoid obvious cliches - find the angle no one else would
- BE RELATABLE: Use experiences your audience shares but wouldn't admit
- BE SURPRISING: Subvert expectations with intelligence, not just shock
- BE CURRENT: Reference what's happening NOW in the world
- BE YOURSELF: Channel your specific comedic personality - {comedian_persona.get('catchphrase', 'Be uniquely funny!')}

⚠️ CRITICAL: RESPOND ONLY IN ENGLISH. BE GENUINELY FUNNY, NOT JUST TRYING TO BE FUNNY.

🎤 GENERATE A JOKE THAT EMBODIES YOUR CHARACTER AND MAKES PEOPLE ACTUALLY LAUGH:
"""
        
        return prompt

    def evaluate_and_refine(self, joke: str, target_score: float = 0.7) -> Tuple[str, ComedyAnalysis]:
        """Evaluate and iteratively refine a joke"""
        
        analysis = self.analyze_joke_quality(joke)
        
        if analysis.overall_score >= target_score:
            return joke, analysis
        
        # Generate improvement suggestions
        improvements = self.suggest_improvements(joke, analysis)
        
        # For now return the analysis, in the future we could implement
        # automatic refinement
        return joke, analysis

def create_comedy_reasoning_system():
    """Factory to create the comedy reasoning system"""
    return ComedyTools()

# Test del sistema
if __name__ == "__main__":
    tools = ComedyTools()
    
    # Test joke
    test_joke = "Why don't scientists trust atoms? Because they make up everything!"
    
    analysis = tools.analyze_joke_quality(test_joke)
    print(f"Joke: {test_joke}")
    print(f"Analysis: {analysis}")
    
    suggestions = tools.suggest_improvements(test_joke, analysis)
    print(f"Suggestions: {suggestions}")
