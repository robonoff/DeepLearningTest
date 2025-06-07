#!/usr/bin/env python3
"""
Configuration Management for Comedy Club Simulator
"""

import os
from typing import Dict, List, Any

class Config:
    """Central configuration class"""
    
    # Ollama Settings
    OLLAMA_BASE_URL = "http://localhost:11434"
    OLLAMA_MODEL = "llama3.2:1b"  # Faster 1b model for development
    OLLAMA_TIMEOUT = 45
    OLLAMA_MAX_TOKENS = 150
    OLLAMA_TEMPERATURE = 0.7
    
    # File Paths
    LOGS_DIR = "logs"
    CONFIG_DIR = "config" 
    DATASETS_DIR = "datasets"
    
    # Comedy Club Settings
    DEFAULT_ROUNDS = 2
    DEFAULT_TOPICS = [
        "technology and smartphones",
        "everyday life annoyances", 
        "social media behavior",
        "food and restaurants",
        "transportation and travel",
        "work and office life"
    ]
    
    # GUI Settings
    WINDOW_WIDTH = 1200
    WINDOW_HEIGHT = 800
    DARK_THEME = True
    
    @classmethod
    def get_ollama_config(cls) -> List[Dict[str, Any]]:
        """Get Ollama configuration for AutoGen"""
        return [
            {
                "model": cls.OLLAMA_MODEL,
                "api_key": "ollama",
                "base_url": f"{cls.OLLAMA_BASE_URL}/v1",
                "timeout": cls.OLLAMA_TIMEOUT,
                "max_tokens": cls.OLLAMA_MAX_TOKENS,
                "temperature": cls.OLLAMA_TEMPERATURE
            }
        ]
    
    @classmethod
    def get_file_path(cls, file_type: str, filename: str) -> str:
        """Get full path for different file types"""
        base_dirs = {
            "logs": cls.LOGS_DIR,
            "config": cls.CONFIG_DIR,
            "datasets": cls.DATASETS_DIR
        }
        base_dir = base_dirs.get(file_type, ".")
        return os.path.join(base_dir, filename)
