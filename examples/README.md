# Examples README

This directory contains example scripts demonstrating different use cases for Mini Memori.

## Available Examples

### 1. Basic Usage (`basic_usage.py`)

Demonstrates fundamental operations:
- Creating a memory engine
- Saving messages with embeddings
- Retrieving relevant memories
- Getting conversation history
- Viewing statistics

**Run:**
```bash
python examples/basic_usage.py
```

### 2. Chatbot Demo (`chatbot_demo.py`)

Shows how to create a custom chatbot:
- Programmatic chatbot usage
- Custom conversation settings
- Memory-enhanced responses

**Run:**
```bash
python examples/chatbot_demo.py
```

### 3. Batch Import (`batch_import.py`)

Import existing conversations:
- Import from JSON files
- Import conversation pairs
- Bulk data loading

**Run:**
```bash
python examples/batch_import.py
```

### 4. Memory Search (`memory_search.py`)

Advanced search techniques:
- Semantic similarity search
- Filtered search by conversation
- Threshold-based filtering
- Keyword search

**Run:**
```bash
python examples/memory_search.py
```

## Prerequisites

Make sure you have:
1. Installed Mini Memori: `pip install -e .`
2. Set your OpenAI API key: `export OPENAI_API_KEY=your_key`
3. Installed dependencies: `pip install -r requirements.txt`

## Notes

- Each example creates its own database file to avoid conflicts
- Examples include detailed console output showing what's happening
- Check the source code for detailed comments and explanations
