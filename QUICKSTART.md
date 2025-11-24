# Quick Start Guide

Get up and running with Mini Memori in 5 minutes!

## 1. Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd mini-memori

# Install dependencies
pip install -e .
```

## 2. Set Up API Key

Create a `.env` file in the project root:

```bash
OPENAI_API_KEY=your_api_key_here
```

Or set it in your environment:

```bash
# Linux/Mac
export OPENAI_API_KEY=your_api_key_here

# Windows PowerShell
$env:OPENAI_API_KEY="your_api_key_here"
```

## 3. Run Your First Example

```bash
python examples/basic_usage.py
```

This will:
- Create a memory database
- Save some test messages
- Retrieve relevant memories
- Show statistics

## 4. Try the Interactive Chatbot

```bash
python -m mini_memori.chatbot
```

Or use the installed command:

```bash
mini-memori-chat
```

### Available Commands:

- `/help` - Show help
- `/stats` - Show memory statistics
- `/history` - Show conversation history
- `/search <query>` - Search memories
- `/clear` - Clear conversation
- `/quit` - Exit

## 5. Use in Your Code

```python
from mini_memori import MemoryEngine

# Create engine
engine = MemoryEngine()

# Save a message
engine.save_message(
    role="user",
    content="My favorite programming language is Python",
    conversation_id="my_conversation"
)

# Retrieve relevant memories
memories = engine.retrieve_memories(
    query="What's my favorite language?",
    top_k=3
)

for memory in memories:
    print(f"{memory['role']}: {memory['content']}")
    print(f"Similarity: {memory['similarity']:.3f}\n")
```

## Common Use Cases

### 1. Personal Assistant

```python
from mini_memori.chatbot import MemoriChatbot

chatbot = MemoriChatbot(conversation_id="assistant")

# The chatbot remembers previous conversations
response = chatbot.chat("Remember that I like coffee")
print(response)

# Later...
response = chatbot.chat("What do I like to drink?")
print(response)  # Will reference that you like coffee
```

### 2. Knowledge Base

```python
engine = MemoryEngine(db_path="knowledge.db")

# Add knowledge
facts = [
    "The capital of France is Paris",
    "Python was created by Guido van Rossum",
    "The Eiffel Tower was built in 1889"
]

for fact in facts:
    engine.save_message(role="system", content=fact)

# Query knowledge
results = engine.retrieve_memories("Who created Python?", top_k=1)
print(results[0]['content'])
```

### 3. Conversation Analysis

```python
# Get all conversations
stats = engine.get_statistics()
print(f"Total conversations: {stats['total_conversations']}")

# Search across conversations
memories = engine.retrieve_memories(
    query="machine learning",
    top_k=10
)

# Analyze results
for memory in memories:
    print(f"Conversation: {memory['conversation_id']}")
    print(f"Content: {memory['content']}\n")
```

## Next Steps

1. **Explore Examples**: Check out the `examples/` directory
2. **Read the Docs**: See README.md for full API reference
3. **Run Tests**: `pytest tests/` to verify everything works
4. **Customize**: Modify chatbot behavior, add features
5. **Contribute**: See CONTRIBUTING.md

## Troubleshooting

### API Key Error
```
ValueError: OpenAI API key is required
```
**Solution**: Set your `OPENAI_API_KEY` environment variable

### Import Error
```
ModuleNotFoundError: No module named 'mini_memori'
```
**Solution**: Install in development mode: `pip install -e .`

### Database Locked
```
sqlite3.OperationalError: database is locked
```
**Solution**: Close other connections or wait for operations to complete

## Need Help?

- Check the [README.md](README.md) for detailed documentation
- Look at [examples/](examples/) for more code samples
- Open an issue on GitHub

---

Happy coding! 🚀
