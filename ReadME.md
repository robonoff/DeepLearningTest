# 🎭 AI Comedy ## 🚀 Quick Start

### Prerequisites

1. **Configure Orfeo Access:**
   Create a `.env` file in the root directory with your Orfeo credentials:
   ```bash
   TOKEN=<your-token-of-any-model>
   ORFEO_MODEL=<model>
   ORFEO_BASE_URL=<optional>
   ```

We used a pre-trained model hosted in a container that is in a cluster facility GPU resource, so that's why we use a baseurl.

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
- **Beautiful Terminal UI**: Rich visual presentation with colors and formatting
- **Performance Analytics**: Track comedian effectiveness over time
- **Uses Orfeo cluster** with llama3.3:latest model for superior performance

## 🚀 Quick Start

### Prerequisites (only in case of local usage on your own laptop)

1. **Install Ollama**
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
Start the visual interface with real-time performance display and human rating system:
```bash
python start_gui_rag.py
```

**GUI Features:**
- Live comedian status indicators with real-time statistics
- Interactive human rating system (😍 Love, 👍 Like, 😐 Meh, 👎 Dislike, 🤮 Hate)
- Visual audience reaction simulation with dual scoring system
- Complete show logging with timestamps and performance analytics
- Color-coded comedian identification
- Interactive buttons to start/stop shows
- Adaptive learning system based on human feedback



## 📁 Project Structure

**Public Repository Structure:**
```
├── main_clean_rag.py           # 🚀 Terminal entry point with RAG + Orfeo
├── start_gui_rag.py            # 🎨 GUI launcher with rating system
├── src/
│   ├── core/
│   │   ├── comedy_club_clean.py    # Main ComedyClub class with Orfeo integration
│   │   └── orfeo_client_new.py     # Orfeo client for llama3.3:latest
│   ├── agents/
│   │   └── comedians.py        # 4 comedian personalities (Dave, Sarah, Mike, Lisa)
│   ├── gui/
│   │   └── comedy_club_gui.py  # Tkinter GUI with human rating system
│   └── utils/
│       ├── enhanced_joke_rag.py    # RAG system with 230k+ jokes + web search
│       ├── comedy_feedback.py      # Dual scoring system (quality + audience)
│       ├── human_rating.py         # Human rating system with adaptive learning
│       ├── adaptive_comedy.py      # Adaptive learning from human feedback
│       └── comedy_tools.py         # Advanced comedy analysis tools
├── tests/
│   └── test_enhanced_rag.py    # Orfeo connectivity and RAG tests
├── datasets/
│   └── [joke datasets]         # 230k+ jokes and categorized content
├── scripts/
│   └── [utility scripts]       # Data processing and setup scripts
├── slides/
│   ├── slides.md              # Presentation slides (Marp format)
│   └── images/                # Presentation images and diagrams
├── logs/                       # 📊 Generated performance logs (auto-created)
├── requirements.txt            # 📋 Python dependencies
└── README.md                   # � This documentation
```

**Local Development (gitignored):**
```
├── examples/                   # � Simplified examples for learning
├── config/                     # 🔧 Configuration files and credentials
├── papers/                     # � Research papers and documentation
└── .env                        # � Environment variables and tokens
```

## 📊 SLIDES VISUALISATION

For all the information about the project, please refer to the slides folder. Here's a tutorial on how to work with Marp slides:

#### Requirements: marp (Markdown presentation ecosystem)

#### 4. **Export to HTML**
For VSCode users, install the extension trough VSCode GUI.
Then install the required tools -- [follow this documentation as well](https://github.com/marp-team/marp-cli):

```bash
# Install Marp CLI (if not already installed)
npm install -g @marp-team/marp-cli

#Install live-server

npm install -g live-server

```

```bash
# Convert slides to HTML
marp slides.md --html --watch --output slides.html

# To deploy

live-server .

```


## 📚 References

- [Short jokes dataset](https://www.kaggle.com/datasets/abhinavmoudgil95/short-jokes/data)
- [Jester dataset](https://www.kaggle.com/datasets/vikashrajluhaniwal/jester-17m-jokes-ratings-dataset)
- [Sciagents repo](https://github.com/lamm-mit/SciAgentsDiscovery)
- [Agent hospital paper](https://arxiv.org/abs/2405.02957)
- [The CARLIN Method article](https://gregrobison.medium.com/the-carlin-method-teaching-ai-how-to-be-genuinely-funny-2bd5e45deaf2)
