#!/usr/bin/env python3
"""
Comedy Club Visual Interface
Creates an animated visualization of the comedy club simulation
Similar to Agent Hospital but for a comedy club environment
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import json
import threading
import time
from datetime import datetime
from typing import Dict, List
import random

class ComedyClubGUI:
    """Visual interface for the comedy club simulation"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("🎭 AI Comedy Club Simulation")
        self.root.geometry("1200x800")
        self.root.configure(bg='#1a1a1a')  # Dark comedy club theme
        
        # Simulation state
        self.is_running = False
        self.is_paused = False  # New pause state for individual jokes
        self.current_show_log = []
        self.current_performer = None
            self.update_current_performance("Show Manager", f"🧠 {rag_status} initialized")
            self.update_current_performance("Show Manager", "✅ Connected! Starting performance...")
            self.show_info.config(text=f"Show started: {datetime.now().strftime('%H:%M:%S')}")
            
            # Start immediately without any delay
            self.run_visual_show(club)
    
    def __init__(self, root):
        self.root = root
        self.root.title("🎭 AI Comedy Club Simulation")
        self.root.geometry("1200x800")
        self.root.configure(bg='#1a1a1a')  # Dark comedy club theme
        
        # Simulation state
        self.is_running = False
        self.is_paused = False  # New pause state for individual jokes
        self.current_show_log = []
        self.current_performer = None
        
        # Comedian colors for visual distinction
        self.comedian_colors = {
            'Jerry_Observational': '#FF6B6B',    # Red
            'Raven_Dark': '#4ECDC4',             # Teal  
            'Penny_Wordplay': '#45B7D1',         # Blue
            'Cosmic_Absurd': '#96CEB4',          # Green
            'Show_Manager': '#FECA57'            # Yellow
        }
        
        self.setup_gui()
    
    def setup_gui(self):
        """Setup the main GUI layout"""
        
        # Main title
        title_frame = tk.Frame(self.root, bg='#1a1a1a')
        title_frame.pack(fill='x', padx=10, pady=5)
        
        title_label = tk.Label(
            title_frame, 
            text="🎭 AI COMEDY CLUB SIMULATION", 
            font=('Arial', 20, 'bold'),
            fg='#FECA57',
            bg='#1a1a1a'
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            title_frame,
            text="Four AI Comedians • Live Performance Simulation",
            font=('Arial', 12),
            fg='#95a5a6',
            bg='#1a1a1a'
        )
        subtitle_label.pack()
        
        # Main content area - only stage (no log area)
        main_frame = tk.Frame(self.root, bg='#1a1a1a')
        main_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Only the stage area (log area removed)
        self.setup_stage_area(main_frame)
        
        # Bottom controls
        self.setup_controls()
    
    def setup_stage_area(self, parent):
        """Setup the visual stage area"""
        stage_frame = tk.Frame(parent, bg='#2c3e50', relief='raised', bd=2)
        stage_frame.pack(fill='both', expand=True)  # Fill entire area
        
        # Stage title
        stage_title = tk.Label(
            stage_frame,
            text="🎤 COMEDY CLUB STAGE",
            font=('Arial', 14, 'bold'),
            fg='white',
            bg='#000080'
        )
        stage_title.pack(pady=5)
        
        # Show info
        self.show_info = tk.Label(
            stage_frame,
            text="No show running",
            font=('Arial', 10),
            fg='#95a5a6',
            bg='#2c3e50'
        )
        self.show_info.pack(pady=2)
        
        # Comedian status area
        self.comedian_frame = tk.Frame(stage_frame, bg='#2c3e50')
        self.comedian_frame.pack(fill='x', padx=10, pady=5)
        
        # Create comedian status widgets
        self.comedian_widgets = {}
        comedians = [
            ('Jerry_Observational', '🤵 Jerry\\n(Observational)', '#FF6B6B'),
            ('Raven_Dark', '🖤 Raven\\n(Dark Humor)', '#4ECDC4'),
            ('Penny_Wordplay', '🎯 Penny\\n(Wordplay)', '#45B7D1'),
            ('Cosmic_Absurd', '🌌 Cosmic\\n(Absurdist)', '#96CEB4')
        ]
        
        for i, (name, display, color) in enumerate(comedians):
            row = i // 2
            col = i % 2
            
            comedian_widget = tk.Frame(self.comedian_frame, bg=color, relief='raised', bd=2)
            comedian_widget.grid(row=row, column=col, padx=5, pady=5, sticky='ew')
            
            status_label = tk.Label(
                comedian_widget,
                text=display,
                font=('Arial', 10, 'bold'),
                fg='white',
                bg=color
            )
            status_label.pack(pady=5)
            
            activity_label = tk.Label(
                comedian_widget,
                text="💤 Waiting",
                font=('Arial', 9),
                fg='white',
                bg=color
            )
            activity_label.pack()
            
            self.comedian_widgets[name] = {
                'frame': comedian_widget,
                'status': status_label,
                'activity': activity_label,
                'color': color
            }
        
        # Configure grid weights
        self.comedian_frame.columnconfigure(0, weight=1)
        self.comedian_frame.columnconfigure(1, weight=1)
        
        # Current performance area
        perf_frame = tk.Frame(stage_frame, bg='#34495e', relief='sunken', bd=2)
        perf_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        perf_title = tk.Label(
            perf_frame,
            text="🎭 CURRENT PERFORMANCE",
            font=('Arial', 12, 'bold'),
            fg='white',
            bg='#34495e'
        )
        perf_title.pack(pady=5)
        
        self.current_performance = scrolledtext.ScrolledText(
            perf_frame,
            height=15,  # Increased height
            width=80,   # Increased width
            font=('Arial', 12),  # Larger font
            bg='#2c3e50',
            fg='white',
            insertbackground='white',
            state='disabled',
            wrap=tk.WORD  # Word wrap for better readability
        )
        self.current_performance.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Audience reaction
        reaction_frame = tk.Frame(stage_frame, bg='#2c3e50')
        reaction_frame.pack(fill='x', padx=10, pady=5)
        
        reaction_title = tk.Label(
            reaction_frame,
            text="👏 AUDIENCE REACTION",
            font=('Arial', 10, 'bold'),
            fg='white',
            bg='#2c3e50'
        )
        reaction_title.pack()
        
        self.audience_reaction = tk.Label(
            reaction_frame,
            text="🤐 Silence...",
            font=('Arial', 12),
            fg='#95a5a6',
            bg='#2c3e50',
            wraplength=400
        )
        self.audience_reaction.pack(pady=5)
    
    def setup_log_area(self, parent):
        """Setup the performance log area"""
        log_frame = tk.Frame(parent, bg='#34495e', relief='raised', bd=2)
        log_frame.pack(side='right', fill='both', expand=True, padx=(5, 0))
        
        # Log title
        log_title = tk.Label(
            log_frame,
            text="📝 SHOW LOG",
            font=('Arial', 14, 'bold'),
            fg='white',
            bg='#34495e'
        )
        log_title.pack(pady=5)
        
        # Show info
        self.show_info = tk.Label(
            log_frame,
            text="No show running",
            font=('Arial', 10),
            fg='#95a5a6',
            bg='#34495e'
        )
        self.show_info.pack(pady=2)
        
        # Log text area
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            height=25,
            width=50,
            font=('Consolas', 9),
            bg='#2c3e50',
            fg='white',
            insertbackground='white',
            state='disabled'
        )
        self.log_text.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Configure text tags for colored output
        for name, color in self.comedian_colors.items():
            self.log_text.tag_config(name, foreground=color, font=('Consolas', 9, 'bold'))
    
    def setup_controls(self):
        """Setup control buttons"""
        control_frame = tk.Frame(self.root, bg='#1a1a1a')
        control_frame.pack(fill='x', padx=10, pady=5)
        
        # Control buttons
        self.start_button = tk.Button(
            control_frame,
            text="🎬 Start Show",
            command=self.start_show,
            font=('Arial', 12, 'bold'),
            bg='#27ae60',
            fg='white',
            padx=20,
            pady=5
        )
        self.start_button.pack(side='left', padx=5)
        
        self.stop_button = tk.Button(
            control_frame,
            text="⏹️ Stop Show", 
            command=self.stop_show,
            font=('Arial', 12, 'bold'),
            bg='#e74c3c',
            fg='white',
            padx=20,
            pady=5,
            state='disabled'
        )
        self.stop_button.pack(side='left', padx=5)
        
        # Pause/Play button for individual jokes
        self.pause_button = tk.Button(
            control_frame,
            text="⏸️ Pause Reading",
            command=self.toggle_pause,
            font=('Arial', 12, 'bold'),
            bg='#f39c12',
            fg='white',
            padx=20,
            pady=5,
            state='disabled'
        )
        self.pause_button.pack(side='left', padx=5)
        
        # Topic input
        tk.Label(
            control_frame,
            text="Topic:",
            font=('Arial', 10),
            fg='white',
            bg='#1a1a1a'
        ).pack(side='left', padx=(20, 5))
        
        self.topic_entry = tk.Entry(
            control_frame,
            font=('Arial', 10),
            width=25,
            bg='#2c3e50',
            fg='white',
            insertbackground='white'
        )
        self.topic_entry.pack(side='left', padx=5)
        self.topic_entry.insert(0, "technology")  # Default topic
        
        # RAG Controls
        rag_frame = tk.Frame(control_frame, bg='#1a1a1a')
        rag_frame.pack(side='left', padx=(20, 5))
        
        tk.Label(
            rag_frame,
            text="🧠 RAG:",
            font=('Arial', 10, 'bold'),
            fg='#4ECDC4',
            bg='#1a1a1a'
        ).pack()
        
        self.web_search_var = tk.BooleanVar(value=True)
        self.web_search_check = tk.Checkbutton(
            rag_frame,
            text="🌐 Web Search",
            variable=self.web_search_var,
            font=('Arial', 9),
            fg='white',
            bg='#1a1a1a',
            selectcolor='#2c3e50'
        )
        self.web_search_check.pack()
        
        self.load_button = tk.Button(
            control_frame,
            text="📂 Load Show Log",
            command=self.load_show_log,
            font=('Arial', 12),
            bg='#3498db',
            fg='white',
            padx=20,
            pady=5
        )
        self.load_button.pack(side='left', padx=(20, 5))
        
        # Status indicator
        self.status_label = tk.Label(
            control_frame,
            text="Ready to start",
            font=('Arial', 10),
            fg='#95a5a6',
            bg='#1a1a1a'
        )
        self.status_label.pack(side='right', padx=10)
    
    def start_show(self):
        """Start a new comedy show simulation"""
        if self.is_running:
            return
        
        self.is_running = True
        self.is_paused = False
        self.start_button.config(state='disabled')
        self.stop_button.config(state='normal')
        self.pause_button.config(state='normal', text="⏸️ Pause Reading", bg='#f39c12')
        self.status_label.config(text="Show in progress...", fg='#f39c12')
        
        # Clear previous content
        self.clear_displays()
        
        # Start simulation in separate thread
        self.simulation_thread = threading.Thread(target=self.run_simulation, daemon=True)
        self.simulation_thread.start()
    
    def stop_show(self):
        """Stop the current show"""
        self.is_running = False
        self.is_paused = False
        self.start_button.config(state='normal')
        self.stop_button.config(state='disabled')
        self.pause_button.config(state='disabled', text="⏸️ Pause Reading")
        self.status_label.config(text="Show stopped", fg='#e74c3c')
        
        # Reset comedian status
        for name, widget in self.comedian_widgets.items():
            widget['activity'].config(text="💤 Waiting")
    
    def toggle_pause(self):
        """Toggle pause state for reading jokes"""
        if self.is_paused:
            self.is_paused = False
            self.pause_button.config(text="⏸️ Pause Reading", bg='#f39c12')
            self.status_label.config(text="Show resumed...", fg='#27ae60')
        else:
            self.is_paused = True
            self.pause_button.config(text="▶️ Continue Reading", bg='#27ae60')
            self.status_label.config(text="Reading paused...", fg='#f39c12')
    
    def smart_sleep(self, seconds):
        """Sleep that respects pause state - checks every 0.5 seconds"""
        total_time = 0
        while total_time < seconds and self.is_running:
            if not self.is_paused:
                time.sleep(0.5)
                total_time += 0.5
            else:
                # While paused, just check every 0.1 seconds
                time.sleep(0.1)
    
    def clear_displays(self):
        """Clear all display areas"""
        # Only clear the performance area since we removed the log
        self.current_performance.config(state='normal')
        self.current_performance.delete(1.0, tk.END)
        self.current_performance.config(state='disabled')
        
        self.audience_reaction.config(text="🤐 Silence...")
    
    def run_simulation(self):
        """Run the actual comedy simulation"""
        try:
            # Import and run the simulation with Orfeo
            import sys
            import os
            sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
            
            # Show immediate feedback
            self.update_current_performance("Show Manager", "🚀 Starting show immediately...")
            
            # Import and initialize
            from src.core.comedy_club_clean import ComedyClub
            self.update_current_performance("Show Manager", "🔗 Connecting to Orfeo cluster...")
            
            club = ComedyClub()
            
            self.update_current_performance("Show Manager", "✅ Connected! Starting performance...")
            self.show_info.config(text=f"Show started: {datetime.now().strftime('%H:%M:%S')}")
            
            # Start immediately without any delay
            self.run_visual_show(club)
            
        except Exception as e:
            self.update_current_performance("Error", f"System error: {e}")
        finally:
            if self.is_running:
                self.stop_show()
    
    def run_visual_show(self, club):
        """Run the show with visual updates and comedian debates"""
        # Get the user-specified topic
        user_topic = self.topic_entry.get().strip() or "general comedy"
        
        # Get the comedians list and shuffle for performance order
        comedian_names = list(club.comedians.keys())
        random.shuffle(comedian_names)
        
        # Opening - start immediately
        self.update_audience_reaction("🎤 Welcome to the AI Comedy Club!")
        self.update_current_performance("Show Manager", f"🎯 Topic: '{user_topic.upper()}' - Let's go!")
        # No delay - start immediately
        
        # Store jokes for debates
        round_jokes = []
        
        # Main show with debates
        for round_num in range(2):  # 2 rounds
            if not self.is_running:
                break
                
            self.update_current_performance("Show Manager", f"🎭 ROUND {round_num + 1} - Topic: {user_topic}")
            # Start round immediately
            
            # Each comedian performs on the user's topic
            current_round_jokes = []
            
            for comedian_name in comedian_names:
                if not self.is_running:
                    break
                
                # Map GUI names to clean names
                gui_name = comedian_name
                if comedian_name == "Jerry":
                    gui_name = "Jerry_Observational"
                elif comedian_name == "Raven":
                    gui_name = "Raven_Dark"
                elif comedian_name == "Penny":
                    gui_name = "Penny_Wordplay"
                elif comedian_name == "Cosmic":
                    gui_name = "Cosmic_Absurd"
                
                # Update status
                self.update_comedian_status(gui_name, "🎤 Performing")
                
                # Show that we're generating
                self.update_current_performance(comedian_name, "🤔 Thinking of a joke...")
                
                # Get performance with user's topic
                try:
                    joke = club.get_joke(comedian_name, user_topic)
                    
                    # Store joke for debates
                    current_round_jokes.append({
                        'comedian': comedian_name,
                        'gui_name': gui_name,
                        'joke': joke
                    })
                    
                    # Display performance
                    self.update_current_performance(comedian_name, joke)
                    
                    # Simulate audience reaction based on comedian style
                    comedian_info = club.comedians[comedian_name]
                    reactions = {
                        'observational humor': ["😂 Big laughs!", "👏 Standing ovation!", "🤣 Audience loves it!"],
                        'dark humor': ["😬 Nervous laughter", "😨 Gasps then applause", "🖤 Dark humor appreciated"],
                        'wordplay and puns': ["🙄 Groans and laughs", "📚 Dad joke energy!", "🎯 Pun perfection!"],
                        'absurd and surreal humor': ["🤔 Confused laughter", "🌌 Mind = blown", "👽 What just happened?!"]
                    }
                    
                    reaction = random.choice(reactions.get(comedian_info['style'], ["👏 Polite applause"]))
                    self.update_audience_reaction(reaction)
                    
                    # Shorter time for jokes in first round to speed up start
                    if round_num == 0:
                        self.smart_sleep(15)  # 15 seconds for first round jokes
                    else:
                        self.smart_sleep(30)  # 30 seconds for later rounds
                    
                except Exception as e:
                    self.update_current_performance("Error", f"{comedian_name} had technical difficulties: {e}")
                
                finally:
                    self.update_comedian_status(gui_name, "💤 Waiting")
            
            # Now the debate phase!
            if len(current_round_jokes) > 1 and self.is_running:
                self.update_current_performance("Show Manager", "💬 DEBATE TIME - Each comedian gets ONE response!")
                # No delay - instant debate announcement
                
                # Each comedian responds to another's joke (ONE TIME ONLY)
                for i, performer in enumerate(current_round_jokes):
                    if not self.is_running:
                        break
                    
                    # Pick someone else's joke to respond to
                    other_jokes = [j for j in current_round_jokes if j['comedian'] != performer['comedian']]
                    if other_jokes:
                        target_joke = random.choice(other_jokes)
                        
                        # Update status
                        self.update_comedian_status(performer['gui_name'], "💭 Responding")
                        
                        # Show that we're generating a response
                        self.update_current_performance(f"{performer['comedian']}", "💭 Crafting a comeback...")
                        
                        try:
                            # Create a debate prompt
                            debate_prompt = f"React to this joke about {user_topic} from another comedian as a {club.comedians[performer['comedian']]['style']} comedian: '{target_joke['joke']}'. Give a witty comeback or build on it with your own joke style. Keep it to 1-2 sentences."
                            
                            response = club.client.generate(debate_prompt, max_tokens=100)
                            
                            self.update_current_performance(f"{performer['comedian']} responds to {target_joke['comedian']}", response)
                            
                            # Audience loves debates!
                            debate_reactions = ["🔥 Burn!", "😂 Great comeback!", "👏 Brilliant response!", "🎭 Comedy gold!"]
                            reaction = random.choice(debate_reactions)
                            self.update_audience_reaction(reaction)
                            
                            # Shorter time for debate responses in first round
                            if round_num == 0:
                                self.smart_sleep(15)  # 15 seconds for first round debates
                            else:
                                self.smart_sleep(30)  # 30 seconds for later rounds
                            
                        except Exception as e:
                            self.update_current_performance("Error", f"{performer['comedian']} couldn't respond: {e}")
                        
                        finally:
                            self.update_comedian_status(performer['gui_name'], "💤 Waiting")
                
                # End debate phase explicitly
                self.update_current_performance("Show Manager", "🎪 End of debate for this round!")
                # No delay - instant end message
            
            round_jokes.extend(current_round_jokes)
            
            if round_num < 1 and self.is_running:  # Only pause between rounds, not after last
                self.update_current_performance("Show Manager", "⏸️ Brief intermission...")
                # No delay - instant intermission
        
        # Closing
        if self.is_running:
            self.update_current_performance("Show Manager", f"🎉 That's our show! Tonight's topic '{user_topic}' brought out the best in our comedians!")
            self.update_audience_reaction("👏🎉 THUNDEROUS APPLAUSE! 🎉👏")
    
    def update_comedian_status(self, comedian_name, status):
        """Update a comedian's status display"""
        if comedian_name in self.comedian_widgets:
            self.root.after(0, lambda: self.comedian_widgets[comedian_name]['activity'].config(text=status))
    
    def update_current_performance(self, comedian_name, performance):
        """Update the current performance display"""
        def update():
            self.current_performance.config(state='normal')
            self.current_performance.delete(1.0, tk.END)
            # Don't add comedian name if it's already in the performance text
            if performance.startswith(comedian_name) or ":" in performance.split('\n')[0]:
                self.current_performance.insert(tk.END, performance)
            else:
                self.current_performance.insert(tk.END, f"{comedian_name}:\n{performance}")
            self.current_performance.config(state='disabled')
        
        self.root.after(0, update)
    
    def update_audience_reaction(self, reaction):
        """Update the audience reaction display"""
        self.root.after(0, lambda: self.audience_reaction.config(text=reaction))
    
    def add_log(self, message, speaker="System"):
        """Add a message to the log - disabled since log area was removed"""
        # Log area was removed, so this method does nothing now
        pass
    
    def load_show_log(self):
        """Load a previous show log"""
        from tkinter import filedialog
        
        filename = filedialog.askopenfilename(
            title="Load Comedy Show Log",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                self.clear_displays()
                self.show_info.config(text=f"Loaded: {filename.split('/')[-1]}")
                
                # Display the loaded show
                for entry in data.get('show_log', []):
                    speaker = entry.get('speaker', 'Unknown')
                    message = entry.get('message', '')
                    self.add_log(message, speaker)
                
                self.status_label.config(text="Show log loaded", fg='#27ae60')
                
            except Exception as e:
                self.add_log(f"❌ Error loading file: {e}", "Show_Manager")

def main():
    """Main function to run the GUI"""
    root = tk.Tk()
    app = ComedyClubGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
