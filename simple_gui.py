#!/usr/bin/env python3
"""
Simplified Comedy Club GUI
Works with the new organized structure
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import json
import threading
import time
import sys
import os
from datetime import datetime
import random

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

class SimpleComedyGUI:
    """Simplified visual interface for the comedy club"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("🎭 AI Comedy Club")
        self.root.geometry("1000x700")
        self.root.configure(bg='#1a1a1a')
        
        self.is_running = False
        self.setup_gui()
    
    def setup_gui(self):
        """Setup the GUI"""
        # Title
        title = tk.Label(
            self.root,
            text="🎭 AI Comedy Club Simulator",
            font=('Arial', 20, 'bold'),
            fg='#FECA57',
            bg='#1a1a1a'
        )
        title.pack(pady=10)
        
        # Main area
        main_frame = tk.Frame(self.root, bg='#1a1a1a')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Performance display
        self.log_text = scrolledtext.ScrolledText(
            main_frame,
            height=25,
            width=80,
            font=('Consolas', 10),
            bg='#2c3e50',
            fg='white',
            insertbackground='white',
            state='disabled'
        )
        self.log_text.pack(fill='both', expand=True, pady=10)
        
        # Controls
        control_frame = tk.Frame(self.root, bg='#1a1a1a')
        control_frame.pack(fill='x', padx=10, pady=5)
        
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
        
        # Status
        self.status_label = tk.Label(
            control_frame,
            text="Ready to start",
            font=('Arial', 10),
            fg='#95a5a6',
            bg='#1a1a1a'
        )
        self.status_label.pack(side='right', padx=10)
    
    def add_log(self, message, speaker="System"):
        """Add message to log"""
        def update():
            self.log_text.config(state='normal')
            timestamp = datetime.now().strftime("%H:%M:%S")
            self.log_text.insert(tk.END, f"[{timestamp}] {speaker}: {message}\n")
            self.log_text.see(tk.END)
            self.log_text.config(state='disabled')
        
        self.root.after(0, update)
    
    def start_show(self):
        """Start the comedy show"""
        if self.is_running:
            return
        
        self.is_running = True
        self.start_button.config(state='disabled')
        self.stop_button.config(state='normal')
        self.status_label.config(text="Show in progress...", fg='#f39c12')
        
        # Clear log
        self.log_text.config(state='normal')
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state='disabled')
        
        # Start simulation
        self.simulation_thread = threading.Thread(target=self.run_simulation, daemon=True)
        self.simulation_thread.start()
    
    def stop_show(self):
        """Stop the show"""
        self.is_running = False
        self.start_button.config(state='normal')
        self.stop_button.config(state='disabled')
        self.status_label.config(text="Show stopped", fg='#e74c3c')
    
    def run_simulation(self):
        """Run the comedy simulation"""
        try:
            from src.core import ComedyClubSimulator
            
            self.add_log("🎭 Initializing comedy club...", "Show_Manager")
            club = ComedyClubSimulator(use_ollama=True)
            
            self.add_log("🎪 All comedians ready!", "Show_Manager")
            
            # Run a simplified show
            for round_num in range(2):
                if not self.is_running:
                    break
                
                self.add_log(f"\n🎭 === ROUND {round_num + 1} ===", "Show_Manager")
                
                # Shuffle comedians
                comedians = club.comedians.copy()
                random.shuffle(comedians)
                
                for comedian in comedians:
                    if not self.is_running:
                        break
                    
                    self.add_log(f"\n🎤 {comedian.name} takes the stage!", comedian.name)
                    
                    # Get performance
                    try:
                        performance = club.get_comedian_performance(comedian, "general comedy")
                        self.add_log(f"🗣️ {performance}", comedian.name)
                        
                        # Simulate audience reaction
                        reactions = ["😂 Big laughs!", "👏 Applause!", "🤣 Great stuff!"]
                        reaction = random.choice(reactions)
                        self.add_log(f"👥 Audience: {reaction}", "Audience")
                        
                        time.sleep(2)  # Pause
                        
                    except Exception as e:
                        self.add_log(f"❌ Technical difficulties: {e}", comedian.name)
            
            if self.is_running:
                self.add_log("\n🎉 That's our show! Thank you everyone!", "Show_Manager")
            
        except Exception as e:
            self.add_log(f"❌ Error: {e}", "Show_Manager")
        finally:
            if self.is_running:
                self.stop_show()

def main():
    """Main function"""
    root = tk.Tk()
    app = SimpleComedyGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
