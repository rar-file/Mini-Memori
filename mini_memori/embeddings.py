"""
Embeddings module for Mini Memori.

Handles OpenAI embeddings generation and vector similarity calculations.
"""

import openai
from typing import List, Optional
import numpy as np
import logging

logger = logging.getLogger(__name__)


class EmbeddingService:
    """
    Service for generating and comparing embeddings using OpenAI's API.
    
    This class handles:
    - Embedding generation via OpenAI API
    - Cosine similarity calculations
    - Batch processing of embeddings
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "text-embedding-3-small"
    ):
        """
        Initialize the embedding service.
        
        Args:
            api_key: OpenAI API key (if None, uses environment variable)
            model: OpenAI embedding model to use
        """
        self.model = model
        
        if api_key:
            openai.api_key = api_key
            
        logger.info(f"Initialized EmbeddingService with model: {model}")
        
    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate an embedding vector for the given text.
        
        Args:
            text: Text to embed
            
        Returns:
            Embedding vector as list of floats
            
        Raises:
            Exception: If API call fails
        """
        try:
            # Clean and prepare text
            text = text.replace("\n", " ").strip()
            
            if not text:
                raise ValueError("Cannot generate embedding for empty text")
                
            # Call OpenAI API
            response = openai.embeddings.create(
                input=text,
                model=self.model
            )
            
            embedding = response.data[0].embedding
            logger.debug(f"Generated embedding of dimension {len(embedding)}")
            
            return embedding
            
        except openai.APIError as e:
            logger.error(f"OpenAI API error: {e}")
            raise
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            raise
            
    def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts in a batch.
        
        Args:
            texts: List of texts to embed
            
        Returns:
            List of embedding vectors
        """
        try:
            # Clean texts
            cleaned_texts = [text.replace("\n", " ").strip() for text in texts]
            
            # Filter out empty texts
            valid_texts = [text for text in cleaned_texts if text]
            
            if not valid_texts:
                raise ValueError("No valid texts to embed")
                
            # Call OpenAI API with batch
            response = openai.embeddings.create(
                input=valid_texts,
                model=self.model
            )
            
            embeddings = [item.embedding for item in response.data]
            logger.debug(f"Generated {len(embeddings)} embeddings in batch")
            
            return embeddings
            
        except openai.APIError as e:
            logger.error(f"OpenAI API error in batch processing: {e}")
            raise
        except Exception as e:
            logger.error(f"Error generating embeddings batch: {e}")
            raise
            
    @staticmethod
    def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
        """
        Calculate cosine similarity between two vectors.
        
        Args:
            vec1: First vector
            vec2: Second vector
            
        Returns:
            Cosine similarity score (0 to 1)
        """
        try:
            # Convert to numpy arrays for efficient computation
            v1 = np.array(vec1)
            v2 = np.array(vec2)
            
            # Calculate cosine similarity
            dot_product = np.dot(v1, v2)
            norm_v1 = np.linalg.norm(v1)
            norm_v2 = np.linalg.norm(v2)
            
            if norm_v1 == 0 or norm_v2 == 0:
                return 0.0
                
            similarity = dot_product / (norm_v1 * norm_v2)
            
            # Clamp to [0, 1] range (handle floating point errors)
            similarity = max(0.0, min(1.0, float(similarity)))
            
            return similarity
            
        except Exception as e:
            logger.error(f"Error calculating cosine similarity: {e}")
            raise
            
    def find_most_similar(
        self,
        query_embedding: List[float],
        embeddings: List[tuple],
        top_k: int = 5,
        threshold: float = 0.0
    ) -> List[tuple]:
        """
        Find the most similar embeddings to a query embedding.
        
        Args:
            query_embedding: Query vector
            embeddings: List of (id, embedding_vector, data) tuples
            top_k: Number of results to return
            threshold: Minimum similarity threshold
            
        Returns:
            List of (id, similarity_score, data) tuples, sorted by similarity
        """
        try:
            similarities = []
            
            for item_id, embedding_vec, data in embeddings:
                similarity = self.cosine_similarity(query_embedding, embedding_vec)
                
                if similarity >= threshold:
                    similarities.append((item_id, similarity, data))
                    
            # Sort by similarity (descending) and take top_k
            similarities.sort(key=lambda x: x[1], reverse=True)
            results = similarities[:top_k]
            
            logger.debug(f"Found {len(results)} similar items (threshold: {threshold})")
            return results
            
        except Exception as e:
            logger.error(f"Error finding similar embeddings: {e}")
            raise
            
    def get_embedding_dimension(self) -> int:
        """
        Get the dimension of embeddings for the current model.
        
        Returns:
            Embedding dimension
        """
        # Map of known models to dimensions
        dimensions = {
            "text-embedding-3-small": 1536,
            "text-embedding-3-large": 3072,
            "text-embedding-ada-002": 1536,
        }
        
        return dimensions.get(self.model, 1536)
