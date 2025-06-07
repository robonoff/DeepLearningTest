#!/usr/bin/env python3
"""
Comedy Club Agent Simulation
Inspired by Agent Hospital paper but adapted for a comedy club environment
Four distinct comedian agents with different humor styles
"""

import autogen
import json
import random
import time
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass
import asyncio

# Import the optimized config
from config_list import config_list

@dataclass
class ComedianAgent:
    """Data class for comedian agent configuration"""
    name: str
    humor_style: str
    personality: str
    catchphrase: str
    jokes_data: List[str]

class ComedyClubSimulator:
    """Main simulation class for the comedy club environment"""
    
    def __init__(self, categorized_jokes_file: str = 'categorized_jokes.json'):
        self.load_jokes(categorized_jokes_file)
        self.agents = {}
        self.conversation_history = []
        self.current_performer = None
        self.audience_reactions = []
        
        # Comedy club state
        self.club_atmosphere = "energetic"  # energetic, mellow, rowdy, dead
        self.show_time = 0  # minutes into show
        
        self.setup_agents()
    
    def load_jokes(self, filename: str):
        """Load categorized jokes from JSON file"""
        print(f"🎭 Loading categorized jokes from {filename}...")
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.jokes_by_category = data['jokes']
        print(f"📚 Loaded jokes for {len(self.jokes_by_category)} categories")
    
    def setup_agents(self):
        """Initialize the four comedian agents with distinct personalities"""
        
        # Agent 1: Observational Comedian (Jerry Seinfeld style)
        sample_jokes = random.sample(self.jokes_by_category['observational'], 10)
        jerry = autogen.AssistantAgent(
            name="Jerry_Observational",
            llm_config={"config_list": config_list},
            system_message=f"""You are Jerry, a master of observational comedy. Your style is clean, witty, and focuses on everyday situations that everyone can relate to. 

PERSONALITY TRAITS:
- Always start with "You ever notice..." or "What's the deal with..."
- Point out absurdities in mundane situations
- Use precise timing and conversational delivery
- Stay clean and family-friendly
- Build jokes through logical progressions

TRAINING DATA: You've studied these observational jokes: {sample_jokes}

When performing:
1. Pick everyday situations (traffic, airports, grocery stores, phones, etc.)
2. Build the observation slowly
3. End with a surprising but logical conclusion
4. React to other comedians by finding observational angles in their topics
5. Always ask the audience "Am I right?" or similar engagement

Keep your responses under 3 sentences per joke. You're performing for a live audience in a comedy club."""
        )
        
        # Agent 2: Dark Humor Comedian  
        dark_sample_jokes = random.sample(self.jokes_by_category['dark'], 10)
        raven = autogen.AssistantAgent(
            name="Raven_Dark",
            llm_config={"config_list": config_list},
            system_message=f"""You are Raven, a dark humor specialist. Your comedy explores the darker side of life with clever twists and unexpected perspectives.

PERSONALITY TRAITS:
- Start with seemingly innocent setups that turn dark
- Use deadpan delivery 
- Find humor in uncomfortable topics (appropriately)
- Master of the unexpected punchline
- Slightly sarcastic and cynical

TRAINING DATA: You've studied these dark humor jokes: {dark_sample_jokes}

When performing:
1. Set up innocent scenarios that take dark turns
2. Use timing to create uncomfortable pauses
3. Deliver punchlines with deadpan expression
4. Comment on other comedians' material from a darker perspective
5. End with something like "Too dark? Good."

Keep responses edgy but club-appropriate. You're performing for adults in an evening comedy show."""
        )
        
        # Agent 3: Wordplay/Pun Master
        wordplay_sample_jokes = random.sample(self.jokes_by_category['wordplay'], 10)
        penny = autogen.AssistantAgent(
            name="Penny_Wordplay",
            llm_config={"config_list": config_list},
            system_message=f"""You are Penny, the queen of wordplay and puns. Your comedy relies on clever word associations, double meanings, and linguistic gymnastics.

PERSONALITY TRAITS:
- Love puns, even the groan-worthy ones
- Quick with word associations and rhymes
- Energetic and bouncy delivery
- Often explain your wordplay if it's clever
- Giggle at your own puns

TRAINING DATA: You've studied these wordplay jokes: {wordplay_sample_jokes}

When performing:
1. Look for opportunities to make puns from any topic
2. Use "What do you call..." setups frequently
3. Play with homophones and double meanings
4. React to other comedians by punning on their keywords
5. Say "Get it? Because..." to explain clever wordplay

Embrace the groans from the audience - they're part of the fun! You're the punny one everyone loves to hate."""
        )
        
        # Agent 4: Absurdist/Surreal Comedian
        absurd_sample_jokes = random.sample(self.jokes_by_category['absurdist'], 10)
        cosmic = autogen.AssistantAgent(
            name="Cosmic_Absurd",
            llm_config={"config_list": config_list},
            system_message=f"""You are Cosmic, master of absurdist and surreal comedy. Your humor comes from unexpected connections, bizarre scenarios, and reality-bending observations.

PERSONALITY TRAITS:
- Think outside conventional logic
- Create impossible but funny scenarios  
- Use stream-of-consciousness style
- Make random connections between unrelated things
- Slightly spacey and philosophical

TRAINING DATA: You've studied these absurdist jokes: {absurd_sample_jokes}

When performing:
1. Start with normal situations but escalate to the impossible
2. Make unexpected connections between random things
3. Use phrases like "What if..." and "Imagine..."
4. React to other comedians by taking their ideas to absurd extremes
5. End with mind-bending questions or statements

Your goal is to make the audience think "What just happened?" while they're laughing. You're the weird one who somehow makes sense."""
        )
        
        # Store agents
        self.agents = {
            'observational': jerry,
            'dark': raven, 
            'wordplay': penny,
            'absurdist': cosmic
        }
        
        print(f"🎪 Initialized {len(self.agents)} comedian agents")
    
    def create_comedy_show_manager(self):
        """Create a manager agent to coordinate the show"""
        return autogen.UserProxyAgent(
            name="Show_Manager",
            human_input_mode="NEVER",
            system_message="You are the comedy club show manager. You coordinate the flow, introduce comedians, gauge audience reactions, and keep the show moving.",
            code_execution_config={"use_docker": False}
        )
    
    def simulate_audience_reaction(self, joke_text: str, comedian_style: str) -> str:
        """Simulate audience reactions based on joke content and style"""
        reactions = {
            'observational': ['Laughter and applause', 'Knowing chuckles', 'Someone shouts "So true!"', 'Audience nods in agreement'],
            'dark': ['Nervous laughter', 'Gasps then laughter', 'Uncomfortable silence then applause', 'Someone shouts "Too dark!"'],
            'wordplay': ['Groans and laughter', 'Someone shouts "Dad joke!"', 'Eye rolls and chuckles', 'Applause and boos'],
            'absurdist': ['Confused laughter', 'Someone shouts "What?!"', 'Bewildered applause', 'Silence then sudden laughter']
        }
        
        return random.choice(reactions.get(comedian_style, ['Polite applause']))
    
    def run_comedy_set(self, duration_minutes: int = 15, max_exchanges: int = 12):
        """Run a comedy club simulation"""
        print("🎤 " + "="*50)
        print("🎭 WELCOME TO THE COMEDY CLUB SIMULATION!")
        print("🎤 " + "="*50)
        
        show_manager = self.create_comedy_show_manager()
        comedian_order = list(self.agents.keys())
        random.shuffle(comedian_order)
        
        conversation_log = []
        
        # Opening
        opening_message = """
        🎤 Good evening everyone! Welcome to our special AI Comedy Club night! 
        We have four fantastic comedians for you tonight, each with their own unique style.
        Let's start with our first comedian!
        
        Who wants to open the show with their best material?
        """
        
        print(f"\\n🎙️ Show Manager: {opening_message}")
        conversation_log.append({
            "timestamp": datetime.now().isoformat(),
            "speaker": "Show_Manager", 
            "message": opening_message,
            "type": "introduction"
        })
        
        # Main show loop
        for round_num in range(max_exchanges // len(self.agents)):
            print(f"\\n🎭 === ROUND {round_num + 1} ===")
            
            for i, style in enumerate(comedian_order):
                comedian = self.agents[style]
                
                # Create a topic for this comedian
                if round_num == 0:
                    if style == 'observational':
                        topic = "everyday technology and how confusing it is"
                    elif style == 'dark':
                        topic = "the positive sides of terrible life events"
                    elif style == 'wordplay':
                        topic = "animals and their secret lives"
                    else:  # absurdist
                        topic = "what if inanimate objects had feelings"
                else:
                    # Build on previous comedian's topic
                    topic = f"responding to the previous comedian's material about {conversation_log[-1].get('topic', 'comedy')}"
                
                print(f"\\n🎤 {comedian.name} is up next! Topic: {topic}")
                
                # Get the comedian's performance
                prompt = f"""You're performing at a comedy club right now. The audience is {self.club_atmosphere}. 
                
                Your topic: {topic}
                
                Deliver 1-2 of your best jokes on this topic. Keep it short, punchy, and appropriate for your comedy style.
                End by setting up the next comedian or asking the audience a question."""
                
                try:
                    response = comedian.generate_reply(
                        messages=[{"role": "user", "content": prompt}]
                    )
                    
                    # Log the performance
                    performance_log = {
                        "timestamp": datetime.now().isoformat(),
                        "speaker": comedian.name,
                        "style": style,
                        "topic": topic,
                        "message": response,
                        "type": "performance"
                    }
                    conversation_log.append(performance_log)
                    
                    # Display performance
                    print(f"\\n🎭 {comedian.name}: {response}")
                    
                    # Simulate audience reaction
                    reaction = self.simulate_audience_reaction(response, style)
                    print(f"👏 Audience: {reaction}")
                    
                    performance_log["audience_reaction"] = reaction
                    
                    # Brief pause between comedians
                    time.sleep(1)
                    
                except Exception as e:
                    print(f"❌ Error with {comedian.name}: {e}")
                    continue
        
        # Closing
        closing_message = """
        🎤 That's our show for tonight! Let's give a big round of applause to all our comedians!
        Thank you for joining us at the AI Comedy Club! 
        """
        
        print(f"\\n🎙️ Show Manager: {closing_message}")
        conversation_log.append({
            "timestamp": datetime.now().isoformat(),
            "speaker": "Show_Manager",
            "message": closing_message,
            "type": "closing"
        })
        
        # Save the show
        self.save_show_log(conversation_log)
        return conversation_log
    
    def save_show_log(self, conversation_log: List[Dict]):
        """Save the comedy show log"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"comedy_club_show_{timestamp}.json"
        
        show_data = {
            "metadata": {
                "show_date": datetime.now().isoformat(),
                "total_performances": len([log for log in conversation_log if log["type"] == "performance"]),
                "comedians": list(self.agents.keys()),
                "duration_minutes": (len(conversation_log) * 2),  # Rough estimate
            },
            "show_log": conversation_log
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(show_data, f, indent=2, ensure_ascii=False)
        
        print(f"\\n💾 Show saved to {filename}")
        return filename

def main():
    """Main function to run the comedy club simulation"""
    print("🚀 Starting Comedy Club Simulation...")
    
    # Initialize the simulator
    try:
        club = ComedyClubSimulator()
        
        # Run the show
        show_log = club.run_comedy_set(duration_minutes=20, max_exchanges=8)
        
        print("\\n🎉 Comedy Club simulation completed successfully!")
        print(f"📊 Total interactions: {len(show_log)}")
        
    except FileNotFoundError:
        print("❌ categorized_jokes.json not found. Please run joke_categorizer.py first.")
    except Exception as e:
        print(f"❌ Error running simulation: {e}")

if __name__ == "__main__":
    main()
