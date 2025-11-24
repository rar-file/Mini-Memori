"""
Unit tests for Mini Memori utility functions.
"""

import unittest
from datetime import datetime
from mini_memori.utils import (
    format_timestamp,
    truncate_text,
    estimate_tokens,
    sanitize_conversation_id,
    validate_message_data,
    create_message_dict,
)


class TestUtils(unittest.TestCase):
    """Test cases for utility functions."""
    
    def test_format_timestamp(self):
        """Test timestamp formatting."""
        timestamp = "2024-01-15T10:30:00"
        result = format_timestamp(timestamp)
        self.assertEqual(result, "2024-01-15 10:30:00")
        
    def test_format_timestamp_invalid(self):
        """Test formatting invalid timestamp."""
        invalid = "not a timestamp"
        result = format_timestamp(invalid)
        self.assertEqual(result, invalid)
        
    def test_truncate_text_short(self):
        """Test truncating text that's already short."""
        text = "Short text"
        result = truncate_text(text, max_length=100)
        self.assertEqual(result, text)
        
    def test_truncate_text_long(self):
        """Test truncating long text."""
        text = "A" * 200
        result = truncate_text(text, max_length=50)
        self.assertEqual(len(result), 50)
        self.assertTrue(result.endswith("..."))
        
    def test_truncate_text_custom_suffix(self):
        """Test truncating with custom suffix."""
        text = "A" * 200
        result = truncate_text(text, max_length=50, suffix=" [more]")
        self.assertTrue(result.endswith(" [more]"))
        
    def test_estimate_tokens(self):
        """Test token estimation."""
        text = "A" * 400  # ~100 tokens
        result = estimate_tokens(text)
        self.assertEqual(result, 100)
        
    def test_sanitize_conversation_id_valid(self):
        """Test sanitizing valid conversation ID."""
        conv_id = "valid_conversation-123"
        result = sanitize_conversation_id(conv_id)
        self.assertEqual(result, conv_id)
        
    def test_sanitize_conversation_id_invalid_chars(self):
        """Test sanitizing ID with invalid characters."""
        conv_id = "conversation@#$%^&*()"
        result = sanitize_conversation_id(conv_id)
        self.assertEqual(result, "conversation")
        
    def test_sanitize_conversation_id_empty(self):
        """Test sanitizing empty ID."""
        result = sanitize_conversation_id("@#$%")
        self.assertEqual(result, "default")
        
    def test_validate_message_data_valid(self):
        """Test validating valid message data."""
        is_valid, error = validate_message_data(
            role="user",
            content="Test message",
            conversation_id="conv_1"
        )
        self.assertTrue(is_valid)
        self.assertIsNone(error)
        
    def test_validate_message_data_empty_role(self):
        """Test validating with empty role."""
        is_valid, error = validate_message_data(
            role="",
            content="Test message",
            conversation_id="conv_1"
        )
        self.assertFalse(is_valid)
        self.assertIsNotNone(error)
        
    def test_validate_message_data_empty_content(self):
        """Test validating with empty content."""
        is_valid, error = validate_message_data(
            role="user",
            content="",
            conversation_id="conv_1"
        )
        self.assertFalse(is_valid)
        self.assertIsNotNone(error)
        
    def test_validate_message_data_empty_conversation_id(self):
        """Test validating with empty conversation ID."""
        is_valid, error = validate_message_data(
            role="user",
            content="Test message",
            conversation_id=""
        )
        self.assertFalse(is_valid)
        self.assertIsNotNone(error)
        
    def test_validate_message_data_wrong_type(self):
        """Test validating with wrong data type."""
        is_valid, error = validate_message_data(
            role=123,  # Should be string
            content="Test message",
            conversation_id="conv_1"
        )
        self.assertFalse(is_valid)
        self.assertIsNotNone(error)
        
    def test_create_message_dict(self):
        """Test creating message dictionary."""
        result = create_message_dict(
            role="user",
            content="Test message"
        )
        
        self.assertEqual(result['role'], "user")
        self.assertEqual(result['content'], "Test message")
        self.assertIn('timestamp', result)
        
    def test_create_message_dict_with_metadata(self):
        """Test creating message dict with metadata."""
        metadata = {"key": "value"}
        result = create_message_dict(
            role="user",
            content="Test message",
            metadata=metadata
        )
        
        self.assertEqual(result['metadata'], metadata)


if __name__ == '__main__':
    unittest.main()
