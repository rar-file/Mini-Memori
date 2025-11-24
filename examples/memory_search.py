"""
Advanced memory search techniques.

Demonstrates different ways to search and filter memories.
"""

from mini_memori import MemoryEngine
from mini_memori.config import setup_logging
from mini_memori.utils import format_memory_output

setup_logging("INFO")


def main():
    print("\n" + "="*60)
    print("🔍 Advanced Memory Search Example")
    print("="*60)
    
    # Initialize and populate with sample data
    engine = MemoryEngine(db_path="search_demo.db")
    
    print("\n1. Populating database with sample data...")
    
    # Add diverse messages
    sample_data = [
        ("user", "I love playing guitar on weekends", "hobbies"),
        ("user", "Python is my favorite programming language", "tech"),
        ("user", "I enjoy hiking in the mountains", "hobbies"),
        ("user", "I'm learning about machine learning", "tech"),
        ("user", "My favorite food is pizza", "food"),
        ("user", "I work as a software engineer at a startup", "work"),
        ("user", "I play tennis every Tuesday", "hobbies"),
        ("user", "I'm interested in neural networks", "tech"),
    ]
    
    for role, content, conv_id in sample_data:
        engine.save_message(role, content, conversation_id=conv_id)
    
    print(f"   ✓ Added {len(sample_data)} messages")
    
    # Semantic search examples
    print("\n2. Semantic Search Examples")
    print("-"*60)
    
    search_queries = [
        ("What are my hobbies?", 3),
        ("What do I do for work?", 2),
        ("What programming topics interest me?", 3),
        ("What's my favorite food?", 1),
    ]
    
    for query, top_k in search_queries:
        print(f"\n📝 Query: '{query}'")
        memories = engine.retrieve_memories(query, top_k=top_k, threshold=0.5)
        
        if memories:
            for i, mem in enumerate(memories, 1):
                print(f"   [{i}] {mem['content']} (similarity: {mem['similarity']:.3f})")
        else:
            print("   No relevant memories found.")
    
    # Filtered search by conversation
    print("\n\n3. Filtered Search by Conversation")
    print("-"*60)
    
    print("\n🎯 Searching only in 'tech' conversation:")
    tech_memories = engine.retrieve_memories(
        "programming",
        top_k=5,
        conversation_id="tech"
    )
    
    for i, mem in enumerate(tech_memories, 1):
        print(f"   [{i}] {mem['content']} (similarity: {mem['similarity']:.3f})")
    
    # Threshold filtering
    print("\n\n4. Threshold Filtering")
    print("-"*60)
    
    print("\n🎯 High threshold (0.8) - only very relevant results:")
    high_threshold = engine.retrieve_memories(
        "software development",
        top_k=5,
        threshold=0.8
    )
    print(f"   Found {len(high_threshold)} highly relevant memories")
    
    print("\n🎯 Low threshold (0.3) - more permissive:")
    low_threshold = engine.retrieve_memories(
        "software development",
        top_k=5,
        threshold=0.3
    )
    print(f"   Found {len(low_threshold)} memories")
    
    # Keyword search
    print("\n\n5. Keyword Search (Non-Semantic)")
    print("-"*60)
    
    keyword = "learning"
    print(f"\n🔎 Keyword search for '{keyword}':")
    keyword_results = engine.search_by_keyword(keyword, limit=5)
    
    for i, msg in enumerate(keyword_results, 1):
        print(f"   [{i}] {msg['content']}")
    
    # Show all conversations
    print("\n\n6. Conversation Overview")
    print("-"*60)
    
    stats = engine.get_statistics()
    print(f"\n📊 Total conversations: {stats['total_conversations']}")
    print(f"📊 Total messages: {stats['total_messages']}")
    
    print("\n✅ Search demo completed!\n")
    
    engine.close()


if __name__ == "__main__":
    main()
