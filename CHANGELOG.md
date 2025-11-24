# Changelog

All notable changes to Mini Memori will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-11-24

### Added
- Initial release of Mini Memori
- Core `MemoryEngine` class for memory management
- SQLite database backend with full schema
- OpenAI embeddings integration
- Vector similarity search with cosine similarity
- Interactive CLI chatbot interface
- Configuration management with environment variables
- Comprehensive utility functions
- Full test suite with unit and integration tests
- Documentation and examples:
  - Basic usage example
  - Chatbot demo
  - Batch import example
  - Advanced search techniques
- Context manager support for engine and database
- Conversation management (create, retrieve, clear)
- Message metadata support
- Statistics and analytics
- Keyword search functionality
- Top-k retrieval with threshold filtering

### Features

#### Memory Engine
- Save messages with automatic embedding generation
- Retrieve relevant memories using semantic search
- Get conversation history with pagination
- Clear conversations
- Database statistics

#### Chatbot
- Interactive CLI interface
- Long-term memory across sessions
- Context-aware responses
- Built-in commands (/help, /stats, /history, /search, /clear, /quit)
- Memory retrieval for enhanced context

#### Database
- SQLite with WAL mode for better concurrency
- Optimized indexes for performance
- Foreign key constraints
- Conversation metadata tracking

#### Configuration
- Environment variable support
- .env file loading
- Configurable models and paths
- Logging configuration

### Documentation
- Comprehensive README with examples
- API reference documentation
- Contributing guidelines
- Example scripts
- Test coverage

### Technical Details
- Python 3.8+ support
- Type hints throughout codebase
- Proper error handling and logging
- PEP 8 compliant code style

---

## [Unreleased]

### Planned Features
- Support for additional embedding providers
- Web interface for memory exploration
- Export/import in multiple formats
- Memory pruning and archiving
- Advanced filtering and search operators
- Performance optimizations
- Async support
- Streaming responses

---

For more details, see the [commit history](https://github.com/yourusername/mini-memori/commits/main).
