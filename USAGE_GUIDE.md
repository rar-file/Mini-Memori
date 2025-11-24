# Usage Guide - Mini Memori

Comprehensive guide to using Mini Memori effectively.

## Table of Contents

1. [Basic Usage](#basic-usage)
2. [Advanced Features](#advanced-features)
3. [Chatbot Usage](#chatbot-usage)
4. [Best Practices](#best-practices)
5. [Common Patterns](#common-patterns)
6. [Troubleshooting](#troubleshooting)

---

## Basic Usage

### 1. Initialize the Engine

```python
from mini_memori import MemoryEngine

# Basic initialization (uses defaults from .env or config)
engine = MemoryEngine()

# Custom configuration
engine = MemoryEngine(
    db_path="my_memories.db",
    embedding_model="text-embedding-3-small",
    api_key="your-api-key"
)
```

### 2. Save Messages

```python
# Simple save
message_id = engine.save_message(
    role="user",
    content="My favorite color is blue",
    conversation_id="conversation_1"
)

# With metadata
message_id = engine.save_message(
    role="user",
    content="I love programming in Python",
    conversation_id="conversation_1",
    metadata={
        "timestamp": "2024-01-15T10:30:00",
        "source": "user_input",
        "category": "preferences"
    }
)
```

### 3. Retrieve Memories

```python
# Basic retrieval
memories = engine.retrieve_memories(
    query="What's my favorite color?",
    top_k=5
)

# With conversation filter
memories = engine.retrieve_memories(
    query="What do I like?",
    top_k=3,
    conversation_id="conversation_1"
)

# With similarity threshold
memories = engine.retrieve_memories(
    query="programming preferences",
    top_k=5,
    threshold=0.8  # Only highly relevant results
)

# Process results
for memory in memories:
    print(f"Similarity: {memory['similarity']:.3f}")
    print(f"{memory['role']}: {memory['content']}")
    print(f"From: {memory['conversation_id']}")
    print()
```

### 4. Get Conversation History

```python
# Get recent messages
history = engine.get_conversation_history(
    conversation_id="conversation_1",
    limit=50
)

# Process history
for message in history:
    print(f"[{message['timestamp']}] {message['role']}: {message['content']}")
```

### 5. Manage Conversations

```python
# Get statistics
stats = engine.get_statistics()
print(f"Total messages: {stats['total_messages']}")
print(f"Total conversations: {stats['total_conversations']}")

# Clear a conversation
deleted_count = engine.clear_conversation("conversation_1")
print(f"Deleted {deleted_count} messages")

# Search by keyword
matches = engine.search_by_keyword(
    keyword="Python",
    conversation_id="conversation_1",
    limit=10
)
```

---

## Advanced Features

### 1. Batch Message Saving

```python
# Save multiple messages efficiently
messages = [
    ("user", "I work in software engineering"),
    ("assistant", "That's a great field!"),
    ("user", "I specialize in backend development"),
    ("assistant", "Backend is crucial for applications"),
]

for role, content in messages:
    engine.save_message(
        role=role,
        content=content,
        conversation_id="work_chat"
    )
```

### 2. Context-Aware Retrieval

```python
def get_contextual_response(user_query: str, conversation_id: str) -> str:
    """Get response with relevant context from memory."""
    
    # Retrieve relevant memories
    memories = engine.retrieve_memories(
        query=user_query,
        top_k=3,
        conversation_id=conversation_id,
        threshold=0.7
    )
    
    # Build context
    context = "\n".join([
        f"{m['role']}: {m['content']}" 
        for m in memories
    ])
    
    # Use context in your application
    return context

# Usage
context = get_contextual_response(
    "What are my technical skills?",
    "work_chat"
)
print(context)
```

### 3. Memory Filtering

```python
def filter_memories_by_date(memories, start_date, end_date):
    """Filter memories by date range."""
    from datetime import datetime
    
    filtered = []
    for memory in memories:
        timestamp = datetime.fromisoformat(memory['timestamp'])
        if start_date <= timestamp <= end_date:
            filtered.append(memory)
    
    return filtered

# Usage
from datetime import datetime, timedelta

all_memories = engine.retrieve_memories("programming", top_k=100)
recent = filter_memories_by_date(
    all_memories,
    datetime.now() - timedelta(days=7),
    datetime.now()
)
```

### 4. Custom Search Strategies

```python
def multi_query_search(queries: list, top_k_per_query: int = 3) -> list:
    """Search with multiple queries and combine results."""
    all_memories = []
    seen_ids = set()
    
    for query in queries:
        memories = engine.retrieve_memories(query, top_k=top_k_per_query)
        
        for memory in memories:
            if memory['id'] not in seen_ids:
                all_memories.append(memory)
                seen_ids.add(memory['id'])
    
    # Sort by similarity
    all_memories.sort(key=lambda x: x['similarity'], reverse=True)
    return all_memories

# Usage
memories = multi_query_search([
    "Python programming",
    "software development",
    "coding best practices"
])
```

---

## Chatbot Usage

### 1. Interactive CLI

```bash
# Start the chatbot
python -m mini_memori.chatbot

# Or use the installed command
mini-memori-chat
```

### 2. Programmatic Usage

```python
from mini_memori.chatbot import MemoriChatbot

# Create chatbot
chatbot = MemoriChatbot(
    conversation_id="my_session",
    chat_model="gpt-4o-mini",
    memory_top_k=5  # Number of memories to use as context
)

# Chat
response = chatbot.chat("What's my name?")
print(response)

# Get statistics
chatbot.show_statistics()

# Show history
chatbot.show_recent_history(limit=10)

# Search memories
chatbot.search_memories("favorite things")
```

### 3. Custom Chatbot

```python
from mini_memori import MemoryEngine
import openai

class CustomChatbot:
    def __init__(self, engine: MemoryEngine):
        self.engine = engine
        self.conversation_id = "custom_chat"
    
    def chat(self, user_message: str) -> str:
        # Save user message
        self.engine.save_message(
            role="user",
            content=user_message,
            conversation_id=self.conversation_id
        )
        
        # Get relevant context
        memories = self.engine.retrieve_memories(
            query=user_message,
            top_k=3,
            conversation_id=self.conversation_id
        )
        
        # Build context
        context = "Relevant memories:\n"
        for m in memories:
            context += f"- {m['content']}\n"
        
        # Get response from OpenAI
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant with memory."},
                {"role": "system", "content": context},
                {"role": "user", "content": user_message}
            ]
        )
        
        assistant_message = response.choices[0].message.content
        
        # Save response
        self.engine.save_message(
            role="assistant",
            content=assistant_message,
            conversation_id=self.conversation_id
        )
        
        return assistant_message

# Usage
engine = MemoryEngine()
bot = CustomChatbot(engine)
response = bot.chat("Hello, I'm Alice!")
print(response)
```

---

## Best Practices

### 1. Conversation Organization

```python
# Use meaningful conversation IDs
conversation_id = f"user_{user_id}_session_{session_id}"

# Organize by topic
engine.save_message(role="user", content="...", conversation_id="tech_support")
engine.save_message(role="user", content="...", conversation_id="sales")
```

### 2. Metadata Usage

```python
# Add useful metadata
engine.save_message(
    role="user",
    content="I want to buy product X",
    conversation_id="sales",
    metadata={
        "user_id": "12345",
        "product_id": "X",
        "intent": "purchase",
        "priority": "high"
    }
)
```

### 3. Error Handling

```python
from mini_memori import MemoryEngine

try:
    engine = MemoryEngine()
    
    memories = engine.retrieve_memories(
        query="test query",
        top_k=5
    )
    
except ValueError as e:
    print(f"Configuration error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

### 4. Resource Management

```python
# Use context manager for automatic cleanup
with MemoryEngine() as engine:
    engine.save_message(role="user", content="Hello")
    memories = engine.retrieve_memories("greeting")

# Or manual cleanup
engine = MemoryEngine()
try:
    # Your code here
    pass
finally:
    engine.close()
```

---

## Common Patterns

### 1. Personal Assistant

```python
class PersonalAssistant:
    def __init__(self):
        self.engine = MemoryEngine(db_path="assistant.db")
        self.user_id = "user_123"
    
    def remember(self, info: str):
        """Store information."""
        self.engine.save_message(
            role="user",
            content=info,
            conversation_id=f"user_{self.user_id}",
            metadata={"type": "preference"}
        )
        return "I'll remember that!"
    
    def recall(self, query: str):
        """Recall information."""
        memories = self.engine.retrieve_memories(
            query=query,
            top_k=3,
            conversation_id=f"user_{self.user_id}"
        )
        
        if memories:
            return memories[0]['content']
        return "I don't recall that."

# Usage
assistant = PersonalAssistant()
assistant.remember("My favorite food is pizza")
print(assistant.recall("What's my favorite food?"))
```

### 2. Knowledge Base

```python
class KnowledgeBase:
    def __init__(self):
        self.engine = MemoryEngine(db_path="knowledge.db")
    
    def add_fact(self, fact: str, category: str):
        """Add a fact to the knowledge base."""
        self.engine.save_message(
            role="system",
            content=fact,
            conversation_id=category,
            metadata={"type": "fact"}
        )
    
    def query(self, question: str, category: str = None):
        """Query the knowledge base."""
        return self.engine.retrieve_memories(
            query=question,
            top_k=5,
            conversation_id=category
        )

# Usage
kb = KnowledgeBase()
kb.add_fact("Python was created by Guido van Rossum", "programming")
kb.add_fact("The capital of France is Paris", "geography")

results = kb.query("Who created Python?")
```

### 3. Conversation Analytics

```python
def analyze_conversation(engine, conversation_id):
    """Analyze a conversation."""
    history = engine.get_conversation_history(
        conversation_id,
        limit=1000
    )
    
    # Count messages by role
    role_counts = {}
    for msg in history:
        role = msg['role']
        role_counts[role] = role_counts.get(role, 0) + 1
    
    # Find common topics
    all_content = " ".join([msg['content'] for msg in history])
    
    return {
        'message_count': len(history),
        'role_counts': role_counts,
        'avg_length': sum(len(m['content']) for m in history) / len(history)
    }

# Usage
stats = analyze_conversation(engine, "conversation_1")
print(f"Messages: {stats['message_count']}")
```

---

## Troubleshooting

### Issue: "No memories found"

**Solution**: Check that:
1. Messages were saved with embeddings
2. Similarity threshold isn't too high
3. Query is relevant to stored content

```python
# Lower the threshold
memories = engine.retrieve_memories(query, threshold=0.3)

# Increase top_k
memories = engine.retrieve_memories(query, top_k=10)
```

### Issue: "API rate limit"

**Solution**: Implement retry logic or batch processing

```python
import time

def save_with_retry(engine, role, content, max_retries=3):
    for attempt in range(max_retries):
        try:
            return engine.save_message(role, content)
        except Exception as e:
            if "rate_limit" in str(e).lower():
                time.sleep(2 ** attempt)  # Exponential backoff
            else:
                raise
```

### Issue: "Database locked"

**Solution**: Ensure only one connection at a time

```python
# Use context manager
with MemoryEngine() as engine:
    # Your code here
    pass

# Or ensure proper cleanup
engine = MemoryEngine()
try:
    # Your code
    pass
finally:
    engine.close()
```

---

For more help, see:
- [README.md](README.md) - Complete documentation
- [QUICKSTART.md](QUICKSTART.md) - Quick start guide
- [examples/](examples/) - Example scripts
- [GitHub Issues](https://github.com/yourusername/mini-memori/issues)
