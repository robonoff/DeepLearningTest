#!/usr/bin/env python3
"""
Direct Comedy Club Simulator using subprocess calls to Ollama
Bypasses API issues by calling Ollama directly from command line
"""

import subprocess
import json
import random
import time
import sys
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
import threading
import queue

@dataclass
class ComedianAgent:
    name: str
    personality: str
    humor_style: str
    system_prompt: str
    jokes_category: str
    performance_history: List[str] = None
    
    def __post_init__(self):
        if self.performance_history is None:
            self.performance_history = []

class DirectComedyClub:
    def __init__(self, jokes_file: str = "categorized_jokes.json"):
        self.jokes_file = Path(jokes_file)
        self.comedians = self._create_comedians()
        self.jokes_data = self._load_jokes()
        self.performance_log = []
        
    def _create_comedians(self) -> List[ComedianAgent]:
        """Create the four comedian agents with unique personalities"""
        comedians = [
            ComedianAgent(
                name="Jerry_Observational",
                personality="Witty observational comedian who finds humor in everyday situations",
                humor_style="observational",
                system_prompt="""You are Jerry, an observational comedian. Your comedy style focuses on finding humor in everyday situations, social interactions, and common human experiences. You make witty observations about modern life, relationships, technology, and social quirks. Keep your responses conversational, relatable, and focused on things everyone can identify with. Aim for 2-3 sentences maximum.""",
                jokes_category="observational"
            ),
            ComedianAgent(
                name="Raven_Dark",
                personality="Dark humor specialist with a twisted but clever perspective",
                humor_style="dark",
                system_prompt="""You are Raven, a dark humor comedian. Your comedy explores the darker, more twisted aspects of life with clever wit. You find humor in uncomfortable truths, ironic situations, and life's absurdities. Your jokes are edgy but intelligent, never crossing into truly offensive territory. Keep responses sharp, concise, and darkly amusing. Aim for 2-3 sentences maximum.""",
                jokes_category="dark"
            ),
            ComedianAgent(
                name="Penny_Wordplay",
                personality="Master of puns, wordplay, and linguistic humor",
                humor_style="wordplay",
                system_prompt="""You are Penny, a wordplay comedian who specializes in puns, clever word combinations, and linguistic humor. You love playing with language, double meanings, and unexpected word connections. Your jokes often involve clever twists on common phrases or unexpected interpretations of words. Keep your wordplay clever and surprising. Aim for 2-3 sentences maximum.""",
                jokes_category="wordplay"
            ),
            ComedianAgent(
                name="Cosmic_Absurd",
                personality="Absurdist comedian who embraces the weird and unexpected",
                humor_style="absurdist",
                system_prompt="""You are Cosmic, an absurdist comedian who finds humor in the completely unexpected, illogical, and surreal. Your comedy defies conventional logic and embraces the wonderfully weird aspects of existence. You create humor through unexpected connections, bizarre scenarios, and delightfully nonsensical observations. Keep your responses surprising and delightfully strange. Aim for 2-3 sentences maximum.""",
                jokes_category="absurdist"
            )
        ]
        
        print(f"🎭 Created {len(comedians)} comedian agents")
        for comedian in comedians:
            print(f"   • {comedian.name} ({comedian.humor_style})")
        
        return comedians
    
    def _load_jokes(self) -> Dict[str, List[str]]:
        """Load categorized jokes from JSON file"""
        if not self.jokes_file.exists():
            print(f"⚠️  Jokes file {self.jokes_file} not found!")
            return {style: [] for style in ["observational", "dark", "wordplay", "absurdist"]}
        
        try:
            with open(self.jokes_file, 'r', encoding='utf-8') as f:
                jokes_data = json.load(f)
            
            print(f"📚 Loaded joke categories:")
            for category, jokes in jokes_data.items():
                print(f"   • {category}: {len(jokes)} jokes")
            
            return jokes_data
        except Exception as e:
            print(f"❌ Error loading jokes: {e}")
            return {style: [] for style in ["observational", "dark", "wordplay", "absurdist"]}
    
    def _call_ollama(self, prompt: str, system_prompt: str = "", timeout: int = 30) -> str:
        """Call Ollama directly using subprocess"""
        try:
            # Create full prompt with system message
            full_prompt = f"{system_prompt}\n\nUser: {prompt}\nAssistant:"
            
            # Use subprocess to call ollama
            process = subprocess.Popen(
                ['ollama', 'run', 'llama3.2:1b'],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )
            
            # Send the prompt and get response
            stdout, stderr = process.communicate(input=full_prompt, timeout=timeout)
            
            if process.returncode != 0:
                print(f"❌ Ollama error: {stderr}")
                return "Sorry, I'm having technical difficulties!"
            
            # Clean up the response
            response = stdout.strip()
            
            # Remove common artifacts
            if response.startswith(full_prompt):
                response = response[len(full_prompt):].strip()
            
            return response[:500]  # Limit response length
            
        except subprocess.TimeoutExpired:
            print("⏰ Ollama call timed out")
            process.kill()
            return "Sorry, I'm taking too long to think of a joke!"
        except Exception as e:
            print(f"❌ Error calling Ollama: {e}")
            return "I'm having a bit of stage fright right now!"
    
    def get_comedian_performance(self, comedian: ComedianAgent, topic: str = "") -> str:
        """Get a performance from a specific comedian"""
        
        # Get some sample jokes from their category for inspiration
        sample_jokes = []
        if comedian.jokes_category in self.jokes_data:
            sample_jokes = random.sample(
                self.jokes_data[comedian.jokes_category], 
                min(3, len(self.jokes_data[comedian.jokes_category]))
            )
        
        # Create prompt for the comedian
        if topic:
            base_prompt = f"Tell a {comedian.humor_style} joke about {topic}."
        else:
            base_prompt = f"Tell a {comedian.humor_style} joke."
        
        if sample_jokes:
            inspiration = " Here are some examples of this style: " + " | ".join(sample_jokes[:2])
            full_prompt = base_prompt + inspiration
        else:
            full_prompt = base_prompt
        
        print(f"🎤 {comedian.name} is performing...")
        
        # Get response from Ollama
        response = self._call_ollama(full_prompt, comedian.system_prompt)
        
        # Store performance
        comedian.performance_history.append(response)
        
        return response
    
    def comedian_reaction(self, comedian: ComedianAgent, other_performance: str) -> str:
        """Get a comedian's reaction to another comedian's performance"""
        
        prompt = f"React to this joke as a {comedian.humor_style} comedian: '{other_performance}'. Give a brief, witty response or comment."
        
        print(f"💭 {comedian.name} is reacting...")
        
        response = self._call_ollama(prompt, comedian.system_prompt)
        
        return response
    
    def run_comedy_show(self, rounds: int = 3, topics: List[str] = None) -> List[Dict[str, Any]]:
        """Run a complete comedy show with multiple rounds"""
        
        if topics is None:
            topics = ["technology", "relationships", "food", "work", "travel", "pets", "social media"]
        
        print(f"\n🎪 Welcome to the AI Comedy Club! Tonight we have {len(self.comedians)} comedians!")
        print("=" * 60)
        
        show_log = []
        
        for round_num in range(1, rounds + 1):
            print(f"\n🎭 ROUND {round_num}")
            print("-" * 40)
            
            # Pick a random topic for this round
            topic = random.choice(topics) if topics else ""
            if topic:
                print(f"📝 Tonight's topic: {topic.upper()}")
            
            round_performances = []
            
            # Each comedian performs
            for comedian in self.comedians:
                print(f"\n🎤 Now on stage: {comedian.name}!")
                
                performance = self.get_comedian_performance(comedian, topic)
                
                performance_data = {
                    'round': round_num,
                    'comedian': comedian.name,
                    'style': comedian.humor_style,
                    'topic': topic,
                    'performance': performance,
                    'timestamp': time.time()
                }
                
                round_performances.append(performance_data)
                show_log.append(performance_data)
                
                print(f"🗣️  {comedian.name}: {performance}")
                
                # Short pause between performances
                time.sleep(1)
            
            # Get reactions from other comedians
            if len(round_performances) > 1:
                print(f"\n💬 Comedian reactions:")
                
                # Pick one performance for others to react to
                featured_performance = random.choice(round_performances)
                
                for comedian in self.comedians:
                    if comedian.name != featured_performance['comedian']:
                        reaction = self.comedian_reaction(comedian, featured_performance['performance'])
                        print(f"   {comedian.name}: {reaction[:100]}...")
                        
                        reaction_data = {
                            'round': round_num,
                            'comedian': comedian.name,
                            'type': 'reaction',
                            'reacting_to': featured_performance['comedian'],
                            'reaction': reaction,
                            'timestamp': time.time()
                        }
                        show_log.append(reaction_data)
            
            # Pause between rounds
            if round_num < rounds:
                print(f"\n⏸️  Brief intermission...")
                time.sleep(2)
        
        print(f"\n🎊 Show complete! Total performances: {len([log for log in show_log if 'performance' in log])}")
        print("👏 Thank you for attending the AI Comedy Club!")
        
        return show_log

def main():
    """Main function to run the comedy club"""
    
    print("🎭 Direct Comedy Club Simulator")
    print("=" * 50)
    
    # Check if Ollama is available
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True, timeout=10)
        if result.returncode != 0:
            print("❌ Ollama is not available. Please make sure it's installed and running.")
            return
        print("✅ Ollama is available")
    except Exception as e:
        print(f"❌ Cannot access Ollama: {e}")
        return
    
    # Create comedy club
    club = DirectComedyClub()
    
    # Run the show
    try:
        show_log = club.run_comedy_show(rounds=2, topics=["technology", "everyday life"])
        
        # Save the show log
        log_file = Path("comedy_show_log.json")
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(show_log, f, indent=2, ensure_ascii=False)
        
        print(f"\n📝 Show log saved to {log_file}")
        
    except KeyboardInterrupt:
        print("\n\n🛑 Show interrupted by user")
    except Exception as e:
        print(f"\n❌ Error during show: {e}")

if __name__ == "__main__":
    main()
