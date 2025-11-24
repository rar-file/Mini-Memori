"""
Interactive chatbot interface for Mini Memori.

CLI chatbot that uses the memory engine for long-term memory.
"""

import sys
import openai
from typing import List, Dict, Any, Optional
import logging
from datetime import datetime
from .engine import MemoryEngine
from .config import get_config, setup_logging
from .utils import format_memory_output

logger = logging.getLogger(__name__)


class MemoriChatbot:
    """
    Interactive chatbot with long-term memory capabilities.
    
    Features:
    - Remembers conversation history
    - Retrieves relevant context from past conversations
    - Integrates with OpenAI's chat models
    - Persistent memory across sessions
    """
    
    def __init__(
        self,
        memory_engine: Optional[MemoryEngine] = None,
        conversation_id: Optional[str] = None,
        chat_model: str = "gpt-4o-mini",
        memory_top_k: int = 3
    ):
        """
        Initialize the chatbot.
        
        Args:
            memory_engine: MemoryEngine instance (creates new if None)
            conversation_id: Conversation identifier (generates if None)
            chat_model: OpenAI chat model to use
            memory_top_k: Number of memories to retrieve for context
        """
        # Initialize or use provided memory engine
        self.memory = memory_engine or MemoryEngine()
        
        # Set up conversation
        self.conversation_id = conversation_id or f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.chat_model = chat_model
        self.memory_top_k = memory_top_k
        
        # Get API key from config
        config = get_config()
        openai.api_key = config.openai_api_key
        
        logger.info(
            f"Chatbot initialized (conversation: {self.conversation_id}, "
            f"model: {self.chat_model})"
        )
        
    def get_system_prompt(self) -> str:
        """
        Get the system prompt for the chatbot.
        
        Returns:
            System prompt string
        """
        return (
            "You are a helpful AI assistant with long-term memory. "
            "You have access to relevant memories from previous conversations. "
            "Use these memories to provide personalized and contextually aware responses. "
            "If you reference information from memories, acknowledge it naturally."
        )
        
    def retrieve_relevant_context(self, user_message: str) -> List[Dict[str, Any]]:
        """
        Retrieve relevant memories for context.
        
        Args:
            user_message: User's current message
            
        Returns:
            List of relevant memories
        """
        try:
            memories = self.memory.retrieve_memories(
                query=user_message,
                top_k=self.memory_top_k,
                threshold=0.7  # Only include fairly relevant memories
            )
            
            logger.debug(f"Retrieved {len(memories)} relevant memories")
            return memories
            
        except Exception as e:
            logger.error(f"Error retrieving context: {e}")
            return []
            
    def format_context_for_prompt(self, memories: List[Dict[str, Any]]) -> str:
        """
        Format memories into a context string for the prompt.
        
        Args:
            memories: List of memory dictionaries
            
        Returns:
            Formatted context string
        """
        if not memories:
            return ""
            
        context_parts = ["Relevant memories from previous conversations:"]
        
        for i, memory in enumerate(memories, 1):
            role = memory['role']
            content = memory['content']
            context_parts.append(f"{i}. [{role}]: {content}")
            
        return "\n".join(context_parts)
        
    def chat(self, user_message: str, use_memory: bool = True) -> str:
        """
        Send a message and get a response.
        
        Args:
            user_message: User's message
            use_memory: Whether to use memory for context
            
        Returns:
            Assistant's response
        """
        try:
            # Save user message
            self.memory.save_message(
                role="user",
                content=user_message,
                conversation_id=self.conversation_id
            )
            
            # Build messages for API
            messages = [
                {"role": "system", "content": self.get_system_prompt()}
            ]
            
            # Add relevant context from memory
            if use_memory:
                relevant_memories = self.retrieve_relevant_context(user_message)
                if relevant_memories:
                    context = self.format_context_for_prompt(relevant_memories)
                    messages.append({
                        "role": "system",
                        "content": context
                    })
                    
            # Add recent conversation history
            recent_history = self.memory.get_conversation_history(
                conversation_id=self.conversation_id,
                limit=10
            )
            
            # Add recent messages (excluding the one we just saved)
            for msg in recent_history[:-1]:
                messages.append({
                    "role": msg['role'],
                    "content": msg['content']
                })
                
            # Add current user message
            messages.append({
                "role": "user",
                "content": user_message
            })
            
            # Call OpenAI API
            response = openai.chat.completions.create(
                model=self.chat_model,
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )
            
            assistant_message = response.choices[0].message.content
            
            # Save assistant response
            self.memory.save_message(
                role="assistant",
                content=assistant_message,
                conversation_id=self.conversation_id
            )
            
            return assistant_message
            
        except Exception as e:
            logger.error(f"Error in chat: {e}")
            return f"Sorry, I encountered an error: {str(e)}"
            
    def show_statistics(self) -> None:
        """Display memory statistics."""
        stats = self.memory.get_statistics()
        print("\n📊 Memory Statistics:")
        print(f"  Total messages: {stats['total_messages']}")
        print(f"  Total conversations: {stats['total_conversations']}")
        print(f"  Total embeddings: {stats['total_embeddings']}")
        if stats['first_message']:
            print(f"  First message: {stats['first_message']}")
        if stats['last_message']:
            print(f"  Last message: {stats['last_message']}")
        print()
        
    def show_recent_history(self, limit: int = 5) -> None:
        """Display recent conversation history."""
        messages = self.memory.get_conversation_history(
            conversation_id=self.conversation_id,
            limit=limit
        )
        
        print(f"\n💬 Recent History (last {len(messages)} messages):")
        for msg in messages:
            role_emoji = "👤" if msg['role'] == "user" else "🤖"
            print(f"{role_emoji} {msg['role'].upper()}: {msg['content'][:100]}...")
        print()
        
    def search_memories(self, query: str) -> None:
        """Search and display memories."""
        print(f"\n🔍 Searching for: '{query}'")
        memories = self.memory.retrieve_memories(query, top_k=5, threshold=0.5)
        
        if memories:
            print(format_memory_output(memories, max_content_length=150))
        else:
            print("No relevant memories found.")
        print()


def run_interactive_chat():
    """Run the interactive chatbot CLI."""
    # Set up logging
    setup_logging()
    
    # Print welcome message
    print("\n" + "="*60)
    print("🧠 Mini Memori - Chatbot with Long-Term Memory")
    print("="*60)
    print("\nCommands:")
    print("  /help     - Show this help message")
    print("  /stats    - Show memory statistics")
    print("  /history  - Show recent conversation history")
    print("  /search   - Search memories (e.g., /search favorite color)")
    print("  /clear    - Clear current conversation")
    print("  /quit     - Exit the chatbot")
    print("\n" + "-"*60 + "\n")
    
    try:
        # Initialize chatbot
        chatbot = MemoriChatbot()
        print(f"✅ Connected to conversation: {chatbot.conversation_id}\n")
        
        # Main chat loop
        while True:
            try:
                # Get user input
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                    
                # Handle commands
                if user_input.startswith("/"):
                    command_parts = user_input.split(maxsplit=1)
                    command = command_parts[0].lower()
                    
                    if command == "/quit":
                        print("\n👋 Goodbye! Your memories have been saved.")
                        break
                        
                    elif command == "/help":
                        print("\nCommands:")
                        print("  /help     - Show this help message")
                        print("  /stats    - Show memory statistics")
                        print("  /history  - Show recent conversation history")
                        print("  /search   - Search memories")
                        print("  /clear    - Clear current conversation")
                        print("  /quit     - Exit the chatbot")
                        print()
                        
                    elif command == "/stats":
                        chatbot.show_statistics()
                        
                    elif command == "/history":
                        chatbot.show_recent_history()
                        
                    elif command == "/search":
                        if len(command_parts) > 1:
                            query = command_parts[1]
                            chatbot.search_memories(query)
                        else:
                            print("Usage: /search <query>")
                            
                    elif command == "/clear":
                        count = chatbot.memory.clear_conversation(chatbot.conversation_id)
                        print(f"\n🗑️  Cleared {count} messages from current conversation.\n")
                        
                    else:
                        print(f"Unknown command: {command}")
                        print("Type /help for available commands.\n")
                        
                    continue
                    
                # Regular chat message
                response = chatbot.chat(user_input)
                print(f"\nAssistant: {response}\n")
                
            except KeyboardInterrupt:
                print("\n\n👋 Interrupted. Goodbye!")
                break
                
            except Exception as e:
                logger.error(f"Error in chat loop: {e}")
                print(f"\n❌ Error: {str(e)}\n")
                
    except Exception as e:
        logger.error(f"Failed to initialize chatbot: {e}")
        print(f"\n❌ Failed to start chatbot: {str(e)}")
        print("\nMake sure you have:")
        print("  1. Set OPENAI_API_KEY environment variable")
        print("  2. Installed required packages: pip install -r requirements.txt")
        sys.exit(1)
        
    finally:
        print("\n" + "="*60)


def main():
    """Main entry point for the chatbot."""
    run_interactive_chat()


if __name__ == "__main__":
    main()
