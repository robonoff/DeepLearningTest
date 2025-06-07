# Configuration for Ollama with Llama 3.2 - Optimized for Apple M1
config_list = [
    {
        "model": "llama3.2:1b",  # Using the standard 1b model
        "api_key": "ollama",  # Ollama doesn't require a real API key
        "base_url": "http://localhost:11434/v1",  # Standard Ollama API endpoint
        "timeout": 60,  # Add timeout to prevent hanging
        "max_tokens": 150,  # Limit response length for faster generation
        "temperature": 0.7  # Add some creativity but keep it controlled
    }
]



