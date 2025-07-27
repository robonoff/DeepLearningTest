#!/usr/bin/env python3
"""
Comedy Club Visual Interface with Human Rating System
Creates an animated visualization of the comedy club with joke rating capabilities
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import json
import threading
import time
from datetime import datetime
from typing import Dict, List, Optional
import random

# Import our human rating system
try:
    from src.utils.human_rating import HumanRatingSystem
except ImportError:
    print("⚠️ Human rating system not found. Some features may be limited.")
    HumanRatingSystem = None

class ComedyClubGUI:
    """Visual interface for the comedy club simulation with human rating"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("🎭 AI Comedy Club Simulation with Rating")
        self.root.geometry("1400x900")
        self.root.configure(bg='#f3ece6')  # Light comedy club theme
        
        # Initialize rating system
        if HumanRatingSystem:
            self.rating_system = HumanRatingSystem()
        else:
            self.rating_system = None
        
        # Simulation state
        self.is_running = False
        self.is_paused = False  # New pause state for individual jokes
        self.current_show_log = []
        self.current_performer = None
        self.current_joke_data = None  # Store current joke for rating
        
        # Comedian colors for visual distinction
        self.comedian_colors = {
            'Dave_Observational': "#F10000",    # Red - Edgy Dave
            'Mike_Dark': "#06001D",             # Teal - Dark Mike  
            'Sarah_Wordplay': "#87CF8A",         # Blue - Sharp Sarah
            'Lisa_Absurd': "#9C0060",          # Green - Weird Lisa
            'Show_Manager': '#FECA57'            # Yellow
        }
        
        self.setup_gui()
    
    def setup_gui(self):
        """Setup the main GUI layout"""
        
        # Main title
        title_frame = tk.Frame(self.root, bg='#f3ece6')
        title_frame.pack(fill='x', padx=10, pady=5)
        
        title_label = tk.Label(
            title_frame, 
            text="🎭 AI COMEDY CLUB SIMULATION", 
            font=('Arial', 20, 'bold'),
            fg="#002555",
            bg="#f3ece6"
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            title_frame,
            text="Four AI Comedians • Live Performance Simulation",
            font=('Arial', 12),
            fg="#002555",
            bg='#f3ece6'
        )
        subtitle_label.pack()
        
        # Main content area - only stage (no log area)
        main_frame = tk.Frame(self.root, bg='#f3ece6')
        main_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Only the stage area (log area removed)
        self.setup_stage_area(main_frame)
        
        # Bottom controls
        self.setup_controls()
    
    def setup_stage_area(self, parent):
        """Setup the visual stage area"""
        stage_frame = tk.Frame(parent, bg='#f3ece6', relief='raised', bd=2)
        stage_frame.pack(fill='both', expand=True)  # Fill entire area
        
        # Stage title
        stage_title = tk.Label(
            stage_frame,
            text="🎤 COMEDY CLUB STAGE",
            font=('Arial', 14, 'bold'),
            fg="#002555",
            bg='#f3ece6'
        )
        stage_title.pack(pady=5)
        
        # Show info
        self.show_info = tk.Label(
            stage_frame,
            text="No show running",
            font=('Arial', 10),
            fg='#002555',
            bg='#95a5a6'
        )
        self.show_info.pack(pady=2)
        
        # Comedian status area
        self.comedian_frame = tk.Frame(stage_frame, bg='#f3ece6')
        self.comedian_frame.pack(fill='x', padx=10, pady=5)
        
        # Create comedian status widgets
        self.comedian_widgets = {}
        comedians = [
            ('Dave_Observational', '🔥 Dave\n(Brutally Honest Observer)', '#FF6B6B'),
            ('Mike_Dark', '🖤 Mike\n(Dark Family Man)', '#4ECDC4'),
            ('Sarah_Wordplay', '⚡ Sarah\n(Feminist Wordsmith)', '#45B7D1'),
            ('Lisa_Absurd', '🧪 Lisa\n(Mad Scientist Comic)', '#96CEB4')
        ]
        
        for i, (name, display, color) in enumerate(comedians):
            row = i // 2
            col = i % 2
            
            comedian_widget = tk.Frame(self.comedian_frame, bg=color, relief='raised', bd=2)
            comedian_widget.grid(row=row, column=col, padx=5, pady=5, sticky='ew')
            
            status_label = tk.Label(
                comedian_widget,
                text=display,
                font=('Times New Roman', 10, 'bold'),
                fg='white',
                bg=color
            )
            status_label.pack(pady=5)
            
            activity_label = tk.Label(
                comedian_widget,
                text="💤 Waiting",
                font=('Times New Roman', 9),
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
            bg='#002555',
            fg='white',
            insertbackground='white',
            state='disabled',
            wrap=tk.WORD  # Word wrap for better readability
        )
        self.current_performance.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Audience reaction
        reaction_frame = tk.Frame(stage_frame, bg='#f3ece6')
        reaction_frame.pack(fill='x', padx=10, pady=5)
        
        reaction_title = tk.Label(
            reaction_frame,
            text="👏 AUDIENCE REACTION",
            font=('Arial', 10, 'bold'),
            fg='#002555',
            bg='#f3ece6'
        )
        reaction_title.pack()
        
        self.audience_reaction = tk.Label(
            reaction_frame,
            text="🤐 Silence...",
            font=('Arial', 12),
            fg='#002555',
            bg='#f3ece6',
            wraplength=400
        )
        self.audience_reaction.pack(pady=5)
        
        # Human Rating Area
        self.setup_rating_area(stage_frame)
    
    def setup_rating_area(self, parent):
        """Setup the human rating area for jokes"""
        if not self.rating_system:
            return
            
        rating_frame = tk.Frame(parent, bg='#bdc3c7', relief='raised', bd=2)
        rating_frame.pack(fill='x', padx=10, pady=5)
        
        # Rating title
        rating_title = tk.Label(
            rating_frame,
            text="⭐ RATE THIS JOKE ⭐",
            font=('Arial', 12, 'bold'),
            fg='#002555',
            bg='#bdc3c7'
        )
        rating_title.pack(pady=5)
        
        # Rating buttons frame
        buttons_frame = tk.Frame(rating_frame, bg='#bdc3c7')
        buttons_frame.pack(pady=5)
        
        # Rating buttons with emojis and colors
        self.rating_buttons = {}
        rating_options = [
            ("😍", "love", "#27ae60", "LOVE IT!"),
            ("👍", "like", "#2ecc71", "Like"),
            ("😐", "meh", "#7f8c8d", "Meh"),
            ("👎", "dislike", "#e74c3c", "Dislike"),
            ("🤮", "hate", "#c0392b", "HATE IT!")
        ]
        
        for emoji, rating, color, text in rating_options:
            btn = tk.Button(
                buttons_frame,
                text=f"{emoji}\n{text}",
                command=lambda r=rating: self.rate_current_joke(r),
                font=('Arial', 9, 'bold'),
                bg=color,
                fg='white',
                width=8,
                height=3,
                state='disabled'  # Initially disabled
            )
            btn.pack(side='left', padx=3)
            self.rating_buttons[rating] = btn
        
        # Comment entry
        comment_frame = tk.Frame(rating_frame, bg='#bdc3c7')
        comment_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(
            comment_frame,
            text="💬 Comment (optional):",
            font=('Arial', 9),
            fg='#002555',
            bg='#bdc3c7'
        ).pack(anchor='w')
        
        self.comment_entry = tk.Entry(
            comment_frame,
            font=('Arial', 9),
            bg='#34495e',
            fg='white',
            insertbackground='white'
        )
        self.comment_entry.pack(fill='x', pady=2)
        
        # Rating status
        self.rating_status = tk.Label(
            rating_frame,
            text="🎭 No joke to rate yet...",
            font=('Arial', 9),
            fg='#002555',
            bg='#bdc3c7'
        )
        self.rating_status.pack(pady=2)
    
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
            bg='#002555',
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
        control_frame = tk.Frame(self.root, bg='#f3ece6')
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
            fg='#002555',
            bg='#f3ece6'
        ).pack(side='left', padx=(20, 5))
        
        self.topic_entry = tk.Entry(
            control_frame,
            font=('Arial', 10),
            width=25,
            bg='#002555',
            fg='white',
            insertbackground='white'
        )
        self.topic_entry.pack(side='left', padx=5)
        self.topic_entry.insert(0, "technology")  # Default topic
        
        # RAG Controls
        self.web_search_var = tk.BooleanVar(value=True)
        self.web_search_check = tk.Checkbutton(
            control_frame,
            text="🌐 Web Search",
            variable=self.web_search_var,
            font=('Arial', 9),
            fg='#002555',
            bg='#f3ece6',
            selectcolor='#95a5a6'
        )
        self.web_search_check.pack(side='left', padx=(10, 5))
        
        # Enhanced TV/Meme Search Control
        self.tv_meme_var = tk.BooleanVar(value=False)
        self.tv_meme_check = tk.Checkbutton(
            control_frame,
            text="📺 TV/Meme Search",
            variable=self.tv_meme_var,
            font=('Arial', 9),
            fg='#002555',
            bg='#f3ece6',
            selectcolor='#95a5a6'
        )
        self.tv_meme_check.pack(side='left', padx=5)
        
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
        
        # Statistics button for comedy feedback
        self.stats_button = tk.Button(
            control_frame,
            text="📊 Show Stats",
            command=self.show_statistics,
            font=('Arial', 12),
            bg='#9b59b6',
            fg='white',
            padx=20,
            pady=5
        )
        self.stats_button.pack(side='left', padx=5)
        
        # Status indicator
        self.status_label = tk.Label(
            control_frame,
            text="Ready to start",
            font=('Arial', 10),
            fg='#002555',
            bg='#f3ece6'
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
            
            # MODALITÀ COMPLETA: RAG e Web Search riabilitati
            use_web_search = True  # Riabilitato per contenuti freschi
            club = ComedyClub(use_web_search=True, use_rag=True, use_rating=True)
            
            # Check what systems are available
            systems_active = []
            if hasattr(club, 'enhanced_rag') and club.enhanced_rag:
                systems_active.append("RAG")
            if hasattr(club, 'comedy_tools') and club.comedy_tools:
                systems_active.append("Comedy Tools")
            if hasattr(club, 'feedback_system') and club.feedback_system:
                systems_active.append("Feedback System")
            if use_web_search:
                systems_active.append("Web Search")
            
            systems_str = " + ".join(systems_active) if systems_active else "Basic"
            rag_status = f"🧠 {systems_str}"
            self.update_current_performance("Show Manager", f"✅ {rag_status} ready!")
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
                if comedian_name == "Dave":
                    gui_name = "Dave_Observational"
                elif comedian_name == "Mike":
                    gui_name = "Mike_Dark"
                elif comedian_name == "Sarah":
                    gui_name = "Sarah_Wordplay"
                elif comedian_name == "Lisa":
                    gui_name = "Lisa_Absurd"
                else:
                    # Fallback for unknown comedian
                    gui_name = comedian_name
                
                # Update status
                self.update_comedian_status(gui_name, "🎤 Performing")
                
                # Show that we're generating
                self.update_current_performance(comedian_name, "🤔 Thinking of a joke...")
                
                # Get performance with user's topic and enhanced search option
                try:
                    enhanced_tv_search = self.tv_meme_var.get()
                    
                    # Use get_joke_for_gui if available for rating integration
                    if hasattr(club, 'get_joke_for_gui'):
                        joke_data = club.get_joke_for_gui(comedian_name, user_topic, enhanced_tv_search=enhanced_tv_search)
                        joke = joke_data['joke']
                        
                        # Update joke data for rating
                        self.update_joke_for_rating({
                            'joke': joke,
                            'comedian': comedian_name,
                            'topic': user_topic,
                            'timestamp': joke_data.get('timestamp', time.time())
                        })
                    else:
                        joke = club.get_joke(comedian_name, user_topic, enhanced_tv_search=enhanced_tv_search)
                    
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
                    
                    # Tempo ridotto per tutte le battute - 5 secondi
                    self.smart_sleep(5)  # 5 seconds for all jokes
                    
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
                            
                            # Update joke data for rating the response too!
                            self.update_joke_for_rating({
                                'joke': response,
                                'comedian': performer['comedian'],
                                'topic': user_topic,
                                'timestamp': time.time(),
                                'type': 'response',  # Mark as response for better tracking
                                'responding_to': target_joke['comedian']
                            })
                            
                            # Audience loves debates!
                            debate_reactions = ["🔥 Burn!", "😂 Great comeback!", "👏 Brilliant response!", "🎭 Comedy gold!"]
                            reaction = random.choice(debate_reactions)
                            self.update_audience_reaction(reaction)
                            
                            # Tempo ridotto per tutte le risposte - 5 secondi
                            self.smart_sleep(5)  # 5 seconds for all responses
                            
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

    def show_statistics(self):
        """Show comedy performance statistics in a popup window"""
        try:
            import sys
            import os
            sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
            
            from src.utils.comedy_feedback import ComedyFeedbackSystem
            
            # Create statistics window
            stats_window = tk.Toplevel(self.root)
            stats_window.title("📊 Comedy Performance Statistics")
            stats_window.geometry("600x500")
            stats_window.configure(bg='#f3ece6')
            
            # Title
            title_label = tk.Label(
                stats_window,
                text="📊 COMEDY PERFORMANCE STATISTICS",
                font=('Arial', 16, 'bold'),
                fg='#002555',
                bg='#f3ece6'
            )
            title_label.pack(pady=10)
            
            # Create text area with scrollbar
            text_frame = tk.Frame(stats_window, bg='#f3ece6')
            text_frame.pack(fill='both', expand=True, padx=10, pady=10)
            
            stats_text = tk.Text(
                text_frame,
                font=('Consolas', 10),
                bg='#002555',
                fg='white',
                wrap='word',
                state='normal'
            )
            
            scrollbar = tk.Scrollbar(text_frame, orient='vertical', command=stats_text.yview)
            stats_text.configure(yscrollcommand=scrollbar.set)
            
            stats_text.pack(side='left', fill='both', expand=True)
            scrollbar.pack(side='right', fill='y')
            
            # Load and display statistics
            feedback_system = ComedyFeedbackSystem()
            
            # DEBUG: Mostra tutti i comedian presenti nel feedback
            all_comedians = set()
            for feedback in feedback_system.feedback_history:
                all_comedians.add(feedback.get('comedian', 'Unknown'))
            
            stats_text.insert('end', f"📋 DEBUG: Comedians found in feedback: {', '.join(sorted(all_comedians))}\n")
            stats_text.insert('end', f"📊 Total feedback entries: {len(feedback_system.feedback_history)}\n\n")
            
            # General leaderboard
            stats_text.insert('end', "🏆 COMEDY LEADERBOARD\n")
            stats_text.insert('end', "=" * 50 + "\n\n")
            
            top_performers = feedback_system.get_top_performers(4)
            if top_performers:
                for i, performer in enumerate(top_performers, 1):
                    medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "🏅"
                    stats_text.insert('end', f"{medal} {i}° {performer['comedian']}: "
                                             f"{performer['average_score']:.2f}/1.0 "
                                             f"({performer['performances']} performances)\n")
            else:
                stats_text.insert('end', "No performance data available yet.\n")
            
            stats_text.insert('end', "\n" + "=" * 50 + "\n\n")
            
            # Individual comedian stats
            comedians = ["Dave", "Sarah", "Mike", "Lisa"]
            for comedian in comedians:
                stats = feedback_system.get_comedian_stats(comedian)
                
                stats_text.insert('end', f"🎭 {comedian.upper()}\n")
                stats_text.insert('end', "-" * 30 + "\n")
                
                if "message" in stats:
                    stats_text.insert('end', f"   {stats['message']}\n")
                else:
                    stats_text.insert('end', f"   Total Performances: {stats['total_performances']}\n")
                    stats_text.insert('end', f"   Quality Average: {stats['average_quality']:.2f}/1.0\n")
                    stats_text.insert('end', f"   Audience Score: {stats['average_audience_score']:.2f}/1.0\n")
                    stats_text.insert('end', f"   Best Topic: {stats['best_topic']}\n")
                    stats_text.insert('end', f"   Trend: {stats['improvement_trend']}\n")
                    if stats['best_joke']:
                        best_joke = stats['best_joke'][:80] + "..." if len(stats['best_joke']) > 80 else stats['best_joke']
                        stats_text.insert('end', f"   Best Joke: {best_joke}\n")
                
                stats_text.insert('end', "\n")
            
            # System info
            stats_text.insert('end', "🔧 SYSTEM INFO\n")
            stats_text.insert('end', "-" * 30 + "\n")
            stats_text.insert('end', "   RAG System: ✅ Active with Jester Dataset\n")
            stats_text.insert('end', "   Comedy Tools: ✅ Advanced Reasoning\n")
            stats_text.insert('end', "   Feedback System: ✅ Iterative Learning\n")
            stats_text.insert('end', f"   Web Search: {'✅ Enabled' if self.web_search_var.get() else '❌ Disabled'}\n")
            
            stats_text.config(state='disabled')
            
            # Close button
            close_button = tk.Button(
                stats_window,
                text="Close",
                command=stats_window.destroy,
                font=('Arial', 12),
                bg='#e74c3c',
                fg='white',
                padx=20,
                pady=5
            )
            close_button.pack(pady=10)
            
        except Exception as e:
            self.add_log(f"❌ Error loading statistics: {e}", "Show_Manager")
    
    def rate_current_joke(self, rating: str):
        """Rate the current joke or response"""
        if not self.current_joke_data or not self.rating_system:
            return
            
        comment = self.comment_entry.get().strip() if hasattr(self, 'comment_entry') else ""
        
        # Enhanced context for responses
        context = {}
        if self.current_joke_data.get('type') == 'response':
            context['is_response'] = True
            context['responding_to'] = self.current_joke_data.get('responding_to', 'unknown')
            context['interaction_type'] = 'comedy_battle'
        
        success = self.rating_system.add_rating(
            self.current_joke_data['joke'],
            self.current_joke_data['comedian'],
            self.current_joke_data.get('topic', 'general'),
            rating,
            comment if comment else None,
            context=context
        )
        
        # AGGIUNTO: Salva anche nel sistema di feedback per le statistiche
        try:
            import sys
            import os
            sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
            from src.utils.comedy_feedback import ComedyFeedbackSystem
            
            feedback_system = ComedyFeedbackSystem()
            
            # Converti rating umano a score numerico
            rating_scores = {
                'love': 1.0,
                'like': 0.8,
                'meh': 0.5,
                'dislike': 0.2,
                'hate': 0.0
            }
            
            # Crea un feedback artificiale per le statistiche
            from dataclasses import asdict
            from src.utils.comedy_feedback import JokeFeedback
            import time
            
            fake_feedback = JokeFeedback(
                joke=self.current_joke_data['joke'],
                comedian=self.current_joke_data['comedian'],
                topic=self.current_joke_data.get('topic', 'general'),
                quality_score=rating_scores.get(rating, 0.5),
                audience_score=rating_scores.get(rating, 0.5),
                feedback_notes=[f"Human rating: {rating}"],
                timestamp=time.time()
            )
            
            feedback_system.feedback_history.append(asdict(fake_feedback))
            feedback_system._save_feedback_history()
            print(f"📊 Rating salvato per {self.current_joke_data['comedian']}: {rating}")
            
        except Exception as e:
            print(f"⚠️ Errore salvataggio feedback: {e}")
        
        if success:
            # Update rating status with more detailed feedback
            rating_text = {
                'love': '😍 LOVED IT!',
                'like': '👍 Liked it!',
                'meh': '😐 Meh...',
                'dislike': '👎 Didn\'t like it',
                'hate': '🤮 HATED IT!'
            }
            
            if hasattr(self, 'rating_status'):
                joke_type = "Response" if self.current_joke_data.get('type') == 'response' else "Joke"
                comedian = self.current_joke_data['comedian']
                self.rating_status.config(text=f"✅ {joke_type} by {comedian}: {rating_text.get(rating, rating)}")
            
            # Clear comment
            if hasattr(self, 'comment_entry'):
                self.comment_entry.delete(0, tk.END)
            
            # Disable rating buttons until next joke
            self.disable_rating_buttons()
            
            # Add rating to log with enhanced info
            joke_type = "response" if self.current_joke_data.get('type') == 'response' else "joke"
            self.add_log(f"⭐ Rated {comedian}'s {joke_type}: {rating_text.get(rating, rating)}", "Rating System")
            
        else:
            messagebox.showerror("Error", "Failed to save rating!")
    
    def enable_rating_buttons(self):
        """Enable rating buttons for a new joke or response"""
        if hasattr(self, 'rating_buttons'):
            for button in self.rating_buttons.values():
                button.config(state='normal')
            
            if hasattr(self, 'rating_status'):
                if self.current_joke_data and self.current_joke_data.get('type') == 'response':
                    comedian = self.current_joke_data['comedian']
                    responding_to = self.current_joke_data.get('responding_to', 'someone')
                    self.rating_status.config(text=f"⭐ Rate {comedian}'s response to {responding_to}!")
                else:
                    self.rating_status.config(text="⭐ Please rate this joke!")
    
    def disable_rating_buttons(self):
        """Disable rating buttons after rating"""
        if hasattr(self, 'rating_buttons'):
            for button in self.rating_buttons.values():
                button.config(state='disabled')
    
    def update_joke_for_rating(self, joke_data: dict):
        """Update current joke data for rating"""
        self.current_joke_data = joke_data
        self.enable_rating_buttons()

def main():
    """Main function to run the GUI"""
    root = tk.Tk()
    app = ComedyClubGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
