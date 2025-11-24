"""
Configuration module for Mini Memori.

Handles environment variables and application configuration.
"""

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)


class Config:
    """
    Configuration management for Mini Memori.
    
    Loads configuration from environment variables and .env file.
    """
    
    def __init__(self, env_file: Optional[str] = None):
        """
        Initialize configuration.
        
        Args:
            env_file: Path to .env file (optional)
        """
        # Load .env file if it exists
        if env_file:
            load_dotenv(env_file)
        else:
            # Try to find .env in current directory or parent directories
            load_dotenv()
            
        logger.info("Configuration loaded")
        
    @property
    def openai_api_key(self) -> Optional[str]:
        """Get OpenAI API key from environment."""
        key = os.getenv("OPENAI_API_KEY")
        if not key:
            logger.warning("OPENAI_API_KEY not found in environment")
        return key
        
    @property
    def db_path(self) -> str:
        """Get database path from environment or use default."""
        return os.getenv("DB_PATH", "memories.db")
        
    @property
    def embedding_model(self) -> str:
        """Get embedding model from environment or use default."""
        return os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
        
    @property
    def chat_model(self) -> str:
        """Get chat model from environment or use default."""
        return os.getenv("CHAT_MODEL", "gpt-4o-mini")
        
    @property
    def log_level(self) -> str:
        """Get log level from environment or use default."""
        return os.getenv("LOG_LEVEL", "INFO")
        
    def validate(self) -> bool:
        """
        Validate that required configuration is present.
        
        Returns:
            True if configuration is valid
        """
        if not self.openai_api_key:
            logger.error("Missing required OPENAI_API_KEY")
            return False
            
        return True
        
    def __repr__(self) -> str:
        """String representation of configuration (excluding sensitive data)."""
        return (
            f"Config(db_path='{self.db_path}', "
            f"embedding_model='{self.embedding_model}', "
            f"chat_model='{self.chat_model}', "
            f"api_key_set={bool(self.openai_api_key)})"
        )


# Global config instance
_config = None


def get_config(env_file: Optional[str] = None) -> Config:
    """
    Get the global configuration instance.
    
    Args:
        env_file: Path to .env file (optional)
        
    Returns:
        Config instance
    """
    global _config
    if _config is None:
        _config = Config(env_file)
    return _config


def setup_logging(level: Optional[str] = None) -> None:
    """
    Set up logging configuration.
    
    Args:
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    config = get_config()
    log_level = level or config.log_level
    
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    logger.info(f"Logging configured at {log_level} level")
