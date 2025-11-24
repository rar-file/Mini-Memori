# Getting Started with Mini Memori 🧠

Welcome to **Mini Memori** - Your Local Memory Engine for LLMs!

## What You've Got

A complete, production-ready memory system with:

✅ **Core Package** - 8 Python modules, ~2000+ lines of code  
✅ **Interactive Chatbot** - CLI with memory capabilities  
✅ **4 Working Examples** - Ready to run demonstrations  
✅ **40+ Unit Tests** - Comprehensive test coverage  
✅ **8 Documentation Files** - Everything you need to know  
✅ **CI/CD Pipeline** - GitHub Actions ready  
✅ **Deployment Guides** - Docker, AWS, GCP, Heroku  

---

## 🚀 Quick Start (5 minutes)

### Step 1: Install Dependencies

```bash
pip install -e .
```

This installs:
- `openai` - For embeddings
- `numpy` - For vector operations
- `python-dotenv` - For environment management

### Step 2: Set Your API Key

**Option A: Environment Variable**
```bash
# Linux/Mac
export OPENAI_API_KEY=your_key_here

# Windows PowerShell
$env:OPENAI_API_KEY="your_key_here"
```

**Option B: .env File**
```bash
# Copy example
cp .env.example .env

# Edit and add your key
# OPENAI_API_KEY=your_key_here
```

### Step 3: Verify Installation

```bash
python verify_installation.py
```

### Step 4: Try It Out!

```bash
# Run basic example
python examples/basic_usage.py

# Start interactive chatbot
python -m mini_memori.chatbot
```

---

## 📚 What to Explore Next

### 1. Run the Examples

```bash
# Basic operations
python examples/basic_usage.py

# Chatbot demo
python examples/chatbot_demo.py

# Batch data import
python examples/batch_import.py

# Advanced search
python examples/memory_search.py
```

### 2. Read the Documentation

- **README.md** - Complete API reference
- **QUICKSTART.md** - Detailed quick start
- **USAGE_GUIDE.md** - Comprehensive usage patterns
- **PROJECT_SUMMARY.md** - Full project overview

### 3. Try Your Own Code

```python
from mini_memori import MemoryEngine

# Create engine
engine = MemoryEngine()

# Save a memory
engine.save_message(
    role="user",
    content="I love Python programming",
    conversation_id="my_chat"
)

# Retrieve it
memories = engine.retrieve_memories(
    query="What do I like?",
    top_k=3
)

# Print results
for memory in memories:
    print(f"{memory['content']} (score: {memory['similarity']:.3f})")
```

---

## 🎯 Common Use Cases

### Personal AI Assistant
```python
from mini_memori.chatbot import MemoriChatbot

chatbot = MemoriChatbot()
response = chatbot.chat("Remember that I like coffee")
# Later...
response = chatbot.chat("What's my favorite drink?")
```

### Knowledge Base
```python
# Add facts
engine.save_message(role="system", content="Python was created by Guido van Rossum")
engine.save_message(role="system", content="The capital of France is Paris")

# Query
results = engine.retrieve_memories("Who created Python?", top_k=1)
print(results[0]['content'])
```

### Conversation Analysis
```python
# Get statistics
stats = engine.get_statistics()
print(f"Total messages: {stats['total_messages']}")
print(f"Total conversations: {stats['total_conversations']}")

# Search across all conversations
memories = engine.retrieve_memories("machine learning", top_k=10)
```

---

## 🛠️ Project Structure

```
mini-memori/
├── mini_memori/          # 📦 Core package (use this in your code)
│   ├── engine.py         # Main MemoryEngine class
│   ├── database.py       # SQLite operations
│   ├── embeddings.py     # OpenAI embeddings
│   ├── chatbot.py        # Interactive chatbot
│   └── ...
│
├── examples/             # 📚 Example scripts (learn from these)
│   ├── basic_usage.py
│   ├── chatbot_demo.py
│   ├── batch_import.py
│   └── memory_search.py
│
├── tests/                # 🧪 Test suite (optional to run)
│   └── test_*.py
│
└── docs/                 # 📖 Documentation (read these)
    ├── README.md
    ├── QUICKSTART.md
    ├── USAGE_GUIDE.md
    └── ...
```

---

## 💡 Key Features

### 1. Save Messages
```python
engine.save_message(
    role="user",                    # or "assistant", "system"
    content="Your message here",
    conversation_id="conv_1",       # organize by conversation
    metadata={"key": "value"}       # optional extra data
)
```

### 2. Semantic Search
```python
memories = engine.retrieve_memories(
    query="What you're looking for",
    top_k=5,                        # number of results
    threshold=0.7,                  # similarity threshold
    conversation_id="conv_1"        # optional filter
)
```

### 3. Conversation Management
```python
# Get history
history = engine.get_conversation_history("conv_1", limit=50)

# Clear conversation
engine.clear_conversation("conv_1")

# Get statistics
stats = engine.get_statistics()
```

---

## 🔧 Configuration

All configuration is done via environment variables or `.env` file:

```bash
# Required
OPENAI_API_KEY=sk-your-key-here

# Optional (with defaults)
DB_PATH=memories.db                    # Database location
EMBEDDING_MODEL=text-embedding-3-small # OpenAI model
CHAT_MODEL=gpt-4o-mini                 # Chat model
LOG_LEVEL=INFO                         # Logging level
```

---

## 🧪 Testing

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=mini_memori tests/

# Run specific test
pytest tests/test_database.py -v
```

---

## 🐛 Troubleshooting

### "No module named 'mini_memori'"
```bash
# Install in development mode
pip install -e .
```

### "OpenAI API key is required"
```bash
# Set your API key
export OPENAI_API_KEY=your_key_here
```

### "No memories found"
```bash
# Lower the similarity threshold
memories = engine.retrieve_memories(query, threshold=0.3)
```

### "Database is locked"
```bash
# Ensure only one connection at a time
# Use context manager:
with MemoryEngine() as engine:
    # your code here
```

---

## 📖 Documentation Guide

1. **Just getting started?** → Read `QUICKSTART.md`
2. **Want to understand the API?** → Read `README.md`
3. **Need usage examples?** → Read `USAGE_GUIDE.md`
4. **Setting up development?** → Read `DEVELOPMENT.md`
5. **Deploying to production?** → Read `DEPLOYMENT.md`
6. **Want to contribute?** → Read `CONTRIBUTING.md`
7. **Understanding architecture?** → Read `PROJECT_STRUCTURE.md`
8. **Full overview?** → Read `PROJECT_SUMMARY.md`

---

## 🚀 Ready to Deploy?

See `DEPLOYMENT.md` for:
- Docker deployment
- Cloud platforms (AWS, GCP, Azure)
- Production best practices
- Security considerations
- Monitoring and logging

---

## 🤝 Contributing

We welcome contributions! See `CONTRIBUTING.md` for:
- Development setup
- Code style guidelines
- Pull request process
- Testing requirements

---

## 📊 Project Stats

- **Lines of Code**: ~2000+
- **Test Files**: 4 (40+ tests)
- **Documentation**: 8 comprehensive guides
- **Examples**: 4 working demos
- **Dependencies**: 3 (openai, numpy, python-dotenv)
- **Python Version**: 3.8+
- **License**: MIT

---

## 🎉 You're Ready!

You now have everything you need to build LLM applications with long-term memory.

### Next Steps:

1. ✅ Run `python verify_installation.py`
2. ✅ Try `python examples/basic_usage.py`
3. ✅ Start `python -m mini_memori.chatbot`
4. ✅ Read `USAGE_GUIDE.md` for advanced patterns
5. ✅ Build something amazing!

---

## 📧 Need Help?

- 📚 Check the documentation files
- 💬 Open a GitHub issue
- 📖 Read the examples
- 🔍 Search existing issues

---

## ⭐ Show Your Support

If you find this project helpful:
- ⭐ Star the repository
- 🐛 Report bugs
- 💡 Suggest features
- 🤝 Contribute code
- 📖 Improve documentation

---

**Happy coding with Mini Memori!** 🧠✨

Built with ❤️ for the AI community
Version 1.0.0 | November 2025

---

## Quick Command Reference

```bash
# Installation
pip install -e .

# Verification
python verify_installation.py

# Examples
python examples/basic_usage.py
python examples/chatbot_demo.py

# Interactive Chatbot
python -m mini_memori.chatbot

# Testing
pytest tests/
pytest --cov=mini_memori tests/

# Chatbot Commands
/help     - Show help
/stats    - Statistics
/history  - Recent messages
/search   - Search memories
/clear    - Clear conversation
/quit     - Exit
```

---

**Your memory-enhanced AI journey starts now!** 🚀
