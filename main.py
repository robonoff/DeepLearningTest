#!/usr/bin/env python3
"""
AI Comedy Club Simulator - Main Entry Point
Enhanced version inspired by Agent Hospital paper but for comedy
"""

import sys
import os
import argparse
import subprocess
from pathlib import Path

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import pandas
        import tkinter
        print("✅ All dependencies available")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("💡 Install with: pip install -r requirements.txt")
        return False

def check_ollama():
    """Check if Ollama is available and has models"""
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True, timeout=10)
        if result.returncode != 0:
            print("⚠️ Ollama not available - will run in mock mode")
            return False
        
        # Check for available models
        models = result.stdout
        if 'llama3.2' in models:
            print("✅ Ollama and Llama 3.2 models available")
            return True
        else:
            print("⚠️ No Llama 3.2 models found - will run in mock mode")
            print("💡 Install with: ollama pull llama3.2:1b")
            return False
            
    except Exception as e:
        print(f"⚠️ Ollama check failed: {e} - will run in mock mode")
        return False

def prepare_data():
    """Prepare joke categorization data if needed"""
    try:
        from src.utils.joke_categorizer import JokeCategorizer
        
        # Check if we have categorized jokes
        if not os.path.exists("logs/categorized_jokes.json"):
            print("📚 Preparing joke database...")
            if os.path.exists("datasets/shortjokes.csv"):
                categorizer = JokeCategorizer("datasets/shortjokes.csv")
                jokes = categorizer.categorize_jokes()
                
                # Ensure logs directory exists
                os.makedirs("logs", exist_ok=True)
                
                import json
                with open("logs/categorized_jokes.json", 'w', encoding='utf-8') as f:
                    json.dump({"jokes": jokes}, f, indent=2, ensure_ascii=False)
                print("✅ Joke database prepared")
            else:
                print("⚠️ No joke dataset found - will use built-in examples")
        else:
            print("✅ Joke database ready")
        return True
        
    except Exception as e:
        print(f"⚠️ Data preparation issue: {e}")
        return True  # Continue anyway

def run_text_simulation():
    """Run the text-based comedy simulation"""
    try:
        from src.core import ComedyClubSimulator
        
        print("🎭 Starting text-based comedy simulation...")
        club = ComedyClubSimulator(use_ollama=check_ollama())
        club.run_comedy_show()
        return True
        
    except Exception as e:
        print(f"❌ Text simulation failed: {e}")
        return False

def run_gui_simulation():
    """Run the GUI-based comedy simulation"""
    try:
        import tkinter as tk
        sys.path.insert(0, 'src/gui')
        from comedy_club_gui import ComedyClubGUI
        
        print("🎨 Starting GUI comedy simulation...")
        root = tk.Tk()
        app = ComedyClubGUI(root)
        root.mainloop()
        return True
        
    except Exception as e:
        print(f"❌ GUI simulation failed: {e}")
        return False

def run_test():
    """Run Ollama connectivity test"""
    try:
        sys.path.insert(0, 'tests')
        import subprocess
        print("🧪 Running Ollama connectivity test...")
        result = subprocess.run([sys.executable, 'tests/test_ollama.py'], 
                              capture_output=False, text=True)
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='AI Comedy Club Simulator - Multi-agent comedy performance system',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                    # Run GUI simulation (default)
  python main.py --mode text        # Run text-only simulation
  python main.py --mode test        # Test Ollama connectivity
  python main.py --skip-checks     # Skip dependency checks
        """
    )
    
    parser.add_argument('--mode', choices=['text', 'gui', 'test'], default='gui',
                       help='Simulation mode (default: gui)')
    parser.add_argument('--skip-checks', action='store_true',
                       help='Skip dependency and system checks')
    
    args = parser.parse_args()
    
    # Print header
    print("🎭" + "=" * 60)
    print("🎤 AI COMEDY CLUB SIMULATOR")
    print("🎭" + "=" * 60)
    print("Inspired by 'Agent Hospital' paper")
    print("Four AI comedians with distinct humor styles")
    print("Powered by local Llama 3.2 via Ollama")
    print("=" * 62)
    
    # Run checks unless skipped
    if not args.skip_checks:
        print("\n🔍 Checking system requirements...")
        
        if not check_dependencies():
            return 1
        
        print("\n📚 Preparing data...")
        if not prepare_data():
            return 1
    
    # Run the selected mode
    try:
        print(f"\n🚀 Starting {args.mode} mode...")
        
        if args.mode == 'text':
            success = run_text_simulation()
        elif args.mode == 'gui':
            success = run_gui_simulation()
        elif args.mode == 'test':
            success = run_test()
        
        if success:
            print(f"\n🎉 {args.mode.title()} simulation completed successfully!")
        else:
            print(f"\n❌ {args.mode.title()} simulation failed")
            return 1
            
    except KeyboardInterrupt:
        print("\n⏹️ Simulation interrupted by user")
        return 0
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
