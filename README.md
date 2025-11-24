# Mini Memori - Local Memory Engine for LLMs

A lightweight, production-ready memory system that stores conversations and retrieves relevant context using OpenAI embeddings. Perfect for building chatbots with long-term memory.

## ✨ Features

- 💾 **Persistent Storage**: SQLite database for reliable conversation storage
- 🧠 **Vector Embeddings**: OpenAI embeddings for semantic similarity search
- 🔍 **Smart Retrieval**: Top-k memory retrieval based on context relevance
- 💬 **Chatbot Integration**: Ready-to-use CLI chatbot interface
- 🎯 **Simple API**: Clean, intuitive Python API
- 🚀 **Production Ready**: Proper error handling, logging, and type hints

## 📦 Installation

### From Source

```bash
# Clone the repository
git clone <your-repo-url>
cd mini-memori

# Install in development mode
pip install -e .
```

### Requirements

- Python 3.8+
- OpenAI API key

## 🔧 Configuration

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_api_key_here
```

Or set the environment variable:

```bash
export OPENAI_API_KEY=your_api_key_here
```

## 🚀 Quick Start

### Try the Demo

```bash
# Run quick demo to see it in action
python demo.py

# Or verify your installation
python verify_installation.py
```

### Basic Usage

```python
from mini_memori import MemoryEngine

# Initialize the engine
engine = MemoryEngine(db_path="memories.db")

# Save a message
engine.save_message(
    role="user",
    content="My favorite color is blue",
    conversation_id="conv_1"
)

# Retrieve relevant memories
memories = engine.retrieve_memories(
    query="What is my favorite color?",
    top_k=5
)

for memory in memories:
    print(f"{memory['role']}: {memory['content']}")
```

### Run the Chatbot

```bash
# Start the interactive chatbot
python -m mini_memori.chatbot

# Or use the convenience command
mini-memori-chat
```

## 📚 API Reference

### MemoryEngine

#### `__init__(db_path: str = "memories.db", embedding_model: str = "text-embedding-3-small")`

Initialize the memory engine.

**Parameters:**
- `db_path`: Path to SQLite database file
- `embedding_model`: OpenAI embedding model to use

#### `save_message(role: str, content: str, conversation_id: str = "default", metadata: dict = None) -> int`

Save a message with its embedding to the database.

**Parameters:**
- `role`: Message role (e.g., "user", "assistant", "system")
- `content`: Message content
- `conversation_id`: Conversation identifier
- `metadata`: Optional metadata dictionary

**Returns:** Message ID

#### `retrieve_memories(query: str, top_k: int = 5, conversation_id: str = None, threshold: float = 0.0) -> List[dict]`

Retrieve the most relevant memories based on semantic similarity.

**Parameters:**
- `query`: Search query
- `top_k`: Number of results to return
- `conversation_id`: Optional conversation filter
- `threshold`: Minimum similarity threshold (0-1)

**Returns:** List of memory dictionaries with similarity scores

#### `get_conversation_history(conversation_id: str, limit: int = 50) -> List[dict]`

Get recent messages from a specific conversation.

**Parameters:**
- `conversation_id`: Conversation identifier
- `limit`: Maximum number of messages to return

**Returns:** List of messages ordered by timestamp

#### `clear_conversation(conversation_id: str) -> int`

Delete all messages from a conversation.

**Parameters:**
- `conversation_id`: Conversation identifier

**Returns:** Number of messages deleted

#### `get_statistics() -> dict`

Get database statistics.

**Returns:** Dictionary with total messages, conversations, and date ranges

## 🏗️ Architecture

```
mini_memori/
├── __init__.py          # Package initialization
├── engine.py            # Core MemoryEngine class
├── database.py          # Database schema and operations
├── embeddings.py        # OpenAI embeddings integration
├── chatbot.py           # Interactive chatbot interface
├── config.py            # Configuration management
└── utils.py             # Utility functions
```

### How It Works

1. **Message Storage**: When you save a message, it's stored in SQLite with a timestamp
2. **Embedding Generation**: OpenAI's API generates a vector embedding for the content
3. **Similarity Search**: Retrieval uses cosine similarity to find the most relevant memories
4. **Context Assembly**: Top-k memories are returned with similarity scores

## 🎯 Use Cases

- **Personal AI Assistants**: Build chatbots that remember user preferences
- **Knowledge Management**: Store and retrieve information semantically
- **Conversation Analysis**: Track and analyze conversation patterns
- **Context-Aware Systems**: Provide relevant historical context to LLMs

## 📝 Examples

See the `examples/` directory for more usage examples:

- `basic_usage.py`: Simple save and retrieve operations
- `chatbot_demo.py`: Custom chatbot implementation
- `batch_import.py`: Importing existing conversations
- `memory_search.py`: Advanced search techniques

## 🧪 Testing

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=mini_memori tests/
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for the embeddings API
- SQLite for the reliable database engine

## 📧 Contact

Project Link: [https://github.com/rar-file/mini-memori](https://github.com/yourusername/mini-memori)

---

Built with ❤️ for the AI community

