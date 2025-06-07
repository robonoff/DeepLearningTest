#!/usr/bin/env python3
"""
Main Comedy Club Simulator
Orchestrates the entire comedy club simulation with multiple agent approaches
"""

import sys
import os
import subprocess
import json
import time
import random
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.agents import ComedianAgent, ComedianFactory
from src.utils import Config

class ComedyClubSimulator:
    """Main comedy club simulator class"""
    
    def __init__(self, use_ollama: bool = True):
        self.use_ollama = use_ollama
        self.comedians = ComedianFactory.create_all_comedians()
        self.performance_log = []
        self.current_round = 0
        
        # Load joke data if available
        self._load_joke_data()
        
        print(f"🎭 Comedy Club initialized with {len(self.comedians)} comedians")
        print(f"🤖 Ollama mode: {'Enabled' if use_ollama else 'Mock mode'}")
    
    def _load_joke_data(self):
        """Load categorized jokes for fallback"""
        joke_file = Config.get_file_path("logs", "categorized_jokes.json")
        try:
            if os.path.exists(joke_file):
                with open(joke_file, 'r', encoding='utf-8') as f:
                    self.joke_data = json.load(f)
                print(f"📚 Loaded joke database from {joke_file}")
            else:
                self.joke_data = None
                print("⚠️ No joke database found - will generate from scratch")
        except Exception as e:
            print(f"❌ Error loading jokes: {e}")
            self.joke_data = None
    
    def _call_ollama(self, prompt: str, system_prompt: str = "") -> str:
        """Call Ollama directly via subprocess"""
        if not self.use_ollama:
            return self._generate_mock_response()
        
        try:
            # Create full prompt with system message
            full_prompt = f"{system_prompt}\n\nUser: {prompt}\nAssistant:"
            
            cmd = ['ollama', 'run', Config.OLLAMA_MODEL]
            
            process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            stdout, stderr = process.communicate(
                input=full_prompt + "\n", 
                timeout=Config.OLLAMA_TIMEOUT
            )
            
            if process.returncode == 0:
                response = stdout.strip()
                # Clean up the response
                if response.startswith("Assistant:"):
                    response = response[10:].strip()
                return response
            else:
                print(f"⚠️ Ollama error: {stderr}")
                return self._generate_mock_response()
                
        except subprocess.TimeoutExpired:
            print("⚠️ Ollama timeout - using fallback")
            return self._generate_mock_response()
        except Exception as e:
            print(f"❌ Ollama error: {e}")
            return self._generate_mock_response()
    
    def _generate_mock_response(self) -> str:
        """Generate a mock response when Ollama is unavailable"""
        mock_responses = [
            "Why do programmers prefer dark mode? Because light attracts bugs!",
            "I told my computer a joke about infinity... it's still processing it.",
            "My computer keeps freezing. I think it needs a warmer outfit!",
            "Why don't robots ever panic? They have excellent byte control!",
            "I tried to catch some fog today. I mist! Get it? Mist?",
            "Life is like a dark comedy - it's funny until it's happening to you."
        ]
        return random.choice(mock_responses)
    
    def get_comedian_performance(self, comedian: ComedianAgent, topic: str = "") -> str:
        """Get a performance from a specific comedian"""
        if topic:
            prompt = f"Perform a {comedian.humor_style} comedy routine about {topic}. Keep it to 1-2 jokes, short and punchy."
        else:
            prompt = f"Perform your best {comedian.humor_style} comedy material. Keep it to 1-2 jokes."
        
        print(f"🎤 {comedian.name} is performing...")
        
        response = self._call_ollama(prompt, comedian.system_prompt)
        comedian.performance_history.append(response)
        
        return response
    
    def get_comedian_reaction(self, comedian: ComedianAgent, other_performance: str) -> str:
        """Get a comedian's reaction to another performance"""
        prompt = f"React to this joke as a {comedian.humor_style} comedian: '{other_performance}'. Give a brief, witty response."
        
        print(f"💭 {comedian.name} is reacting...")
        
        response = self._call_ollama(prompt, comedian.system_prompt)
        return response
    
    def run_comedy_show(self, rounds: int = None, topics: List[str] = None) -> List[Dict[str, Any]]:
        """Run a complete comedy show"""
        if rounds is None:
            rounds = Config.DEFAULT_ROUNDS
        if topics is None:
            topics = Config.DEFAULT_TOPICS
        
        print(f"\n🎪 Welcome to the AI Comedy Club!")
        print(f"🎭 Tonight we have {len(self.comedians)} amazing comedians!")
        print("=" * 60)
        
        show_log = []
        
        for round_num in range(1, rounds + 1):
            self.current_round = round_num
            print(f"\n🎭 ROUND {round_num}")
            print("-" * 40)
            
            # Pick a topic for this round
            topic = random.choice(topics) if topics else ""
            if topic:
                print(f"🎯 Tonight's topic: {topic.upper()}")
            
            round_performances = []
            
            # Shuffle comedians for variety
            comedians_shuffled = self.comedians.copy()
            random.shuffle(comedians_shuffled)
            
            # Each comedian performs
            for comedian in comedians_shuffled:
                print(f"\n🎤 Now on stage: {comedian.name}!")
                
                performance = self.get_comedian_performance(comedian, topic)
                
                performance_data = {
                    'round': round_num,
                    'comedian': comedian.name,
                    'style': comedian.humor_style,
                    'topic': topic,
                    'performance': performance,
                    'timestamp': datetime.now().isoformat()
                }
                
                round_performances.append(performance_data)
                show_log.append(performance_data)
                
                print(f"🗣️  {comedian.name}: {performance}")
                
                # Simulate audience reaction
                reactions = {
                    'observational': ['😂 Big laughs!', '👏 Standing ovation!', '🤣 Audience loves it!'],
                    'dark': ['😬 Nervous laughter', '😨 Gasps then applause', '🖤 Dark humor appreciated'],
                    'wordplay': ['🙄 Groans and laughs', '📚 Dad joke energy!', '🎯 Pun perfection!'],
                    'absurdist': ['🤔 Confused laughter', '🌌 Mind = blown', '👽 What just happened?!']
                }
                reaction = random.choice(reactions.get(comedian.humor_style, ['👏 Polite applause']))
                print(f"👥 Audience: {reaction}")
                
                time.sleep(2)  # Brief pause
            
            # Get reactions between comedians
            if len(round_performances) > 1:
                print(f"\n💬 Comedian reactions:")
                featured_performance = random.choice(round_performances)
                
                for comedian in comedians_shuffled:
                    if comedian.name != featured_performance['comedian']:
                        reaction = self.get_comedian_reaction(comedian, featured_performance['performance'])
                        print(f"   {comedian.name}: {reaction[:80]}...")
                        
                        reaction_data = {
                            'round': round_num,
                            'comedian': comedian.name,
                            'type': 'reaction',
                            'reacting_to': featured_performance['comedian'],
                            'reaction': reaction,
                            'timestamp': datetime.now().isoformat()
                        }
                        show_log.append(reaction_data)
            
            if round_num < rounds:
                print(f"\n⏸️  Brief intermission...")
                time.sleep(2)
        
        print(f"\n🎊 Show complete! Total performances: {len([log for log in show_log if 'performance' in log])}")
        print("👏 Thank you for attending the AI Comedy Club!")
        
        # Save show log
        self._save_show_log(show_log)
        
        return show_log
    
    def _save_show_log(self, show_log: List[Dict[str, Any]]):
        """Save the show log to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = Config.get_file_path("logs", f"comedy_show_{timestamp}.json")
        
        # Ensure logs directory exists
        os.makedirs(Config.LOGS_DIR, exist_ok=True)
        
        show_data = {
            'metadata': {
                'show_date': datetime.now().isoformat(),
                'total_performances': len([log for log in show_log if 'performance' in log]),
                'comedians': [c.name for c in self.comedians],
                'rounds': self.current_round,
                'mode': 'ollama' if self.use_ollama else 'mock'
            },
            'show_log': show_log
        }
        
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(show_data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Show saved to {log_file}")

def main():
    """Main function"""
    print("🎭 AI Comedy Club Simulator")
    print("=" * 50)
    
    # Check if Ollama is available
    use_ollama = True
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True, timeout=10)
        if result.returncode != 0:
            print("⚠️ Ollama not available - running in mock mode")
            use_ollama = False
        else:
            print("✅ Ollama is available")
    except Exception as e:
        print(f"⚠️ Cannot access Ollama: {e} - running in mock mode")
        use_ollama = False
    
    # Create and run comedy club
    try:
        club = ComedyClubSimulator(use_ollama=use_ollama)
        show_log = club.run_comedy_show()
        
        print(f"\n🎉 Comedy Club simulation completed successfully!")
        print(f"📊 Total interactions: {len(show_log)}")
        
    except KeyboardInterrupt:
        print("\n⏹️ Show interrupted by user")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
