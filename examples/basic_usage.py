"""
Basic usage example for Mini Memori.

Demonstrates:
- Creating a memory engine
- Saving messages
- Retrieving relevant memories
"""

from mini_memori import MemoryEngine
from mini_memori.config import setup_logging

# Set up logging to see what's happening
setup_logging("INFO")


def main():
    print("🧠 Mini Memori - Basic Usage Example\n")
    print("="*60)
    
    # Initialize the memory engine
    print("\n1. Initializing Memory Engine...")
    engine = MemoryEngine(db_path="example_memories.db")
    print(f"   ✓ Connected to database: {engine.db_path}")
    
    # Save some messages
    print("\n2. Saving messages to memory...")
    
    messages = [
        ("user", "My name is Alice and I love Python programming."),
        ("assistant", "Nice to meet you, Alice! Python is a great language."),
        ("user", "I'm working on a machine learning project about image classification."),
        ("assistant", "Image classification is fascinating! Are you using PyTorch or TensorFlow?"),
        ("user", "I'm using PyTorch. My favorite color is blue."),
        ("assistant", "PyTorch is excellent for research. Blue is a calming color!"),
    ]
    
    for role, content in messages:
        msg_id = engine.save_message(
            role=role,
            content=content,
            conversation_id="example_conversation"
        )
        print(f"   ✓ Saved message {msg_id}: {content[:50]}...")
    
    # Retrieve relevant memories
    print("\n3. Retrieving relevant memories...")
    
    queries = [
        "What is my name?",
        "What is my favorite color?",
        "What am I working on?",
    ]
    
    for query in queries:
        print(f"\n   Query: '{query}'")
        memories = engine.retrieve_memories(
            query=query,
            top_k=2,
            conversation_id="example_conversation"
        )
        
        for i, memory in enumerate(memories, 1):
            similarity = memory['similarity']
            content = memory['content']
            print(f"     [{i}] (similarity: {similarity:.3f})")
            print(f"         {memory['role']}: {content}")
    
    # Get conversation history
    print("\n4. Getting conversation history...")
    history = engine.get_conversation_history("example_conversation")
    print(f"   ✓ Found {len(history)} messages in conversation")
    
    # Show statistics
    print("\n5. Memory Statistics:")
    stats = engine.get_statistics()
    print(f"   Total messages: {stats['total_messages']}")
    print(f"   Total conversations: {stats['total_conversations']}")
    print(f"   Total embeddings: {stats['total_embeddings']}")
    
    print("\n" + "="*60)
    print("✅ Example completed successfully!")
    print(f"💾 Database saved to: {engine.db_path}")
    
    # Clean up
    engine.close()


if __name__ == "__main__":
    main()
