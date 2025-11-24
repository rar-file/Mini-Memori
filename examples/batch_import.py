"""
Batch import example for Mini Memori.

Shows how to import existing conversations or data into the memory system.
"""

from mini_memori import MemoryEngine
from mini_memori.config import setup_logging
import json
from typing import List, Dict, Any

setup_logging("INFO")


def import_from_json(engine: MemoryEngine, json_file: str, conversation_id: str):
    """
    Import messages from a JSON file.
    
    Expected format:
    [
        {"role": "user", "content": "message", "metadata": {}},
        {"role": "assistant", "content": "response", "metadata": {}},
        ...
    ]
    """
    print(f"\n📥 Importing from {json_file}...")
    
    with open(json_file, 'r', encoding='utf-8') as f:
        messages = json.load(f)
    
    for i, msg in enumerate(messages, 1):
        engine.save_message(
            role=msg['role'],
            content=msg['content'],
            conversation_id=conversation_id,
            metadata=msg.get('metadata')
        )
        print(f"   ✓ Imported message {i}/{len(messages)}")
    
    print(f"✅ Successfully imported {len(messages)} messages!")


def import_conversation_pairs(
    engine: MemoryEngine,
    conversations: List[Dict[str, str]],
    conversation_id: str
):
    """
    Import conversation pairs (user/assistant).
    
    Args:
        conversations: List of dicts with 'user' and 'assistant' keys
    """
    print(f"\n📥 Importing {len(conversations)} conversation pairs...")
    
    count = 0
    for i, pair in enumerate(conversations, 1):
        # Save user message
        engine.save_message(
            role="user",
            content=pair['user'],
            conversation_id=conversation_id
        )
        
        # Save assistant response
        engine.save_message(
            role="assistant",
            content=pair['assistant'],
            conversation_id=conversation_id
        )
        
        count += 2
        print(f"   ✓ Imported pair {i}/{len(conversations)}")
    
    print(f"✅ Successfully imported {count} messages!")


def main():
    print("\n" + "="*60)
    print("📦 Batch Import Example")
    print("="*60)
    
    # Initialize engine
    engine = MemoryEngine(db_path="imported_memories.db")
    
    # Example: Import conversation pairs
    sample_conversations = [
        {
            "user": "What's the capital of France?",
            "assistant": "The capital of France is Paris."
        },
        {
            "user": "Tell me about the Eiffel Tower.",
            "assistant": "The Eiffel Tower is a wrought-iron lattice tower in Paris, France. It was constructed in 1889 and is one of the most recognizable structures in the world."
        },
        {
            "user": "What's the population of Paris?",
            "assistant": "Paris has a population of approximately 2.2 million people within the city proper, and about 12 million in the metropolitan area."
        },
    ]
    
    import_conversation_pairs(
        engine,
        sample_conversations,
        conversation_id="paris_facts"
    )
    
    # Test retrieval
    print("\n🔍 Testing retrieval after import...")
    query = "Tell me about Paris"
    memories = engine.retrieve_memories(query, top_k=3)
    
    print(f"\nQuery: '{query}'")
    print(f"Found {len(memories)} relevant memories:\n")
    
    for i, memory in enumerate(memories, 1):
        print(f"[{i}] (similarity: {memory['similarity']:.3f})")
        print(f"    {memory['role']}: {memory['content']}")
        print()
    
    # Show final statistics
    print("-"*60)
    stats = engine.get_statistics()
    print("\n📊 Final Statistics:")
    print(f"   Total messages: {stats['total_messages']}")
    print(f"   Total conversations: {stats['total_conversations']}")
    print(f"   Total embeddings: {stats['total_embeddings']}")
    
    print("\n✅ Batch import completed!")
    print(f"💾 Database: {engine.db_path}\n")
    
    engine.close()


if __name__ == "__main__":
    main()
