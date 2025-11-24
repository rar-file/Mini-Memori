"""
Database module for Mini Memori.

Handles SQLite database operations including schema creation,
message storage, and retrieval operations.
"""

import sqlite3
import json
from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class Database:
    """
    Manages SQLite database operations for the memory engine.
    
    This class handles all database interactions including:
    - Schema creation and migrations
    - Message CRUD operations
    - Embedding storage and retrieval
    - Conversation management
    """
    
    def __init__(self, db_path: str = "memories.db"):
        """
        Initialize the database connection.
        
        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = db_path
        self.conn = None
        self._connect()
        self._create_schema()
        
    def _connect(self) -> None:
        """Establish database connection with optimized settings."""
        try:
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.conn.row_factory = sqlite3.Row
            # Enable WAL mode for better concurrency
            self.conn.execute("PRAGMA journal_mode=WAL")
            logger.info(f"Connected to database: {self.db_path}")
        except sqlite3.Error as e:
            logger.error(f"Database connection error: {e}")
            raise
            
    def _create_schema(self) -> None:
        """Create database schema if it doesn't exist."""
        try:
            cursor = self.conn.cursor()
            
            # Messages table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    conversation_id TEXT NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    metadata TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Embeddings table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS embeddings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    message_id INTEGER NOT NULL,
                    embedding BLOB NOT NULL,
                    model TEXT NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (message_id) REFERENCES messages (id) ON DELETE CASCADE
                )
            """)
            
            # Conversations table for metadata
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id TEXT PRIMARY KEY,
                    title TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    metadata TEXT
                )
            """)
            
            # Create indexes for better performance
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_messages_conversation 
                ON messages(conversation_id, timestamp)
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_embeddings_message 
                ON embeddings(message_id)
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_messages_timestamp 
                ON messages(timestamp)
            """)
            
            self.conn.commit()
            logger.info("Database schema created successfully")
            
        except sqlite3.Error as e:
            logger.error(f"Schema creation error: {e}")
            raise
            
    def save_message(
        self,
        conversation_id: str,
        role: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> int:
        """
        Save a message to the database.
        
        Args:
            conversation_id: Unique conversation identifier
            role: Message role (user, assistant, system)
            content: Message content
            metadata: Optional metadata dictionary
            
        Returns:
            Message ID
        """
        try:
            cursor = self.conn.cursor()
            
            # Ensure conversation exists
            cursor.execute("""
                INSERT OR IGNORE INTO conversations (id, updated_at) 
                VALUES (?, CURRENT_TIMESTAMP)
            """, (conversation_id,))
            
            # Update conversation timestamp
            cursor.execute("""
                UPDATE conversations 
                SET updated_at = CURRENT_TIMESTAMP 
                WHERE id = ?
            """, (conversation_id,))
            
            # Insert message
            metadata_json = json.dumps(metadata) if metadata else None
            cursor.execute("""
                INSERT INTO messages (conversation_id, role, content, metadata)
                VALUES (?, ?, ?, ?)
            """, (conversation_id, role, content, metadata_json))
            
            message_id = cursor.lastrowid
            self.conn.commit()
            
            logger.debug(f"Saved message {message_id} to conversation {conversation_id}")
            return message_id
            
        except sqlite3.Error as e:
            logger.error(f"Error saving message: {e}")
            self.conn.rollback()
            raise
            
    def save_embedding(
        self,
        message_id: int,
        embedding: List[float],
        model: str
    ) -> int:
        """
        Save an embedding vector for a message.
        
        Args:
            message_id: ID of the associated message
            embedding: Embedding vector as list of floats
            model: Name of the embedding model used
            
        Returns:
            Embedding ID
        """
        try:
            cursor = self.conn.cursor()
            
            # Convert embedding to bytes for storage
            embedding_bytes = json.dumps(embedding).encode('utf-8')
            
            cursor.execute("""
                INSERT INTO embeddings (message_id, embedding, model)
                VALUES (?, ?, ?)
            """, (message_id, embedding_bytes, model))
            
            embedding_id = cursor.lastrowid
            self.conn.commit()
            
            logger.debug(f"Saved embedding {embedding_id} for message {message_id}")
            return embedding_id
            
        except sqlite3.Error as e:
            logger.error(f"Error saving embedding: {e}")
            self.conn.rollback()
            raise
            
    def get_all_embeddings(self) -> List[Tuple[int, List[float], Dict[str, Any]]]:
        """
        Retrieve all embeddings with their associated message data.
        
        Returns:
            List of tuples: (message_id, embedding_vector, message_dict)
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT 
                    m.id,
                    m.conversation_id,
                    m.role,
                    m.content,
                    m.timestamp,
                    m.metadata,
                    e.embedding,
                    e.model
                FROM messages m
                JOIN embeddings e ON m.id = e.message_id
                ORDER BY m.timestamp DESC
            """)
            
            results = []
            for row in cursor.fetchall():
                embedding = json.loads(row['embedding'].decode('utf-8'))
                message_dict = {
                    'id': row['id'],
                    'conversation_id': row['conversation_id'],
                    'role': row['role'],
                    'content': row['content'],
                    'timestamp': row['timestamp'],
                    'metadata': json.loads(row['metadata']) if row['metadata'] else None,
                    'embedding_model': row['model']
                }
                results.append((row['id'], embedding, message_dict))
                
            logger.debug(f"Retrieved {len(results)} embeddings")
            return results
            
        except sqlite3.Error as e:
            logger.error(f"Error retrieving embeddings: {e}")
            raise
            
    def get_conversation_history(
        self,
        conversation_id: str,
        limit: Optional[int] = 50
    ) -> List[Dict[str, Any]]:
        """
        Get message history for a conversation.
        
        Args:
            conversation_id: Conversation identifier
            limit: Maximum number of messages to return
            
        Returns:
            List of message dictionaries
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT 
                    id,
                    conversation_id,
                    role,
                    content,
                    timestamp,
                    metadata
                FROM messages
                WHERE conversation_id = ?
                ORDER BY timestamp ASC
                LIMIT ?
            """, (conversation_id, limit))
            
            messages = []
            for row in cursor.fetchall():
                messages.append({
                    'id': row['id'],
                    'conversation_id': row['conversation_id'],
                    'role': row['role'],
                    'content': row['content'],
                    'timestamp': row['timestamp'],
                    'metadata': json.loads(row['metadata']) if row['metadata'] else None
                })
                
            logger.debug(f"Retrieved {len(messages)} messages from conversation {conversation_id}")
            return messages
            
        except sqlite3.Error as e:
            logger.error(f"Error retrieving conversation history: {e}")
            raise
            
    def delete_conversation(self, conversation_id: str) -> int:
        """
        Delete all messages from a conversation.
        
        Args:
            conversation_id: Conversation identifier
            
        Returns:
            Number of messages deleted
        """
        try:
            cursor = self.conn.cursor()
            
            # Delete messages (embeddings will cascade)
            cursor.execute("""
                DELETE FROM messages WHERE conversation_id = ?
            """, (conversation_id,))
            
            deleted_count = cursor.rowcount
            
            # Delete conversation metadata
            cursor.execute("""
                DELETE FROM conversations WHERE id = ?
            """, (conversation_id,))
            
            self.conn.commit()
            
            logger.info(f"Deleted {deleted_count} messages from conversation {conversation_id}")
            return deleted_count
            
        except sqlite3.Error as e:
            logger.error(f"Error deleting conversation: {e}")
            self.conn.rollback()
            raise
            
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get database statistics.
        
        Returns:
            Dictionary with statistics
        """
        try:
            cursor = self.conn.cursor()
            
            # Total messages
            cursor.execute("SELECT COUNT(*) as count FROM messages")
            total_messages = cursor.fetchone()['count']
            
            # Total conversations
            cursor.execute("SELECT COUNT(DISTINCT conversation_id) as count FROM messages")
            total_conversations = cursor.fetchone()['count']
            
            # Total embeddings
            cursor.execute("SELECT COUNT(*) as count FROM embeddings")
            total_embeddings = cursor.fetchone()['count']
            
            # Date range
            cursor.execute("""
                SELECT 
                    MIN(timestamp) as first_message,
                    MAX(timestamp) as last_message
                FROM messages
            """)
            date_range = cursor.fetchone()
            
            stats = {
                'total_messages': total_messages,
                'total_conversations': total_conversations,
                'total_embeddings': total_embeddings,
                'first_message': date_range['first_message'],
                'last_message': date_range['last_message']
            }
            
            logger.debug(f"Database statistics: {stats}")
            return stats
            
        except sqlite3.Error as e:
            logger.error(f"Error getting statistics: {e}")
            raise
            
    def close(self) -> None:
        """Close the database connection."""
        if self.conn:
            self.conn.close()
            logger.info("Database connection closed")
            
    def __enter__(self):
        """Context manager entry."""
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
