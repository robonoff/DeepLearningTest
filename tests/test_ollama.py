#!/usr/bin/env python3
"""
Ultra-simple Ollama test
"""

import subprocess
import sys

def test_ollama():
    """Test direct Ollama call"""
    print("🧪 Testing Ollama CLI...")
    
    try:
        # Simple test - use faster 1b model
        cmd = ['ollama', 'run', 'llama3.2:1b']
        prompt = "Tell me a one-line joke about computers\n"
        
        print(f"📤 Sending: {prompt.strip()}")
        
        process = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        stdout, stderr = process.communicate(input=prompt, timeout=45)
        
        if process.returncode == 0:
            print(f"✅ Response: {stdout.strip()}")
            return True
        else:
            print(f"❌ Error: {stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("⚠️ Timeout!")
        return False
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

if __name__ == "__main__":
    success = test_ollama()
    sys.exit(0 if success else 1)
