#!/usr/bin/env python3
"""
Custom Ollama client for comedy club simulation
Uses Ollama CLI directly instead of API endpoint
"""

import subprocess
import json
import os
from typing import Dict, List, Optional

class OllamaClient:
    """Custom client using Ollama CLI"""
    
    def __init__(self, model: str = "llama3.2:1b"):
        self.model = model
        
    def generate(self, model: str, prompt: str, **kwargs) -> str:
        """Generate response using Ollama CLI"""
        
        try:
            # Use the specified model or fallback to default
            model_to_use = model if model else self.model
            
            # Simple approach - directly pipe the prompt
            result = subprocess.run([
                'ollama', 'run', model_to_use
            ], 
            input=prompt,
            capture_output=True, 
            text=True, 
            timeout=kwargs.get("timeout", 15)
            )
            
            if result.returncode == 0:
                response = result.stdout.strip()
                return response if response else "🤔 *thinking* (no response generated)"
            else:
                return f"⚠️ Ollama error: {result.stderr.strip()}"
            
        except subprocess.TimeoutExpired:
            return "⚠️ Ollama timeout - try again"
        except FileNotFoundError:
            return "❌ Ollama not found - install Ollama first"
        except Exception as e:
            return f"❌ Error: {e}"
    
    def chat(self, model: str, messages: List[Dict], **kwargs) -> str:
        """Convert chat format to prompt and generate response"""
        
        # Convert messages to a single prompt
        prompt_parts = []
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            
            if role == "system":
                prompt_parts.append(f"System: {content}")
            elif role == "user":
                prompt_parts.append(f"Human: {content}")
            elif role == "assistant":
                prompt_parts.append(f"Assistant: {content}")
        
        prompt = "\n".join(prompt_parts) + "\nAssistant:"
        
        return self.generate(model, prompt, **kwargs)

# Test the client
def test_ollama_client():
    """Test the custom Ollama client"""
    client = OllamaClient()
    
    print("🧪 Testing Ollama CLI client...")
    print("🔍 Using model: llama3.2:1b")
    
    response = client.generate(
        model="llama3.2:1b",
        prompt="Tell me a very short joke about computers",
        timeout=10
    )
    
    print(f"✅ Response: {response}")
    return response

if __name__ == "__main__":
    test_ollama_client()
