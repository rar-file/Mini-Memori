# Mini Memori - Project Structure

```
mini-memori/
├── mini_memori/              # Main package directory
│   ├── __init__.py          # Package initialization, exports main classes
│   ├── __main__.py          # Entry point for `python -m mini_memori`
│   ├── engine.py            # Core MemoryEngine class
│   ├── database.py          # SQLite database operations
│   ├── embeddings.py        # OpenAI embeddings and similarity
│   ├── chatbot.py           # Interactive chatbot interface
│   ├── config.py            # Configuration management
│   └── utils.py             # Utility functions
│
├── examples/                 # Example scripts
│   ├── README.md            # Examples documentation
│   ├── basic_usage.py       # Basic save/retrieve operations
│   ├── chatbot_demo.py      # Custom chatbot implementation
│   ├── batch_import.py      # Importing existing data
│   └── memory_search.py     # Advanced search techniques
│
├── tests/                    # Test suite
│   ├── __init__.py          # Test package initialization
│   ├── test_database.py     # Database module tests
│   ├── test_embeddings.py   # Embeddings module tests
│   ├── test_utils.py        # Utility functions tests
│   └── test_integration.py  # Integration tests
│
├── docs/                     # Documentation (future)
│
├── .env.example             # Example environment variables
├── .gitignore               # Git ignore patterns
├── CHANGELOG.md             # Version history
├── CONTRIBUTING.md          # Contribution guidelines
├── LICENSE                  # MIT License
├── QUICKSTART.md            # Quick start guide
├── README.md                # Main documentation
├── requirements.txt         # Python dependencies
└── setup.py                 # Package installation script
```

## Module Descriptions

### Core Package (`mini_memori/`)

#### `engine.py`
- **MemoryEngine**: Main interface for memory operations
- Methods: save_message, retrieve_memories, get_conversation_history, clear_conversation, get_statistics
- Orchestrates database and embeddings services

#### `database.py`
- **Database**: SQLite database management
- Tables: messages, embeddings, conversations
- CRUD operations with optimized indexes
- Context manager support

#### `embeddings.py`
- **EmbeddingService**: OpenAI embeddings integration
- Vector generation and similarity calculations
- Batch processing support
- Cosine similarity implementation

#### `chatbot.py`
- **MemoriChatbot**: Interactive CLI chatbot
- Commands: /help, /stats, /history, /search, /clear, /quit
- Integrates memory for context-aware responses
- OpenAI chat completions integration

#### `config.py`
- **Config**: Configuration management
- Environment variable loading
- .env file support
- Validation and defaults

#### `utils.py`
- Formatting utilities
- Text processing
- Validation functions
- Helper methods

### Examples (`examples/`)

Each example is self-contained and demonstrates specific features:
- **basic_usage.py**: Core memory operations
- **chatbot_demo.py**: Chatbot implementation
- **batch_import.py**: Data import workflows
- **memory_search.py**: Search techniques and filtering

### Tests (`tests/`)

Comprehensive test coverage:
- **test_database.py**: Database operations (15+ tests)
- **test_embeddings.py**: Embeddings and similarity (10+ tests)
- **test_utils.py**: Utility functions (10+ tests)
- **test_integration.py**: End-to-end workflows (8+ tests)

## Key Features

### 1. Memory Storage
- SQLite database with WAL mode
- Foreign key constraints
- Optimized indexes
- Metadata support

### 2. Vector Search
- OpenAI embeddings (text-embedding-3-small/large)
- Cosine similarity calculations
- Top-k retrieval
- Threshold filtering

### 3. Chatbot Interface
- Interactive CLI
- Persistent memory across sessions
- Context-aware responses
- Built-in commands

### 4. Configuration
- Environment variables
- .env file support
- Flexible model selection
- Logging configuration

## API Overview

### MemoryEngine

```python
engine = MemoryEngine(db_path="memories.db", embedding_model="text-embedding-3-small")

# Save message
msg_id = engine.save_message(role="user", content="...", conversation_id="conv_1")

# Retrieve memories
memories = engine.retrieve_memories(query="...", top_k=5, threshold=0.7)

# Get history
history = engine.get_conversation_history(conversation_id="conv_1", limit=50)

# Statistics
stats = engine.get_statistics()
```

### Chatbot

```python
chatbot = MemoriChatbot(conversation_id="chat_1", chat_model="gpt-4o-mini")

# Chat with memory
response = chatbot.chat("What's my favorite color?")

# Show stats
chatbot.show_statistics()
```

## Dependencies

- **openai** (>=1.0.0): OpenAI API client
- **numpy** (>=1.24.0): Numerical operations
- **python-dotenv** (>=1.0.0): Environment variable management

## Development

### Setup
```bash
pip install -e .
pip install pytest pytest-cov
```

### Run Tests
```bash
pytest tests/
pytest --cov=mini_memori tests/
```

### Run Examples
```bash
python examples/basic_usage.py
python -m mini_memori.chatbot
```

## Architecture Decisions

### Why SQLite?
- Lightweight and portable
- No separate server required
- Good performance for local use
- ACID compliance

### Why OpenAI Embeddings?
- High-quality semantic representations
- Easy to use API
- Support for different model sizes
- Good documentation

### Why Cosine Similarity?
- Standard for text similarity
- Efficient computation
- Range [0, 1] is intuitive
- Works well with normalized vectors

## Performance Considerations

- **Indexes**: Optimized for common queries
- **WAL Mode**: Better concurrency
- **Batch Processing**: Efficient for multiple embeddings
- **Connection Pooling**: Single connection per engine

## Security Notes

- API keys stored in environment variables
- No hardcoded credentials
- SQL injection protection (parameterized queries)
- Input validation on all user data

## Future Enhancements

- [ ] Additional embedding providers (Cohere, Hugging Face)
- [ ] Web interface
- [ ] Export/import formats (JSON, CSV)
- [ ] Memory pruning/archiving
- [ ] Async support
- [ ] Streaming responses
- [ ] Advanced filtering
- [ ] Performance optimizations

---

**Version**: 1.0.0  
**License**: MIT  
**Python**: 3.8+
