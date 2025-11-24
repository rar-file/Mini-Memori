"""
Unit tests for Mini Memori embeddings module.
"""

import unittest
from unittest.mock import Mock, patch
from mini_memori.embeddings import EmbeddingService


class TestEmbeddingService(unittest.TestCase):
    """Test cases for EmbeddingService class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.service = EmbeddingService(model="text-embedding-3-small")
        
    def test_initialization(self):
        """Test service initialization."""
        self.assertEqual(self.service.model, "text-embedding-3-small")
        
    @patch('mini_memori.embeddings.openai.embeddings.create')
    def test_generate_embedding(self, mock_create):
        """Test embedding generation."""
        # Mock the API response
        mock_response = Mock()
        mock_response.data = [Mock(embedding=[0.1, 0.2, 0.3])]
        mock_create.return_value = mock_response
        
        # Generate embedding
        result = self.service.generate_embedding("test text")
        
        # Verify
        self.assertEqual(result, [0.1, 0.2, 0.3])
        mock_create.assert_called_once()
        
    @patch('mini_memori.embeddings.openai.embeddings.create')
    def test_generate_embedding_cleans_text(self, mock_create):
        """Test that text is cleaned before embedding."""
        mock_response = Mock()
        mock_response.data = [Mock(embedding=[0.1, 0.2, 0.3])]
        mock_create.return_value = mock_response
        
        # Text with newlines
        self.service.generate_embedding("test\ntext\nwith\nnewlines")
        
        # Check that create was called with cleaned text
        call_args = mock_create.call_args
        self.assertNotIn("\n", call_args[1]['input'])
        
    def test_generate_embedding_empty_text(self):
        """Test that empty text raises error."""
        with self.assertRaises(ValueError):
            self.service.generate_embedding("")
            
    @patch('mini_memori.embeddings.openai.embeddings.create')
    def test_generate_embeddings_batch(self, mock_create):
        """Test batch embedding generation."""
        mock_response = Mock()
        mock_response.data = [
            Mock(embedding=[0.1, 0.2, 0.3]),
            Mock(embedding=[0.4, 0.5, 0.6])
        ]
        mock_create.return_value = mock_response
        
        # Generate batch
        texts = ["text 1", "text 2"]
        results = self.service.generate_embeddings_batch(texts)
        
        # Verify
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0], [0.1, 0.2, 0.3])
        self.assertEqual(results[1], [0.4, 0.5, 0.6])
        
    def test_cosine_similarity_identical(self):
        """Test cosine similarity of identical vectors."""
        vec = [1.0, 2.0, 3.0]
        similarity = EmbeddingService.cosine_similarity(vec, vec)
        self.assertAlmostEqual(similarity, 1.0, places=5)
        
    def test_cosine_similarity_orthogonal(self):
        """Test cosine similarity of orthogonal vectors."""
        vec1 = [1.0, 0.0, 0.0]
        vec2 = [0.0, 1.0, 0.0]
        similarity = EmbeddingService.cosine_similarity(vec1, vec2)
        self.assertAlmostEqual(similarity, 0.0, places=5)
        
    def test_cosine_similarity_opposite(self):
        """Test cosine similarity of opposite vectors."""
        vec1 = [1.0, 1.0, 1.0]
        vec2 = [-1.0, -1.0, -1.0]
        similarity = EmbeddingService.cosine_similarity(vec1, vec2)
        # Should be clamped to 0.0 (we clamp negative values)
        self.assertGreaterEqual(similarity, 0.0)
        
    def test_cosine_similarity_zero_vector(self):
        """Test cosine similarity with zero vector."""
        vec1 = [1.0, 2.0, 3.0]
        vec2 = [0.0, 0.0, 0.0]
        similarity = EmbeddingService.cosine_similarity(vec1, vec2)
        self.assertEqual(similarity, 0.0)
        
    def test_find_most_similar(self):
        """Test finding most similar embeddings."""
        query = [1.0, 0.0, 0.0]
        
        embeddings = [
            (1, [1.0, 0.0, 0.0], {"content": "exact match"}),
            (2, [0.9, 0.1, 0.0], {"content": "close match"}),
            (3, [0.0, 1.0, 0.0], {"content": "orthogonal"}),
            (4, [0.5, 0.5, 0.0], {"content": "medium match"}),
        ]
        
        # Find top 2
        results = self.service.find_most_similar(query, embeddings, top_k=2)
        
        # Verify
        self.assertEqual(len(results), 2)
        
        # First should be exact match
        self.assertEqual(results[0][0], 1)
        self.assertAlmostEqual(results[0][1], 1.0, places=5)
        
        # Second should be close match
        self.assertEqual(results[1][0], 2)
        
    def test_find_most_similar_with_threshold(self):
        """Test finding similar embeddings with threshold."""
        query = [1.0, 0.0, 0.0]
        
        embeddings = [
            (1, [1.0, 0.0, 0.0], {"content": "exact match"}),
            (2, [0.0, 1.0, 0.0], {"content": "orthogonal"}),
        ]
        
        # High threshold should exclude orthogonal
        results = self.service.find_most_similar(
            query, embeddings, top_k=10, threshold=0.9
        )
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][0], 1)
        
    def test_get_embedding_dimension(self):
        """Test getting embedding dimension."""
        # Test known models
        service_small = EmbeddingService(model="text-embedding-3-small")
        self.assertEqual(service_small.get_embedding_dimension(), 1536)
        
        service_large = EmbeddingService(model="text-embedding-3-large")
        self.assertEqual(service_large.get_embedding_dimension(), 3072)
        
        # Unknown model should return default
        service_unknown = EmbeddingService(model="unknown-model")
        self.assertEqual(service_unknown.get_embedding_dimension(), 1536)


if __name__ == '__main__':
    unittest.main()
