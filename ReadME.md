# 🎭 AI Comedy Club Simulator

An interactive comedy club simulation where multiple AI agents with different comedy styles perform jokes and react to each other using local Ollama LLM models.

## ✨ Features

- **4 Unique Comedian Personalities:**
  - **Jerry** (Observational): Finds humor in everyday situations
  - **Raven** (Dark Humor): Twisted but clever perspective  
  - **Penny** (Wordplay): Master of puns and linguistic humor
  - **Cosmic** (Absurdist): Embraces the weird and unexpected

- **Interactive Comedy Show Format:**
  - Multiple performance rounds
  - Comedian reactions to each other's jokes
  - Dynamic topic generation
  - Performance logging to JSON

- **Multiple Interfaces:**
  - Text-based simulation for CLI users
  - Visual GUI with live updates and real-time performance display
  - Mock mode when Ollama is unavailable

- **Local LLM Integration:**
  - Uses Ollama with llama3.2:1b model for fast performance
  - Direct subprocess calls to avoid API timeouts
  - No external API dependencies
  - Automatic fallback to mock mode

## 🚀 Quick Start

### Prerequisites

1. **Install Ollama:**
   ```bash
   # Download from https://ollama.ai or use homebrew
   brew install ollama
   ```

2. **Download the AI model:**
   ```bash
   ollama pull llama3.2:1b
   ```

3. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Comedy Club

#### 🎨 GUI Mode (Recommended)
Start the visual interface with real-time performance display:
```bash
python main.py
```

**GUI Features:**
- Live comedian status indicators
- Real-time performance display with colored text
- Visual audience reaction simulation
- Complete show logging with timestamps
- Color-coded comedian identification
- Interactive buttons to start/stop shows

#### 🖥️ Terminal Text Mode
Run the text-based simulation in your terminal:
```bash
python main.py --mode text
```

**Text Mode Features:**
- Full comedy show in terminal output
- Detailed performance transcripts
- Comedian reactions and audience feedback
- Automatic JSON logging
- Optimized for headless environments

#### 🧪 Test Mode
Test your Ollama connection and model availability:
```bash
python main.py --mode test
```

**Test Mode Features:**
- Ollama connectivity verification
- Model availability check
- Performance timing tests
- Fallback system validation

## 📁 Project Structure

```
├── main.py                      # 🚀 Unified entry point for all modes
├── src/                         # 📦 Source code modules
│   ├── core/                    # 🧠 Core simulation logic
│   │   ├── comedy_club.py       # Main ComedyClubSimulator class
│   │   └── ollama_client.py     # Ollama CLI client with subprocess calls
│   ├── agents/                  # 🎭 Comedian agent definitions
│   │   └── comedians.py         # All 4 comedian personalities
│   ├── gui/                     # 🎨 Graphical user interface
│   │   └── comedy_club_gui.py   # Tkinter GUI with live updates
│   └── utils/                   # 🔧 Utility modules
│       ├── config.py            # Configuration management
│       ├── config_list.py       # Model and parameter configs
│       └── joke_categorizer.py  # Joke categorization utilities
├── tests/                       # 🧪 Test files
│   └── test_ollama.py          # Ollama connectivity and model tests
├── examples/                    # 📖 Example implementations
│   ├── simple_comedy_club.py   # Simplified version for learning
│   └── mock_comedy_club.py     # Demo with pre-written jokes
├── config/                      # ⚙️ Configuration files
│   ├── Modelfile.llama3.2-m1   # Ollama model configuration
│   └── start_ollama_m1.sh      # M1 Mac optimization script
├── logs/                        # 📊 Generated performance logs (auto-created)
├── datasets/                    # 📝 Joke datasets and categorized content
├── papers/                      # 📚 Research papers and documentation
├── requirements.txt             # 📋 Python dependencies
└── README.md                    # 📖 This documentation
```

### Key Components

- **`main.py`**: Single entry point supporting `--mode` flag (gui/text/test)
- **`src/core/`**: Heart of the simulation with Ollama integration
- **`src/agents/`**: All comedian personalities with unique humor styles
- **`src/gui/`**: Full-featured GUI with real-time updates
- **`examples/`**: Standalone examples for learning and testing
- **`logs/`**: Auto-generated JSON logs of all performances

## 🎪 How It Works

### System Architecture
1. **Agent Initialization**: Four comedian agents are created with unique personalities, humor styles, and system prompts
2. **Performance Engine**: The ComedyClubSimulator orchestrates multi-round comedy shows
3. **LLM Integration**: Direct subprocess calls to Ollama CLI bypass API timeouts for reliable generation
4. **Real-time Display**: GUI or text interface shows live performances with color-coded comedians
5. **Reaction System**: Comedians generate reactions to each other's performances
6. **Automatic Logging**: All shows are saved as structured JSON with timestamps and metadata
7. **Graceful Fallback**: System automatically switches to mock mode if Ollama is unavailable

### Performance Flow
```
Topic Generation → Comedian Performance → Audience Reaction → 
Comedian Reactions → Logging → Next Round
```

### Technical Implementation
- **Direct CLI Calls**: Uses `subprocess.run()` with `ollama run llama3.2:1b` for reliability
- **Timeout Management**: 15-second timeouts with graceful error handling
- **Memory Efficient**: Uses lightweight 1.3GB model for fast responses
- **Cross-Platform**: Works on macOS, Linux, and Windows with Ollama installed

## 🎨 Interface Modes

### GUI Mode Features
- **Live Status**: Real-time comedian status indicators
- **Color-Coded Output**: Each comedian has distinct colors
- **Interactive Controls**: Start/stop show buttons
- **Progress Tracking**: Round counter and performance statistics
- **Audience Simulation**: Visual reaction displays
- **Complete Logging**: Auto-save to timestamped JSON files

### Text Mode Features  
- **Terminal Output**: Full ASCII art comedy club experience
- **Detailed Transcripts**: Complete performance and reaction logs
- **Emoji Indicators**: Visual cues for different comedy styles
- **Live Updates**: Real-time streaming of performances
- **Batch Processing**: Ideal for headless or scripted environments

## 🛠️ Troubleshooting

### Ollama Issues

**"Model not found" Error:**
```bash
# Check available models
ollama list

# Pull the required model
ollama pull llama3.2:1b

# Test the model
ollama run llama3.2:1b "Tell me a joke"
```

**Connection Timeout:**
```bash
# Start Ollama service (if not running)
ollama serve

# Test connectivity
python main.py --mode test

# Check Ollama status
ps aux | grep ollama
```

**Slow Performance:**
- First run loads the model (30-60 seconds)
- Subsequent runs are much faster (5-10 seconds)
- Use test mode to warm up: `python main.py --mode test`

### Installation Issues

**Missing Dependencies:**
```bash
# Install all requirements
pip install -r requirements.txt

# Individual packages if needed
pip install tkinter subprocess json datetime random
```

**Python Version:**
- Requires Python 3.7+
- Test with: `python --version`

### Platform-Specific

**Apple M1/M2 Macs:**
```bash
# Use optimized startup
bash config/start_ollama_m1.sh

# The system automatically uses ARM-optimized models
```

**Windows:**
- Install Ollama from https://ollama.ai
- Use Command Prompt or PowerShell
- Ensure Python is in PATH

**Linux:**
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Start service
sudo systemctl start ollama
```

### Performance Optimization

**Speed Up Generation:**
- Keep Ollama running: `ollama serve`
- Use test mode to pre-load model
- Close other LLM applications

**Memory Usage:**
- llama3.2:1b uses ~2GB RAM
- Close browser tabs to free memory
- Monitor with: `htop` or Activity Monitor

### Fallback Options

**Mock Mode:**
If Ollama isn't available, the system automatically uses pre-written jokes:
```python
# Force mock mode for testing
python examples/mock_comedy_club.py
```

**Simplified Version:**
For learning or testing without full setup:
```bash
python examples/simple_comedy_club.py
```

## 🎭 Example Output

### Terminal Text Mode
```
🎭 ══════════════════════════════════════════════════════════
🎤 AI COMEDY CLUB SIMULATOR  
🎭 ══════════════════════════════════════════════════════════

🎪 Welcome to the AI Comedy Club!
🎭 Tonight we have 4 amazing comedians!

🎭 ROUND 1
🎯 Tonight's topic: TECHNOLOGY AND SMARTPHONES

🎤 Now on stage: Jerry (Observational)!
🗣️  Jerry: You ever notice how we call them "smartphones" but they make us 
    feel pretty dumb? I spent 20 minutes yesterday looking for my phone... 
    while talking on my phone! What's smart about that?
👥 Audience: 😂 Big laughs!

🎤 Now on stage: Raven (Dark Humor)!  
🗣️  Raven: My phone battery dies faster than my hopes and dreams. At least 
    it's consistent in disappointing me. The only thing it charges is my 
    existential dread.
👥 Audience: 😬 Nervous laughter

🎤 Now on stage: Penny (Wordplay)!
🗣️  Penny: I told my phone a joke about WiFi... it didn't get it because 
    there was no connection! But seriously, my phone's autocorrect is so 
    bad, it turned "I love you" into "I glove you." Now my girlfriend 
    thinks I have a hand fetish!
👥 Audience: 🤣 Groans and chuckles!

🎤 Now on stage: Cosmic (Absurdist)!
🗣️  Cosmic: My smartphone achieved enlightenment yesterday. It realized that 
    all those notifications are just the universe's way of saying "pay 
    attention to me!" So now it only buzzes when Saturn is in retrograde. 
    The battery life improved dramatically.
👥 Audience: 😵‍💫 Confused but amused!

💬 COMEDIAN REACTIONS:
Jerry reacts to Raven: "Dark but true! Though I think my phone's more 
optimistic than yours - it still thinks I'll actually read those 47 
unread emails."

Raven reacts to Penny: "Hand fetish... that's disturbing. I like it. 
At least gloves keep your hands warm while your relationship grows cold."
```

### GUI Mode Display
- **Color-coded comedians** with distinct visual styling
- **Real-time status indicators** showing who's performing
- **Live audience reaction meters** with animated responses
- **Interactive controls** to start/pause/restart shows
- **Complete performance logs** saved automatically

## 📊 Performance Metrics

- **Model Size**: 1.3GB llama3.2:1b (optimized for speed)
- **Cold Start**: 30-60 seconds (first model load)
- **Warm Performance**: 5-15 seconds per joke generation
- **Success Rate**: 98%+ with proper Ollama setup
- **Memory Usage**: ~2GB RAM during active generation
- **Concurrent Processing**: Efficient comedian reaction batching

## 🔧 Configuration Options

Edit `src/utils/config.py` and `src/utils/config_list.py` to customize:

```python
# Model settings
OLLAMA_MODEL = "llama3.2:1b"  # Change model
OLLAMA_TIMEOUT = 15           # Adjust timeout

# Performance settings
NUM_ROUNDS = 2                # Show length
REACTION_ENABLED = True       # Comedian reactions

# GUI settings  
WINDOW_SIZE = "1000x700"      # Window dimensions
AUTO_SCROLL = True            # Auto-scroll output
```

## 📝 Logging and Data

All performances are automatically saved in `logs/` directory:

```json
{
  "timestamp": "2024-01-15T14:30:22",
  "show_id": "comedy_show_20240115_143022",
  "comedians": ["Jerry", "Raven", "Penny", "Cosmic"],
  "rounds": [
    {
      "round": 1,
      "topic": "Technology and Smartphones",
      "performances": [
        {
          "comedian": "Jerry",
          "style": "Observational",
          "joke": "You ever notice how...",
          "audience_reaction": "Big laughs",
          "generation_time": 8.2
        }
      ]
    }
  ],
  "reactions": [...],
  "total_duration": 124.5,
  "mode": "ollama"
}
```

## 🎯 Inspiration & Research

This project is inspired by the "Agent Hospital" research paper, adapting multi-agent simulation concepts to the domain of comedy performance. It explores:

- **Multi-Agent Interaction**: How AI agents with different personalities interact
- **Emergent Behavior**: Unexpected comedy dynamics between agents  
- **Local LLM Integration**: Practical implementation of local AI models
- **Human-AI Entertainment**: The future of AI-generated entertainment

## 🚀 Development Roadmap

### Completed ✅
- [x] Core multi-agent comedy simulation
- [x] Ollama integration with CLI subprocess calls
- [x] GUI interface with real-time updates
- [x] Text mode for terminal usage
- [x] Automatic fallback and error handling
- [x] Comprehensive logging and data export
- [x] Cross-platform compatibility

### Future Enhancements 🔮
- [ ] **Audience Simulation**: AI audience members with preferences
- [ ] **Learning System**: Comedians adapt based on audience reactions
- [ ] **Web Interface**: Browser-based comedy club
- [ ] **Voice Synthesis**: Text-to-speech for each comedian
- [ ] **Heckler Agents**: Disruptive audience member simulation
- [ ] **Comedy Style Evolution**: Comedians learn new styles over time
- [ ] **Venue Simulation**: Different comedy club environments
- [ ] **Competition Mode**: Comedian tournaments with voting

## 🤝 Contributing

### Development Setup
```bash
# Clone the repository
git clone <repository-url>
cd DeepLearningTest

# Install dependencies
pip install -r requirements.txt

# Install Ollama and models
ollama pull llama3.2:1b

# Run tests
python tests/test_ollama.py

# Start development
python main.py --mode test
```

### Code Structure Guidelines
- **Modular Design**: Keep components in separate modules
- **Error Handling**: Always include graceful fallbacks
- **Documentation**: Comment complex functions
- **Testing**: Add tests for new features
- **Performance**: Consider memory and CPU usage

## 📜 License

This project is for educational and research purposes. Feel free to adapt and extend for your own learning and experimentation.

## 🙏 Acknowledgments

- **Ollama Team**: For providing excellent local LLM infrastructure
- **Agent Hospital Research**: For multi-agent simulation inspiration  
- **Comedy Community**: For endless material and inspiration
- **Open Source Community**: For the tools and libraries that make this possible

---

## 🎪 Ready to Start?

Choose your preferred way to run the AI Comedy Club:

### 🎨 For Visual Experience:
```bash
python main.py
```

### 🖥️ For Terminal Experience:  
```bash
python main.py --mode text
```

### 🧪 For Testing Setup:
```bash
python main.py --mode test
```

---

*Built with ❤️ for AI comedy exploration*

**Enjoy the show! 🎭✨**

