"""
Unit tests for Mini Memori database module.
"""

import unittest
import os
import tempfile
from mini_memori.database import Database


class TestDatabase(unittest.TestCase):
    """Test cases for Database class."""
    
    def setUp(self):
        """Set up test database before each test."""
        # Create temporary database
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.db = Database(self.temp_db.name)
        
    def tearDown(self):
        """Clean up after each test."""
        self.db.close()
        if os.path.exists(self.temp_db.name):
            os.unlink(self.temp_db.name)
            
    def test_schema_creation(self):
        """Test that database schema is created correctly."""
        cursor = self.db.conn.cursor()
        
        # Check messages table exists
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='messages'
        """)
        self.assertIsNotNone(cursor.fetchone())
        
        # Check embeddings table exists
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='embeddings'
        """)
        self.assertIsNotNone(cursor.fetchone())
        
        # Check conversations table exists
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='conversations'
        """)
        self.assertIsNotNone(cursor.fetchone())
        
    def test_save_message(self):
        """Test saving a message."""
        message_id = self.db.save_message(
            conversation_id="test_conv",
            role="user",
            content="Test message"
        )
        
        self.assertIsInstance(message_id, int)
        self.assertGreater(message_id, 0)
        
    def test_save_message_with_metadata(self):
        """Test saving a message with metadata."""
        metadata = {"key": "value", "number": 42}
        message_id = self.db.save_message(
            conversation_id="test_conv",
            role="user",
            content="Test message",
            metadata=metadata
        )
        
        # Retrieve and verify
        history = self.db.get_conversation_history("test_conv")
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]['metadata'], metadata)
        
    def test_save_embedding(self):
        """Test saving an embedding."""
        # First save a message
        message_id = self.db.save_message(
            conversation_id="test_conv",
            role="user",
            content="Test message"
        )
        
        # Save embedding
        embedding = [0.1, 0.2, 0.3, 0.4, 0.5]
        embedding_id = self.db.save_embedding(
            message_id=message_id,
            embedding=embedding,
            model="test-model"
        )
        
        self.assertIsInstance(embedding_id, int)
        self.assertGreater(embedding_id, 0)
        
    def test_get_all_embeddings(self):
        """Test retrieving all embeddings."""
        # Save messages with embeddings
        for i in range(3):
            message_id = self.db.save_message(
                conversation_id="test_conv",
                role="user",
                content=f"Message {i}"
            )
            self.db.save_embedding(
                message_id=message_id,
                embedding=[float(i)] * 5,
                model="test-model"
            )
            
        # Retrieve all
        embeddings = self.db.get_all_embeddings()
        self.assertEqual(len(embeddings), 3)
        
        # Check structure
        msg_id, embedding_vec, data = embeddings[0]
        self.assertIsInstance(msg_id, int)
        self.assertIsInstance(embedding_vec, list)
        self.assertIsInstance(data, dict)
        
    def test_get_conversation_history(self):
        """Test retrieving conversation history."""
        # Save multiple messages
        messages = ["Message 1", "Message 2", "Message 3"]
        for msg in messages:
            self.db.save_message(
                conversation_id="test_conv",
                role="user",
                content=msg
            )
            
        # Retrieve history
        history = self.db.get_conversation_history("test_conv")
        self.assertEqual(len(history), 3)
        
        # Verify order (chronological)
        for i, msg_dict in enumerate(history):
            self.assertEqual(msg_dict['content'], messages[i])
            
    def test_get_conversation_history_with_limit(self):
        """Test conversation history with limit."""
        # Save 10 messages
        for i in range(10):
            self.db.save_message(
                conversation_id="test_conv",
                role="user",
                content=f"Message {i}"
            )
            
        # Retrieve with limit
        history = self.db.get_conversation_history("test_conv", limit=5)
        self.assertEqual(len(history), 5)
        
    def test_delete_conversation(self):
        """Test deleting a conversation."""
        # Save messages
        for i in range(3):
            self.db.save_message(
                conversation_id="test_conv",
                role="user",
                content=f"Message {i}"
            )
            
        # Delete conversation
        deleted_count = self.db.delete_conversation("test_conv")
        self.assertEqual(deleted_count, 3)
        
        # Verify deletion
        history = self.db.get_conversation_history("test_conv")
        self.assertEqual(len(history), 0)
        
    def test_get_statistics(self):
        """Test getting database statistics."""
        # Add some data
        for i in range(5):
            message_id = self.db.save_message(
                conversation_id=f"conv_{i % 2}",
                role="user",
                content=f"Message {i}"
            )
            self.db.save_embedding(
                message_id=message_id,
                embedding=[float(i)] * 5,
                model="test-model"
            )
            
        # Get statistics
        stats = self.db.get_statistics()
        
        self.assertEqual(stats['total_messages'], 5)
        self.assertEqual(stats['total_conversations'], 2)
        self.assertEqual(stats['total_embeddings'], 5)
        self.assertIsNotNone(stats['first_message'])
        self.assertIsNotNone(stats['last_message'])
        
    def test_context_manager(self):
        """Test using database as context manager."""
        with Database(self.temp_db.name) as db:
            message_id = db.save_message(
                conversation_id="test_conv",
                role="user",
                content="Test message"
            )
            self.assertGreater(message_id, 0)
            
        # Database should be closed
        # Note: can't easily test this without accessing private attributes


if __name__ == '__main__':
    unittest.main()
