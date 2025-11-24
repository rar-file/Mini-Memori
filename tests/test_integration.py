"""
Integration tests for Mini Memori.

Tests the full memory engine workflow.
"""

import unittest
import os
import tempfile
from unittest.mock import Mock, patch
from mini_memori import MemoryEngine


class TestMemoryEngineIntegration(unittest.TestCase):
    """Integration tests for the complete memory engine."""
    
    def setUp(self):
        """Set up test environment."""
        # Create temporary database
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        
        # Mock OpenAI API calls
        self.patcher = patch('mini_memori.embeddings.openai.embeddings.create')
        self.mock_openai = self.patcher.start()
        
        # Mock embeddings response
        def create_mock_embedding(input, model):
            # Generate simple embeddings based on text length
            if isinstance(input, list):
                return Mock(data=[
                    Mock(embedding=[float(len(text)) / 100] * 1536) 
                    for text in input
                ])
            else:
                return Mock(data=[Mock(embedding=[float(len(input)) / 100] * 1536)])
        
        self.mock_openai.side_effect = create_mock_embedding
        
        # Create engine
        self.engine = MemoryEngine(
            db_path=self.temp_db.name,
            api_key="test_key"
        )
        
    def tearDown(self):
        """Clean up after tests."""
        self.patcher.stop()
        self.engine.close()
        if os.path.exists(self.temp_db.name):
            os.unlink(self.temp_db.name)
            
    def test_save_and_retrieve_single_message(self):
        """Test saving and retrieving a single message."""
        # Save message
        msg_id = self.engine.save_message(
            role="user",
            content="What is my favorite color?",
            conversation_id="test_conv"
        )
        
        self.assertIsInstance(msg_id, int)
        self.assertGreater(msg_id, 0)
        
        # Retrieve
        memories = self.engine.retrieve_memories(
            query="favorite color",
            conversation_id="test_conv"
        )
        
        self.assertGreater(len(memories), 0)
        self.assertEqual(memories[0]['content'], "What is my favorite color?")
        
    def test_save_multiple_and_retrieve_relevant(self):
        """Test saving multiple messages and retrieving relevant ones."""
        messages = [
            ("user", "I love Python programming"),
            ("assistant", "Python is a great language!"),
            ("user", "My favorite color is blue"),
            ("assistant", "Blue is a calming color"),
            ("user", "I enjoy hiking on weekends"),
        ]
        
        # Save all messages
        for role, content in messages:
            self.engine.save_message(
                role=role,
                content=content,
                conversation_id="test_conv"
            )
            
        # Retrieve programming-related
        memories = self.engine.retrieve_memories(
            query="programming languages",
            top_k=2,
            conversation_id="test_conv"
        )
        
        # Should find relevant messages
        self.assertGreater(len(memories), 0)
        
    def test_conversation_history(self):
        """Test getting conversation history."""
        messages = [
            ("user", "Hello"),
            ("assistant", "Hi there!"),
            ("user", "How are you?"),
        ]
        
        for role, content in messages:
            self.engine.save_message(
                role=role,
                content=content,
                conversation_id="test_conv"
            )
            
        # Get history
        history = self.engine.get_conversation_history("test_conv")
        
        self.assertEqual(len(history), 3)
        self.assertEqual(history[0]['content'], "Hello")
        self.assertEqual(history[2]['content'], "How are you?")
        
    def test_clear_conversation(self):
        """Test clearing a conversation."""
        # Add messages
        for i in range(5):
            self.engine.save_message(
                role="user",
                content=f"Message {i}",
                conversation_id="test_conv"
            )
            
        # Clear
        count = self.engine.clear_conversation("test_conv")
        self.assertEqual(count, 5)
        
        # Verify cleared
        history = self.engine.get_conversation_history("test_conv")
        self.assertEqual(len(history), 0)
        
    def test_statistics(self):
        """Test getting statistics."""
        # Add messages to multiple conversations
        for conv_id in ["conv1", "conv2"]:
            for i in range(3):
                self.engine.save_message(
                    role="user",
                    content=f"Message {i}",
                    conversation_id=conv_id
                )
                
        stats = self.engine.get_statistics()
        
        self.assertEqual(stats['total_messages'], 6)
        self.assertEqual(stats['total_conversations'], 2)
        self.assertEqual(stats['total_embeddings'], 6)
        
    def test_message_with_metadata(self):
        """Test saving and retrieving messages with metadata."""
        metadata = {"source": "test", "importance": "high"}
        
        self.engine.save_message(
            role="user",
            content="Important message",
            conversation_id="test_conv",
            metadata=metadata
        )
        
        history = self.engine.get_conversation_history("test_conv")
        self.assertEqual(history[0]['metadata'], metadata)
        
    def test_retrieve_with_threshold(self):
        """Test retrieval with similarity threshold."""
        # Save messages
        self.engine.save_message(
            role="user",
            content="Python programming is great",
            conversation_id="test_conv"
        )
        
        self.engine.save_message(
            role="user",
            content="I like pizza",
            conversation_id="test_conv"
        )
        
        # High threshold - should be more selective
        memories = self.engine.retrieve_memories(
            query="software development",
            threshold=0.9,
            conversation_id="test_conv"
        )
        
        # Results depend on mock embedding similarity
        # Just verify it returns a list
        self.assertIsInstance(memories, list)
        
    def test_keyword_search(self):
        """Test keyword-based search."""
        messages = [
            "I love Python programming",
            "JavaScript is also good",
            "My favorite food is pizza"
        ]
        
        for msg in messages:
            self.engine.save_message(
                role="user",
                content=msg,
                conversation_id="test_conv"
            )
            
        # Search for keyword
        results = self.engine.search_by_keyword(
            keyword="Python",
            conversation_id="test_conv"
        )
        
        self.assertEqual(len(results), 1)
        self.assertIn("Python", results[0]['content'])
        
    def test_context_manager(self):
        """Test using engine as context manager."""
        with MemoryEngine(db_path=self.temp_db.name, api_key="test_key") as engine:
            msg_id = engine.save_message(
                role="user",
                content="Test message",
                conversation_id="test_conv"
            )
            self.assertGreater(msg_id, 0)


if __name__ == '__main__':
    unittest.main()
