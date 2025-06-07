#!/usr/bin/env python3
"""
Simple Comedy Club Simulator using Direct Ollama CLI
Bypasses API issues by calling Ollama directly from terminal
"""

import subprocess
import json
import random
import time
from datetime import datetime
from typing import Dict, List, Optional
import os

class SimpleComedyClub:
    """Simplified comedy club using direct Ollama CLI calls"""
    
    def __init__(self, categorized_jokes_file: str = 'categorized_jokes.json'):
        self.load_jokes(categorized_jokes_file)
        self.comedians = {
            'Jerry_Observational': {
                'style': 'observational',
                'prompt_template': """You are Jerry, a master of observational comedy like Jerry Seinfeld. 
Your style: "What's the deal with..." and "You ever notice..." 
Topic: {topic}
Tell ONE short observational joke (2-3 sentences max) and end with "Am I right?" or similar."""
            },
            'Raven_Dark': {
                'style': 'dark',
                'prompt_template': """You are Raven, a dark humor specialist. 
Your style: Dark but clever twists on everyday situations.
Topic: {topic}
Tell ONE short dark humor joke (2-3 sentences max) and end with "Too dark? Good."""
            },
            'Penny_Wordplay': {
                'style': 'wordplay',
                'prompt_template': """You are Penny, the pun master. 
Your style: Wordplay, puns, and "What do you call..." jokes.
Topic: {topic}
Tell ONE short pun or wordplay joke (2-3 sentences max) and say "Get it?" if it's clever."""
            },
            'Cosmic_Absurd': {
                'style': 'absurdist', 
                'prompt_template': """You are Cosmic, the absurdist comedian.
Your style: Surreal, weird connections, "What if..." scenarios.
Topic: {topic}
Tell ONE short absurd joke (2-3 sentences max) that makes people think "What just happened?" """
            }
        }
        
        self.topics = [
            "smartphones and technology",
            "coffee shops and daily routines", 
            "social media behavior",
            "online shopping and delivery",
            "video calls and remote work",
            "streaming services and binge watching"
        ]
    
    def load_jokes(self, filename: str):
        """Load categorized jokes from JSON file"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.jokes_by_category = data['jokes']
            print(f"📚 Loaded jokes for {len(self.jokes_by_category)} categories")
        except FileNotFoundError:
            print("❌ Categorized jokes not found. Using default prompts.")
            self.jokes_by_category = {}
    
    def call_ollama(self, prompt: str, model: str = "llama3.2:1b", max_length: int = 100) -> str:
        """Call Ollama directly via CLI"""
        try:
            # Prepare the command
            cmd = ['ollama', 'run', model]
            
            # Use subprocess to call ollama
            process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Send prompt and get response with timeout
            try:
                stdout, stderr = process.communicate(input=prompt, timeout=30)
            except subprocess.TimeoutExpired:
                process.kill()
                return "⚠️ Ollama timeout - try again"
            
            if process.returncode == 0:
                # Clean up the response
                response = stdout.strip()
                # Remove any loading indicators or extra text
                lines = response.split('\n')
                # Filter out empty lines and join
                clean_lines = [line.strip() for line in lines if line.strip() and not line.startswith('⠋')]
                return ' '.join(clean_lines)
            else:
                return f"❌ Error: {stderr}"
                
        except Exception as e:
            return f"❌ Error calling Ollama: {e}"
    
    def get_comedian_response(self, comedian_name: str, topic: str) -> str:
        """Get a response from a specific comedian"""
        comedian = self.comedians[comedian_name]
        prompt = comedian['prompt_template'].format(topic=topic)
        
        print(f"🎤 {comedian_name} is performing...")
        response = self.call_ollama(prompt)
        
        return response
    
    def run_comedy_show(self, rounds: int = 2):
        """Run a simple comedy show"""
        print("🎭" + "="*60)
        print("🎤 WELCOME TO THE SIMPLE AI COMEDY CLUB!")
        print("🎭" + "="*60)
        
        comedian_names = list(self.comedians.keys())
        
        for round_num in range(rounds):
            print(f"\n🎭 === ROUND {round_num + 1} ===")
            topic = random.choice(self.topics)
            print(f"🎯 Tonight's topic: {topic}")
            
            # Shuffle comedians for variety
            random.shuffle(comedian_names)
            
            for comedian_name in comedian_names:
                print(f"\n🎤 {comedian_name} takes the stage!")
                
                # Get the comedian's joke
                response = self.get_comedian_response(comedian_name, topic)
                
                # Display the performance
                print(f"🎭 {comedian_name}: {response}")
                
                # Simulate audience reaction
                reactions = ["😂 *Audience laughs*", "👏 *Applause*", "😅 *Nervous laughter*", "🤔 *Confused chuckles*"]
                print(f"👥 {random.choice(reactions)}")
                
                # Brief pause between comedians
                time.sleep(2)
        
        print("\n🎉 That's our show! Thank you for coming to the AI Comedy Club!")
        print("🎭" + "="*60)

def main():
    """Main function"""
    print("🚀 Starting Simple Comedy Club...")
    
    # Check if Ollama is available
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True, timeout=5)
        if result.returncode != 0:
            print("❌ Ollama not available. Please install and start Ollama.")
            return
    except Exception:
        print("❌ Ollama not found. Please install Ollama first.")
        return
    
    # Run the show
    try:
        club = SimpleComedyClub()
        club.run_comedy_show(rounds=3)
    except KeyboardInterrupt:
        print("\n⏹️ Show interrupted by user")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
