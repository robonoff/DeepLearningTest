# 🎭 AI Comedy ## 🚀 Quick Start

### Prerequisites

1. **Configure Orfeo Access:**
   Create a `.env` file in the root directory with your Orfeo credentials:
   ```bash
   TOKEN=your_jwt_token_here
   ORFEO_MODEL=llama3.3:latest
   ORFEO_BASE_URL=your_orfeo_base_url
   ```

2. **Install Python Dependencies:**
   ```bash
   pip install -r requirements.txt
   ``` Edition

An interactive comedy club simulation where multiple AI agents with different comedy styles perform jokes and react to each other using Orfeo cluster with llama3.3:latest model.

## ✨ Key Features

- **Four Unique Comedy Agents**: Each with distinct personalities and comedy styles
- **Real-time Interaction**: Comedians react to each other's jokes dynamically
- **Enhanced RAG System**: Intelligent joke retrieval with web search capabilities
- **Advanced Web Search**: TV shows, memes, political content integration
- **Mock mode when Orfeo is unavailable
- **Beautiful Terminal UI**: Rich visual presentation with colors and formatting
- **Performance Analytics**: Track comedian effectiveness over time
- **Uses Orfeo cluster with llama3.3:latest model for superior performance

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

#### 🧪 Test Your Setup

Test your Orfeo connection and model availability:

```bash
python tests/test_enhanced_rag.py
```

This test verifies:
- Orfeo connectivity verification
- RAG system functionality
- Web search integration

## 📁 Project Structure

```
├── main.py                      # 🚀 Unified entry point for all modes
├── src/
│   ├── core/
│   │   ├── comedy_club_clean.py    # Main ComedyClub class with Orfeo integration
│   │   └── orfeo_client_new.py     # Orfeo client for llama3.3:latest
│   ├── agents/
│   │   └── comedians.py        # Comedian personalities and system prompts
│   ├── gui/
│   │   └── comedy_club_gui.py  # Tkinter-based visual interface
│   └── utils/
│       ├── enhanced_joke_rag.py    # RAG system with web search
│       ├── comedy_feedback.py      # Performance tracking system
│       └── comedy_tools.py         # Advanced comedy reasoning tools
├── examples/
│   ├── simple_comedy_club.py   # Simplified version for learning
│   └── mock_comedy_club.py     # Demo with pre-written jokes
├── tests/
│   └── test_enhanced_rag.py    # Orfeo connectivity and RAG tests
├── datasets/
│   └── shortjokes.csv          # 231k jokes dataset
├── config/
│   ├── orfeo_config_new.py     # Orfeo cluster configuration
│   └── set_env.sh              # Environment setup script
├── logs/                        # 📊 Generated performance logs (auto-created)
├── datasets/                    # 📝 Joke datasets and categorized content
├── papers/                      # 📚 Research papers and documentation
├── requirements.txt             # 📋 Python dependencies
└── README.md                    # 📖 This documentation
```

### Key Components

- **`main_clean_rag.py`**: Main entry point with RAG-enhanced comedy system
- **`src/core/`**: Heart of the simulation with Orfeo integration
- **`src/agents/`**: All comedian personalities with unique humor styles
- **`src/gui/`**: Full-featured GUI with real-time updates and rating system
- **`examples/`**: Standalone examples for learning and testing
- **`logs/`**: Auto-generated JSON logs of all performances and ratings

## 🎪 How It Works

### System Architecture
1. **Agent Initialization**: Four comedian agents are created with unique personalities, humor styles, and system prompts
2. **Performance Engine**: The ComedyClub orchestrates multi-round comedy shows with RAG enhancement
3. **LLM Integration**: Direct API calls to Orfeo cluster with llama3.3:latest for superior comedy generation
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
- **Orfeo Integration**: Direct API calls to Orfeo cluster with llama3.3:latest for superior performance
- **Timeout Management**: 120-second timeouts with robust error handling  
- **RAG Enhancement**: Vector-based joke retrieval with real-time web search
- **Cross-Platform**: Works on macOS, Linux, and Windows with proper Orfeo access

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

### Orfeo Connection Issues

**"TOKEN not found" Error:**
```bash
# Check your .env file
cat .env

# Ensure all required variables are set
TOKEN=your_jwt_token
ORFEO_MODEL=llama3.3:latest
ORFEO_BASE_URL=your_orfeo_url

# Source the environment setup
source config/set_env.sh
```

**Connection Timeout:**
```bash
# Test Orfeo connectivity
python -c "
from src.core.orfeo_client_new import OrfeoClient
client = OrfeoClient()
print('✅ Orfeo connection successful')
"

# Check SSH tunnel if needed
ssh -L 8080:10.128.2.165:8080 orfeo
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
- Maintain stable Orfeo connection
- Use SSH tunneling if required: `ssh -L 8080:10.128.2.165:8080 orfeo`
- Close other resource-intensive applications

**Memory Usage:**
- RAG system uses vector embeddings in memory
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

