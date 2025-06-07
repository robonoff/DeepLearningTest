#!/bin/bash

# Apple M1 optimized Ollama startup script
export OLLAMA_NUM_PARALLEL=4          # Allow 4 parallel requests
export OLLAMA_MAX_LOADED_MODELS=2     # Keep 2 models in memory
export OLLAMA_FLASH_ATTENTION=1       # Enable flash attention for faster inference
export OLLAMA_KV_CACHE_TYPE=q8_0      # Use quantized cache for memory efficiency
export OLLAMA_GPU_OVERHEAD=0.1        # Reserve 10% GPU memory for system
export OLLAMA_METAL=1                 # Enable Metal GPU acceleration (Apple Silicon)

echo "Starting Ollama with Apple M1 optimizations..."
echo "Flash Attention: Enabled"
echo "Metal GPU Acceleration: Enabled"
echo "Parallel Requests: 4"
echo "Max Loaded Models: 2"

# Start Ollama service
brew services restart ollama

echo "Ollama started with M1 optimizations!"
echo "You can now run your AutoGen scripts with improved performance."
