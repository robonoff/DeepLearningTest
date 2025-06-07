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
        
        # Main content area with two columns
        main_frame = tk.Frame(self.root, bg='#1a1a1a')
        main_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Left column - Comedy Club Stage
        self.setup_stage_area(main_frame)
        
        # Right column - Performance Log
        self.setup_log_area(main_frame)
        
        # Bottom controls
        self.setup_controls()
    
    def setup_stage_area(self, parent):
        """Setup the visual stage area"""
        stage_frame = tk.Frame(parent, bg='#2c3e50', relief='raised', bd=2)
        stage_frame.pack(side='left', fill='both', expand=True, padx=(0, 5))
        
        # Stage title
        stage_title = tk.Label(
            stage_frame,
            text="🎤 COMEDY CLUB STAGE",
            font=('Arial', 14, 'bold'),
            fg='white',
            bg='#2c3e50'
        )
        stage_title.pack(pady=5)
        
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
            height=8,
            width=50,
            font=('Arial', 10),
            bg='#2c3e50',
            fg='white',
            insertbackground='white',
            state='disabled'
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
        self.load_button.pack(side='left', padx=5)
        
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
        self.start_button.config(state='disabled')
        self.stop_button.config(state='normal')
        self.status_label.config(text="Show in progress...", fg='#f39c12')
        
        # Clear previous content
        self.clear_displays()
        
        # Start simulation in separate thread
        self.simulation_thread = threading.Thread(target=self.run_simulation, daemon=True)
        self.simulation_thread.start()
    
    def stop_show(self):
        """Stop the current show"""
        self.is_running = False
        self.start_button.config(state='normal')
        self.stop_button.config(state='disabled')
        self.status_label.config(text="Show stopped", fg='#e74c3c')
        
        # Reset comedian status
        for name, widget in self.comedian_widgets.items():
            widget['activity'].config(text="💤 Waiting")
    
    def clear_displays(self):
        """Clear all display areas"""
        self.log_text.config(state='normal')
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state='disabled')
        
        self.current_performance.config(state='normal')
        self.current_performance.delete(1.0, tk.END)
        self.current_performance.config(state='disabled')
        
        self.audience_reaction.config(text="🤐 Silence...")
    
    def run_simulation(self):
        """Run the actual comedy simulation"""
        try:
            # Import and run the simulation
            import sys
            import os
            sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
            from src.core.comedy_club import ComedyClubSimulator
            
            self.add_log("🎭 Initializing comedy club...", "Show_Manager")
            club = ComedyClubSimulator(use_ollama=True)
            
            self.add_log("🎪 All comedians ready!", "Show_Manager")
            self.show_info.config(text=f"Show started: {datetime.now().strftime('%H:%M:%S')}")
            
            # Run show with visual updates
            self.run_visual_show(club)
            
        except Exception as e:
            self.add_log(f"❌ Error: {e}", "Show_Manager")
        finally:
            if self.is_running:
                self.stop_show()
    
    def run_visual_show(self, club):
        """Run the show with visual updates"""
        # Get the comedians list and shuffle for performance order
        comedians = club.comedians.copy()
        random.shuffle(comedians)
        
        # Opening
        self.add_log("🎤 Welcome to the AI Comedy Club!", "Show_Manager")
        time.sleep(2)
        
        # Main show
        for round_num in range(2):  # 2 rounds
            if not self.is_running:
                break
                
            self.add_log(f"\\n🎭 === ROUND {round_num + 1} ===", "Show_Manager")
            
            for comedian in comedians:
                if not self.is_running:
                    break
                
                comedian_name = comedian.name
                
                # Update status
                self.update_comedian_status(comedian_name, "🎤 Performing")
                
                # Get topic based on comedian style
                topics = {
                    'observational': "everyday technology annoyances",
                    'dark': "silver linings in disasters", 
                    'wordplay': "animals with jobs",
                    'absurdist': "what if furniture had personalities"
                }
                topic = topics.get(comedian.humor_style, "general comedy")
                
                self.add_log(f"\\n🎯 {comedian_name} takes the stage!", comedian_name)
                self.add_log(f"Topic: {topic}", comedian_name)
                
                # Get performance
                try:
                    performance = club.get_comedian_performance(comedian, topic)
                    
                    # Display performance
                    self.update_current_performance(comedian_name, performance)
                    self.add_log(f"🗣️  {comedian_name}: {performance}", comedian_name)
                    
                    # Simulate audience reaction
                    reactions = {
                        'observational': ["😂 Big laughs!", "👏 Standing ovation!", "🤣 Audience loves it!"],
                        'dark': ["😬 Nervous laughter", "😨 Gasps then applause", "🖤 Dark humor appreciated"],
                        'wordplay': ["🙄 Groans and laughs", "📚 Dad joke energy!", "🎯 Pun perfection!"],
                        'absurdist': ["🤔 Confused laughter", "🌌 Mind = blown", "👽 What just happened?!"]
                    }
                    
                    reaction = random.choice(reactions.get(comedian.humor_style, ["👏 Polite applause"]))
                    self.update_audience_reaction(reaction)
                    self.add_log(f"👥 Audience: {reaction}", "Audience")
                    
                    time.sleep(3)  # Pause between performers
                    
                except Exception as e:
                    self.add_log(f"❌ {comedian_name} had technical difficulties: {e}", "Show_Manager")
                
                finally:
                    self.update_comedian_status(comedian_name, "💤 Waiting")
        
        # Closing
        if self.is_running:
            self.add_log("\\n🎉 That's our show! Thank you everyone!", "Show_Manager")
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
            self.current_performance.insert(tk.END, f"{comedian_name}:\\n{performance}")
            self.current_performance.config(state='disabled')
        
        self.root.after(0, update)
    
    def update_audience_reaction(self, reaction):
        """Update the audience reaction display"""
        self.root.after(0, lambda: self.audience_reaction.config(text=reaction))
    
    def add_log(self, message, speaker="System"):
        """Add a message to the log"""
        def update():
            self.log_text.config(state='normal')
            timestamp = datetime.now().strftime("%H:%M:%S")
            
            if speaker in self.comedian_colors:
                self.log_text.insert(tk.END, f"[{timestamp}] ", 'default')
                self.log_text.insert(tk.END, f"{speaker}: ", speaker)
                self.log_text.insert(tk.END, f"{message}\\n", 'default')
            else:
                self.log_text.insert(tk.END, f"[{timestamp}] {message}\\n")
            
            self.log_text.see(tk.END)
            self.log_text.config(state='disabled')
        
        self.root.after(0, update)
    
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
