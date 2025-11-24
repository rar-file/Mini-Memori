"""
Mini Memori - Local Memory Engine for LLMs

A lightweight memory system that stores conversations and retrieves
relevant items using OpenAI embeddings.
"""

from .engine import MemoryEngine
from .database import Database
from .embeddings import EmbeddingService

__version__ = "1.0.0"
__all__ = ["MemoryEngine", "Database", "EmbeddingService"]
