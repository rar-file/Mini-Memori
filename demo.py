"""
Simple demo script to test Mini Memori quickly.
Run this to see the system in action!
"""

import sys
import os


def print_header(text):
    """Print a formatted header."""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)


def check_api_key():
    """Check if API key is set."""
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("\n⚠️  Warning: OPENAI_API_KEY not set!")
        print("Set it with: export OPENAI_API_KEY=your_key")
        print("\nWe'll continue with mock embeddings for demonstration.\n")
        return False
    return True


def demo_basic_operations():
    """Demonstrate basic memory operations."""
    from mini_memori import MemoryEngine
    import tempfile
    
    print_header("🧠 Demo: Basic Memory Operations")
    
    # Create temporary database
    with tempfile.NamedTemporaryFile(delete=False, suffix='.db') as f:
        temp_db = f.name
    
    try:
        print("\n1️⃣  Creating Memory Engine...")
        engine = MemoryEngine(db_path=temp_db)
        print("   ✅ Memory engine created!")
        
        print("\n2️⃣  Saving some memories...")
        memories_to_save = [
            ("user", "My name is Alice and I love Python programming"),
            ("assistant", "Nice to meet you, Alice! Python is great!"),
            ("user", "I work as a software engineer at a tech company"),
            ("assistant", "That's an exciting field!"),
            ("user", "My favorite color is blue"),
        ]
        
        for role, content in memories_to_save:
            try:
                msg_id = engine.save_message(
                    role=role,
                    content=content,
                    conversation_id="demo",
                    generate_embedding=True  # Will use real embeddings if API key is set
                )
                print(f"   ✅ Saved: {content[:50]}... (ID: {msg_id})")
            except Exception as e:
                print(f"   ⚠️  Skipped embedding generation: {str(e)[:50]}")
                # Save without embedding
                msg_id = engine.save_message(
                    role=role,
                    content=content,
                    conversation_id="demo",
                    generate_embedding=False
                )
                print(f"   ✅ Saved (no embedding): {content[:50]}...")
        
        print("\n3️⃣  Getting conversation history...")
        history = engine.get_conversation_history("demo")
        print(f"   ✅ Found {len(history)} messages")
        for i, msg in enumerate(history[:3], 1):
            print(f"   [{i}] {msg['role']}: {msg['content'][:40]}...")
        
        print("\n4️⃣  Getting statistics...")
        stats = engine.get_statistics()
        print(f"   Total messages: {stats['total_messages']}")
        print(f"   Total conversations: {stats['total_conversations']}")
        print(f"   Total embeddings: {stats['total_embeddings']}")
        
        if stats['total_embeddings'] > 0:
            print("\n5️⃣  Testing semantic search...")
            try:
                memories = engine.retrieve_memories(
                    query="What's my name?",
                    top_k=2,
                    conversation_id="demo"
                )
                print(f"   ✅ Found {len(memories)} relevant memories:")
                for i, mem in enumerate(memories, 1):
                    print(f"   [{i}] Similarity: {mem['similarity']:.3f}")
                    print(f"       {mem['content'][:60]}...")
            except Exception as e:
                print(f"   ⚠️  Search error: {str(e)[:50]}")
        else:
            print("\n5️⃣  Skipping semantic search (no embeddings)")
        
        print("\n✅ Demo completed successfully!")
        engine.close()
        
    finally:
        # Cleanup
        if os.path.exists(temp_db):
            os.unlink(temp_db)


def demo_chatbot_info():
    """Show chatbot information."""
    print_header("💬 Interactive Chatbot")
    
    print("\nTo start the interactive chatbot, run:")
    print("\n  python -m mini_memori.chatbot")
    print("\nAvailable commands:")
    print("  /help     - Show help message")
    print("  /stats    - Show memory statistics")
    print("  /history  - Show conversation history")
    print("  /search   - Search memories")
    print("  /clear    - Clear current conversation")
    print("  /quit     - Exit chatbot")


def demo_code_example():
    """Show a code example."""
    print_header("📝 Code Example")
    
    example = '''
from mini_memori import MemoryEngine

# Initialize
engine = MemoryEngine()

# Save a message
engine.save_message(
    role="user",
    content="I love machine learning",
    conversation_id="tech_talk"
)

# Retrieve relevant memories
memories = engine.retrieve_memories(
    query="What are my interests?",
    top_k=5
)

# Process results
for memory in memories:
    print(f"{memory['content']} (score: {memory['similarity']:.3f})")
'''
    
    print(example)


def main():
    """Main demo function."""
    print("\n" + "="*60)
    print("  🧠 Welcome to Mini Memori Demo!")
    print("="*60)
    
    print("\nThis demo will show you how Mini Memori works.")
    
    # Check API key
    has_api_key = check_api_key()
    
    try:
        # Run basic demo
        demo_basic_operations()
        
        # Show chatbot info
        demo_chatbot_info()
        
        # Show code example
        demo_code_example()
        
        # Final message
        print_header("🎉 Next Steps")
        print("\n1. Explore the examples:")
        print("   python examples/basic_usage.py")
        print("   python examples/chatbot_demo.py")
        
        print("\n2. Read the documentation:")
        print("   - README.md")
        print("   - QUICKSTART.md")
        print("   - USAGE_GUIDE.md")
        
        print("\n3. Start building your own memory-enhanced apps!")
        
        if not has_api_key:
            print("\n⚠️  Remember to set your OPENAI_API_KEY for full functionality!")
        
        print("\n" + "="*60)
        print("  Thanks for trying Mini Memori! 🚀")
        print("="*60 + "\n")
        
    except ImportError as e:
        print("\n❌ Error: Mini Memori not installed properly")
        print(f"   {str(e)}")
        print("\nPlease run: pip install -e .")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\nPlease check the documentation or report this issue.")
        sys.exit(1)


if __name__ == "__main__":
    main()
