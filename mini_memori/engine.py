"""
Core Memory Engine for Mini Memori.

Main interface for saving and retrieving memories with embeddings.
"""

from typing import List, Optional, Dict, Any
import logging
from .database import Database
from .embeddings import EmbeddingService
from .config import get_config
from .utils import validate_message_data, sanitize_conversation_id

logger = logging.getLogger(__name__)


class MemoryEngine:
    """
    Main memory engine that orchestrates storage and retrieval of memories.
    
    This class provides a high-level API for:
    - Saving messages with automatic embedding generation
    - Retrieving relevant memories using semantic search
    - Managing conversation history
    - Getting database statistics
    """
    
    def __init__(
        self,
        db_path: Optional[str] = None,
        embedding_model: Optional[str] = None,
        api_key: Optional[str] = None
    ):
        """
        Initialize the Memory Engine.
        
        Args:
            db_path: Path to SQLite database (uses config default if None)
            embedding_model: OpenAI embedding model (uses config default if None)
            api_key: OpenAI API key (uses config/env if None)
        """
        # Load configuration
        config = get_config()
        
        # Initialize database
        self.db_path = db_path or config.db_path
        self.db = Database(self.db_path)
        
        # Initialize embedding service
        self.embedding_model = embedding_model or config.embedding_model
        self.api_key = api_key or config.openai_api_key
        
        if not self.api_key:
            raise ValueError(
                "OpenAI API key is required. Set OPENAI_API_KEY environment variable "
                "or pass api_key parameter."
            )
            
        self.embeddings = EmbeddingService(
            api_key=self.api_key,
            model=self.embedding_model
        )
        
        logger.info(
            f"MemoryEngine initialized (db: {self.db_path}, "
            f"model: {self.embedding_model})"
        )
        
    def save_message(
        self,
        role: str,
        content: str,
        conversation_id: str = "default",
        metadata: Optional[Dict[str, Any]] = None,
        generate_embedding: bool = True
    ) -> int:
        """
        Save a message to the database with its embedding.
        
        Args:
            role: Message role (user, assistant, system)
            content: Message content
            conversation_id: Conversation identifier
            metadata: Optional metadata dictionary
            generate_embedding: Whether to generate and store embedding
            
        Returns:
            Message ID
            
        Raises:
            ValueError: If message data is invalid
            Exception: If save operation fails
        """
        try:
            # Validate input
            is_valid, error_msg = validate_message_data(role, content, conversation_id)
            if not is_valid:
                raise ValueError(error_msg)
                
            # Sanitize conversation ID
            safe_conv_id = sanitize_conversation_id(conversation_id)
            
            # Save message to database
            message_id = self.db.save_message(
                conversation_id=safe_conv_id,
                role=role,
                content=content,
                metadata=metadata
            )
            
            # Generate and save embedding
            if generate_embedding:
                try:
                    embedding = self.embeddings.generate_embedding(content)
                    self.db.save_embedding(
                        message_id=message_id,
                        embedding=embedding,
                        model=self.embedding_model
                    )
                    logger.debug(f"Generated embedding for message {message_id}")
                except Exception as e:
                    logger.error(f"Failed to generate embedding: {e}")
                    # Continue even if embedding fails
                    
            logger.info(f"Saved message {message_id} to conversation {safe_conv_id}")
            return message_id
            
        except Exception as e:
            logger.error(f"Error saving message: {e}")
            raise
            
    def retrieve_memories(
        self,
        query: str,
        top_k: int = 5,
        conversation_id: Optional[str] = None,
        threshold: float = 0.0
    ) -> List[Dict[str, Any]]:
        """
        Retrieve the most relevant memories based on a query.
        
        Args:
            query: Search query text
            top_k: Number of results to return
            conversation_id: Optional filter by conversation
            threshold: Minimum similarity threshold (0-1)
            
        Returns:
            List of memory dictionaries with similarity scores
        """
        try:
            # Generate query embedding
            logger.debug(f"Retrieving memories for query: {query[:50]}...")
            query_embedding = self.embeddings.generate_embedding(query)
            
            # Get all embeddings from database
            all_embeddings = self.db.get_all_embeddings()
            
            if not all_embeddings:
                logger.warning("No embeddings found in database")
                return []
                
            # Filter by conversation if specified
            if conversation_id:
                safe_conv_id = sanitize_conversation_id(conversation_id)
                all_embeddings = [
                    (msg_id, emb, data) for msg_id, emb, data in all_embeddings
                    if data['conversation_id'] == safe_conv_id
                ]
                logger.debug(f"Filtered to {len(all_embeddings)} embeddings from conversation")
                
            # Find most similar
            similar_items = self.embeddings.find_most_similar(
                query_embedding=query_embedding,
                embeddings=all_embeddings,
                top_k=top_k,
                threshold=threshold
            )
            
            # Format results
            results = []
            for msg_id, similarity, data in similar_items:
                result = {
                    'id': data['id'],
                    'conversation_id': data['conversation_id'],
                    'role': data['role'],
                    'content': data['content'],
                    'timestamp': data['timestamp'],
                    'similarity': similarity,
                    'metadata': data.get('metadata')
                }
                results.append(result)
                
            logger.info(f"Retrieved {len(results)} memories (threshold: {threshold})")
            return results
            
        except Exception as e:
            logger.error(f"Error retrieving memories: {e}")
            raise
            
    def get_conversation_history(
        self,
        conversation_id: str = "default",
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Get recent messages from a conversation.
        
        Args:
            conversation_id: Conversation identifier
            limit: Maximum number of messages to return
            
        Returns:
            List of message dictionaries ordered by timestamp
        """
        try:
            safe_conv_id = sanitize_conversation_id(conversation_id)
            messages = self.db.get_conversation_history(safe_conv_id, limit)
            
            logger.info(f"Retrieved {len(messages)} messages from conversation {safe_conv_id}")
            return messages
            
        except Exception as e:
            logger.error(f"Error getting conversation history: {e}")
            raise
            
    def clear_conversation(self, conversation_id: str = "default") -> int:
        """
        Delete all messages from a conversation.
        
        Args:
            conversation_id: Conversation identifier
            
        Returns:
            Number of messages deleted
        """
        try:
            safe_conv_id = sanitize_conversation_id(conversation_id)
            count = self.db.delete_conversation(safe_conv_id)
            
            logger.info(f"Cleared conversation {safe_conv_id}: {count} messages deleted")
            return count
            
        except Exception as e:
            logger.error(f"Error clearing conversation: {e}")
            raise
            
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get memory engine statistics.
        
        Returns:
            Dictionary with statistics about stored memories
        """
        try:
            stats = self.db.get_statistics()
            stats['database_path'] = self.db_path
            stats['embedding_model'] = self.embedding_model
            
            logger.debug(f"Statistics: {stats}")
            return stats
            
        except Exception as e:
            logger.error(f"Error getting statistics: {e}")
            raise
            
    def search_by_keyword(
        self,
        keyword: str,
        conversation_id: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Simple keyword-based search (non-semantic).
        
        Args:
            keyword: Keyword to search for
            conversation_id: Optional conversation filter
            limit: Maximum number of results
            
        Returns:
            List of matching messages
        """
        try:
            # Get conversation history
            messages = self.get_conversation_history(
                conversation_id or "default",
                limit=1000  # Get more to search through
            )
            
            # Filter by keyword
            keyword_lower = keyword.lower()
            matches = [
                msg for msg in messages
                if keyword_lower in msg['content'].lower()
            ]
            
            # Limit results
            results = matches[:limit]
            
            logger.info(f"Keyword search for '{keyword}': {len(results)} matches")
            return results
            
        except Exception as e:
            logger.error(f"Error in keyword search: {e}")
            raise
            
    def close(self) -> None:
        """Close database connection and cleanup resources."""
        if self.db:
            self.db.close()
            logger.info("MemoryEngine closed")
            
    def __enter__(self):
        """Context manager entry."""
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
        
    def __repr__(self) -> str:
        """String representation of the engine."""
        return (
            f"MemoryEngine(db_path='{self.db_path}', "
            f"embedding_model='{self.embedding_model}')"
        )
