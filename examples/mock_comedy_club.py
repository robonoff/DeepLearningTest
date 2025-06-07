#!/usr/bin/env python3
"""
Mock Comedy Club Simulator
Shows the full system working with pre-written jokes instead of LLM calls
This demonstrates the simulation framework while we debug Ollama issues
"""

import random
import time
from datetime import datetime
import json

class MockComedyClub:
    """Mock comedy club with pre-written jokes to demonstrate the system"""
    
    def __init__(self):
        # Pre-written jokes for each comedian style
        self.comedian_jokes = {
            'Jerry_Observational': [
                "What's the deal with video calls? Half the meeting is just people saying 'Can you hear me?' and 'You're on mute!' Am I right?",
                "You ever notice how we have a computer in our pocket that can access all human knowledge, but we use it to watch videos of cats? What's up with that?",
                "I ordered something online and it said 'Same day delivery' - turned out to be 11:59 PM. Technically correct, but come on! Am I right?",
            ],
            'Raven_Dark': [
                "I love how social media shows us 'memories from this day.' Yeah, thanks for reminding me how much better I looked five years ago. Too dark? Good.",
                "My phone battery dies faster than my motivation on Monday mornings. At least the phone can be recharged. Too dark? Good.",
                "They say laughter is the best medicine. Good thing, because I can't afford actual medicine. Too dark? Good.",
            ],
            'Penny_Wordplay': [
                "Why don't programmers like nature? It has too many bugs! Get it? Because debugging... and actual bugs!",
                "I tried to catch some fog earlier. I mist! Get it? Because missed sounds like mist, and fog is misty!",
                "What do you call a fake noodle? An impasta! Get it? Because impostor plus pasta equals impasta!",
            ],
            'Cosmic_Absurd': [
                "What if WiFi routers are just tiny alien communication devices, and we're all unknowingly helping extraterrestrials coordinate their invasion plans? Think about it - they're everywhere now!",
                "Imagine if elevators were sentient and got tired of carrying people. One day they'd just say 'Take the stairs, I'm having an existential crisis about vertical transportation.'",
                "What if autocorrect isn't trying to fix our typos, but actually an AI trying to rewrite human language one text at a time? We're all just beta testers for the robot takeover!",
            ]
        }
        
        self.topics = [
            "smartphones and technology",
            "coffee shops and daily routines", 
            "social media behavior",
            "online shopping and delivery",
            "video calls and remote work",
            "streaming services and binge watching"
        ]
        
        self.audience_reactions = [
            "😂 *Burst of laughter*",
            "👏 *Enthusiastic applause*", 
            "😅 *Nervous chuckles*",
            "🤔 *Confused but amused*",
            "😆 *Audience member shouts 'So true!'*",
            "🙄 *Groans and laughter*",
            "😮 *Surprised gasps then laughter*"
        ]
    
    def get_comedian_joke(self, comedian_name: str) -> str:
        """Get a random joke from the comedian's repertoire"""
        jokes = self.comedian_jokes.get(comedian_name, ["I forgot my joke! *awkward silence*"])
        return random.choice(jokes)
    
    def simulate_show(self, rounds: int = 3):
        """Run the mock comedy show"""
        print("🎭" + "="*70)
        print("🎤 WELCOME TO THE MOCK AI COMEDY CLUB!")
        print("🎭 (Demonstrating system while debugging Ollama)")
        print("🎭" + "="*70)
        
        comedians = list(self.comedian_jokes.keys())
        show_log = []
        
        # Opening
        print(f"\n🎙️ Show Manager: Good evening everyone! We have four fantastic AI comedians tonight!")
        print("🎙️ Show Manager: Let's get this show started!")
        
        for round_num in range(rounds):
            topic = random.choice(self.topics)
            print(f"\n🎭 === ROUND {round_num + 1} ===")
            print(f"🎯 Tonight's topic: {topic}")
            
            # Shuffle order for variety
            current_order = comedians.copy()
            random.shuffle(current_order)
            
            for comedian in current_order:
                print(f"\n🎤 {comedian} takes the stage!")
                print(f"🎯 Topic: {topic}")
                
                # Add small delay for realism
                time.sleep(1)
                
                # Get and display the joke
                joke = self.get_comedian_joke(comedian)
                print(f"🎭 {comedian}: {joke}")
                
                # Log the performance
                show_log.append({
                    "round": round_num + 1,
                    "comedian": comedian,
                    "topic": topic,
                    "joke": joke,
                    "timestamp": datetime.now().isoformat()
                })
                
                # Simulate audience reaction
                reaction = random.choice(self.audience_reactions)
                print(f"👥 Audience: {reaction}")
                
                # Brief pause between comedians
                time.sleep(1.5)
        
        # Closing
        print(f"\n🎙️ Show Manager: That's our show! Let's give a big round of applause!")
        print("👏 *Standing ovation*")
        print("🎭" + "="*70)
        print("🎉 THANK YOU FOR COMING TO THE MOCK AI COMEDY CLUB!")
        print("🎭" + "="*70)
        
        # Save show log
        self.save_show_log(show_log)
        
        return show_log
    
    def save_show_log(self, show_log):
        """Save the show log"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"mock_comedy_show_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump({
                "show_type": "mock_demonstration",
                "total_performances": len(show_log),
                "show_date": datetime.now().isoformat(),
                "performances": show_log
            }, f, indent=2)
        
        print(f"💾 Show saved to {filename}")

def main():
    """Main function"""
    print("🚀 Starting Mock Comedy Club Demonstration...")
    print("📝 This shows how the system works while we debug Ollama")
    
    try:
        club = MockComedyClub()
        club.simulate_show(rounds=2)
        
        print("\n✅ Mock simulation completed successfully!")
        print("🔧 Once Ollama is working, this will use real AI responses")
        
    except KeyboardInterrupt:
        print("\n⏹️ Show interrupted by user")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
