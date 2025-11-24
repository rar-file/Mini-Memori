"""
Utility functions for Mini Memori.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional
import json
import logging

logger = logging.getLogger(__name__)


def format_timestamp(timestamp: str) -> str:
    """
    Format a timestamp string for display.
    
    Args:
        timestamp: ISO format timestamp string
        
    Returns:
        Formatted timestamp string
    """
    try:
        dt = datetime.fromisoformat(timestamp)
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except (ValueError, TypeError):
        return timestamp


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Truncate text to a maximum length.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def format_memory_output(
    memories: List[Dict[str, Any]],
    include_metadata: bool = False,
    max_content_length: int = 200
) -> str:
    """
    Format memories for display.
    
    Args:
        memories: List of memory dictionaries
        include_metadata: Whether to include metadata
        max_content_length: Maximum length for content display
        
    Returns:
        Formatted string
    """
    if not memories:
        return "No memories found."
        
    lines = []
    for i, memory in enumerate(memories, 1):
        score = memory.get('similarity', 0)
        role = memory.get('role', 'unknown')
        content = memory.get('content', '')
        timestamp = memory.get('timestamp', '')
        
        # Format header
        header = f"\n[{i}] {role.upper()} (similarity: {score:.3f})"
        if timestamp:
            header += f" - {format_timestamp(timestamp)}"
        lines.append(header)
        
        # Format content
        display_content = truncate_text(content, max_content_length)
        lines.append(f"    {display_content}")
        
        # Add metadata if requested
        if include_metadata and memory.get('metadata'):
            metadata_str = json.dumps(memory['metadata'], indent=2)
            lines.append(f"    Metadata: {metadata_str}")
            
    return "\n".join(lines)


def estimate_tokens(text: str) -> int:
    """
    Estimate the number of tokens in a text.
    
    This is a rough approximation: ~4 characters per token.
    For accurate counts, use tiktoken library.
    
    Args:
        text: Text to estimate
        
    Returns:
        Estimated token count
    """
    return len(text) // 4


def prepare_context_window(
    memories: List[Dict[str, Any]],
    max_tokens: int = 4000
) -> List[Dict[str, Any]]:
    """
    Prepare memories to fit within a token budget.
    
    Args:
        memories: List of memory dictionaries
        max_tokens: Maximum token budget
        
    Returns:
        Filtered list of memories that fit within budget
    """
    result = []
    total_tokens = 0
    
    for memory in memories:
        content = memory.get('content', '')
        tokens = estimate_tokens(content)
        
        if total_tokens + tokens > max_tokens:
            logger.debug(f"Reached token limit: {total_tokens}/{max_tokens}")
            break
            
        result.append(memory)
        total_tokens += tokens
        
    return result


def sanitize_conversation_id(conversation_id: str) -> str:
    """
    Sanitize a conversation ID to ensure it's safe for database use.
    
    Args:
        conversation_id: Raw conversation ID
        
    Returns:
        Sanitized conversation ID
    """
    # Remove any potentially problematic characters
    safe_id = "".join(c for c in conversation_id if c.isalnum() or c in "_-.")
    
    # Ensure it's not empty
    if not safe_id:
        safe_id = "default"
        
    return safe_id


def validate_message_data(
    role: str,
    content: str,
    conversation_id: str
) -> tuple[bool, Optional[str]]:
    """
    Validate message data before saving.
    
    Args:
        role: Message role
        content: Message content
        conversation_id: Conversation ID
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not role or not isinstance(role, str):
        return False, "Role must be a non-empty string"
        
    if not content or not isinstance(content, str):
        return False, "Content must be a non-empty string"
        
    if not conversation_id or not isinstance(conversation_id, str):
        return False, "Conversation ID must be a non-empty string"
        
    valid_roles = ['user', 'assistant', 'system']
    if role not in valid_roles:
        logger.warning(f"Unusual role: {role}. Recommended: {valid_roles}")
        
    return True, None


def create_message_dict(
    role: str,
    content: str,
    metadata: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Create a standardized message dictionary.
    
    Args:
        role: Message role
        content: Message content
        metadata: Optional metadata
        
    Returns:
        Message dictionary
    """
    message = {
        'role': role,
        'content': content,
        'timestamp': datetime.utcnow().isoformat()
    }
    
    if metadata:
        message['metadata'] = metadata
        
    return message
