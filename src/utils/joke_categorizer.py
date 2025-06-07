#!/usr/bin/env python3
"""
Joke Categorization System for Comedy Club Agents
Categorizes jokes from shortjokes.csv into different humor styles for agent training
"""

import pandas as pd
import re
import json
from typing import Dict, List, Tuple
import random

class JokeCategorizer:
    def __init__(self, csv_file: str):
        print(f"Loading jokes from {csv_file}...")
        self.df = pd.read_csv(csv_file)
        print(f"Loaded {len(self.df)} jokes")
        self.categories = {
            'observational': [],  # Observational humor (Seinfeld-style)
            'dark': [],           # Dark/edgy humor 
            'wordplay': [],       # Puns, wordplay, linguistic jokes
            'absurdist': []       # Surreal, unexpected, absurd humor
        }
        
    def categorize_jokes(self) -> Dict[str, List[str]]:
        """Categorize jokes into different humor styles using pattern matching"""
        
        for _, row in self.df.iterrows():
            joke = str(row['Joke']).lower()
            
            # Skip very short or invalid jokes
            if len(joke) < 10 or joke == 'nan':
                continue
                
            categorized = False
            
            # Observational humor patterns
            if any(pattern in joke for pattern in [
                'you ever notice', 'have you ever', 'why do people', 'what\'s the deal',
                'anyone else', 'is it just me', 'why is it that', 'ever wonder',
                'you know what i hate', 'the thing about', 'what\'s up with'
            ]):
                self.categories['observational'].append(row['Joke'])
                categorized = True
            
            # Dark humor patterns
            elif any(pattern in joke for pattern in [
                'death', 'die', 'kill', 'murder', 'suicide', 'cancer', 'funeral',
                'grave', 'dead', 'coffin', 'corpse', 'hell', 'depression',
                'divorce', 'broke up', 'ex-wife', 'ex-husband'
            ]):
                self.categories['dark'].append(row['Joke'])
                categorized = True
            
            # Wordplay/puns patterns
            elif any(pattern in joke for pattern in [
                'what do you call', 'why did the', 'what\'s the difference',
                'how do you', 'knock knock', 'what did the', 'why was the'
            ]) or self._has_pun(joke):
                self.categories['wordplay'].append(row['Joke'])
                categorized = True
            
            # If not categorized yet, check for absurdist elements
            elif not categorized:
                if any(pattern in joke for pattern in [
                    'walks into a bar', 'alien', 'unicorn', 'time travel',
                    'zombie', 'robot', 'parallel universe', 'teleport',
                    'magic', 'wizard', 'dragon', 'superhero'
                ]) or self._is_absurd(joke):
                    self.categories['absurdist'].append(row['Joke'])
                else:
                    # Default fallback - distribute randomly
                    category = random.choice(list(self.categories.keys()))
                    self.categories[category].append(row['Joke'])
        
        return self.categories
    
    def _has_pun(self, joke: str) -> bool:
        """Simple heuristic to detect puns"""
        # Look for common pun indicators
        pun_indicators = [
            'pun intended', 'get it', 'play on words', 
            # Common pun structures
            r'\b(\w+)-(\w+)\b',  # hyphenated words often used in puns
            r'\b\w*[qxz]\w*\b',  # unusual letters often in puns
        ]
        
        for pattern in pun_indicators:
            if re.search(pattern, joke):
                return True
        return False
    
    def _is_absurd(self, joke: str) -> bool:
        """Detect absurdist humor patterns"""
        absurd_indicators = [
            'suddenly', 'randomly', 'out of nowhere', 'for no reason',
            'inexplicably', 'somehow', 'apparently', 'allegedly'
        ]
        
        return any(indicator in joke for indicator in absurd_indicators)
    
    def balance_categories(self, target_size: int = 5000) -> Dict[str, List[str]]:
        """Balance categories to have roughly equal sizes"""
        balanced = {}
        
        for category, jokes in self.categories.items():
            if len(jokes) > target_size:
                # Randomly sample if too many
                balanced[category] = random.sample(jokes, target_size)
            else:
                # Take all if too few
                balanced[category] = jokes
                
        return balanced
    
    def save_categorized_jokes(self, output_file: str = 'categorized_jokes.json'):
        """Save categorized jokes to JSON file"""
        categorized = self.categorize_jokes()
        balanced = self.balance_categories()
        
        # Add metadata
        result = {
            'metadata': {
                'total_jokes_processed': len(self.df),
                'categories': {cat: len(jokes) for cat, jokes in balanced.items()},
                'timestamp': pd.Timestamp.now().isoformat()
            },
            'jokes': balanced
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Categorized jokes saved to {output_file}")
        print(f"📊 Categories distribution:")
        for category, jokes in balanced.items():
            print(f"   {category.capitalize()}: {len(jokes)} jokes")
        
        return result

if __name__ == "__main__":
    categorizer = JokeCategorizer('shortjokes.csv')
    result = categorizer.save_categorized_jokes()
