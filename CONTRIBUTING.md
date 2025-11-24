# Contributing to Mini Memori

Thank you for your interest in contributing to Mini Memori! This document provides guidelines and instructions for contributing.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/yourusername/mini-memori.git
   cd mini-memori
   ```
3. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. **Install in development mode**:
   ```bash
   pip install -e .
   pip install pytest pytest-cov  # For testing
   ```

## Development Workflow

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**:
   - Write clean, readable code
   - Follow PEP 8 style guidelines
   - Add docstrings to functions and classes
   - Add type hints where appropriate

3. **Add tests**:
   - Write unit tests for new functionality
   - Ensure existing tests pass
   - Aim for high test coverage

4. **Run tests**:
   ```bash
   pytest tests/
   pytest --cov=mini_memori tests/  # With coverage
   ```

5. **Commit your changes**:
   ```bash
   git add .
   git commit -m "Add feature: description of your changes"
   ```

6. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request** on GitHub

## Code Style

- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Keep functions focused and concise
- Add comments for complex logic
- Use type hints for function parameters and returns

### Example:

```python
def calculate_similarity(vec1: List[float], vec2: List[float]) -> float:
    """
    Calculate cosine similarity between two vectors.
    
    Args:
        vec1: First vector
        vec2: Second vector
        
    Returns:
        Similarity score between 0 and 1
    """
    # Implementation here
    pass
```

## Testing

- Write tests for all new features
- Test edge cases and error conditions
- Use descriptive test names
- Mock external dependencies (OpenAI API)

### Running Tests:

```bash
# All tests
pytest tests/

# Specific test file
pytest tests/test_database.py

# With coverage report
pytest --cov=mini_memori --cov-report=html tests/
```

## Documentation

- Update README.md if adding new features
- Add docstrings to all public functions and classes
- Include usage examples for new features
- Update CHANGELOG.md with your changes

## Pull Request Guidelines

### Before Submitting:

- [ ] All tests pass
- [ ] Code follows style guidelines
- [ ] Documentation is updated
- [ ] Commit messages are clear and descriptive
- [ ] Changes are focused (one feature per PR)

### PR Description Should Include:

- **What**: Brief description of changes
- **Why**: Reason for the changes
- **How**: Implementation approach
- **Testing**: How you tested the changes

## Areas for Contribution

### Good First Issues:

- Improve documentation
- Add more examples
- Write additional tests
- Fix typos or formatting

### Feature Ideas:

- Support for other embedding providers (e.g., Cohere, Hugging Face)
- Web interface for memory exploration
- Export/import functionality for different formats
- Performance optimizations
- Advanced search filters
- Memory pruning/archiving features

### Bug Reports:

When reporting bugs, please include:
- Steps to reproduce
- Expected behavior
- Actual behavior
- Python version and dependencies
- Error messages/stack traces

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Provide constructive feedback
- Focus on the code, not the person
- Help maintain a positive community

## Questions?

Feel free to:
- Open an issue for discussion
- Ask questions in pull requests
- Contact the maintainers

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to Mini Memori! 🎉
