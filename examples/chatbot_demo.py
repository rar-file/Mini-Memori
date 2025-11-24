"""
Custom chatbot implementation example.

Shows how to build your own chatbot using the memory engine.
"""

from mini_memori import MemoryEngine
from mini_memori.chatbot import MemoriChatbot
from mini_memori.config import setup_logging

setup_logging("INFO")


def main():
    print("\n" + "="*60)
    print("🤖 Custom Chatbot Demo")
    print("="*60)
    
    # Create a memory engine
    engine = MemoryEngine(db_path="demo_chatbot.db")
    
    # Create a chatbot with custom settings
    chatbot = MemoriChatbot(
        memory_engine=engine,
        conversation_id="demo_session",
        chat_model="gpt-4o-mini",
        memory_top_k=5  # Retrieve more context
    )
    
    print("\nThis demo shows how to use the chatbot programmatically.\n")
    
    # Example conversation
    test_messages = [
        "Hi! My name is Bob and I'm a software engineer.",
        "I specialize in backend development with Python and Go.",
        "What's my name and what do I do?",
    ]
    
    for user_message in test_messages:
        print(f"\n👤 User: {user_message}")
        
        # Get response from chatbot
        response = chatbot.chat(user_message)
        
        print(f"🤖 Assistant: {response}")
    
    # Show statistics
    print("\n" + "-"*60)
    chatbot.show_statistics()
    
    print("✅ Demo completed!")
    print(f"💾 Conversation saved to database: {engine.db_path}\n")
    
    engine.close()


if __name__ == "__main__":
    main()
