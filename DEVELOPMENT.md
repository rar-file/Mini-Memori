# Development Setup Guide

Complete guide for setting up a development environment for Mini Memori.

## Prerequisites

- Python 3.8 or higher
- Git
- OpenAI API key
- Virtual environment tool (venv, conda, or virtualenv)

## Step-by-Step Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/mini-memori.git
cd mini-memori
```

### 2. Create Virtual Environment

#### Using venv (recommended):
```bash
python -m venv venv
```

#### Activate the environment:

**Linux/Mac:**
```bash
source venv/bin/activate
```

**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
venv\Scripts\activate.bat
```

### 3. Install Dependencies

#### Install in development mode:
```bash
pip install -e .
```

#### Install development dependencies:
```bash
pip install pytest pytest-cov black flake8 mypy
```

### 4. Set Up Environment Variables

#### Create `.env` file:
```bash
# Copy the example
cp .env.example .env

# Edit with your API key
# Linux/Mac:
nano .env

# Windows:
notepad .env
```

#### Add your OpenAI API key:
```
OPENAI_API_KEY=sk-your-key-here
```

### 5. Verify Installation

```bash
# Run tests
pytest tests/

# Run example
python examples/basic_usage.py

# Start chatbot
python -m mini_memori.chatbot
```

## Development Workflow

### 1. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Make Changes

Edit files in your IDE/editor of choice.

### 3. Run Tests Frequently

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_database.py

# Run with coverage
pytest --cov=mini_memori tests/

# Generate HTML coverage report
pytest --cov=mini_memori --cov-report=html tests/
```

### 4. Check Code Quality

```bash
# Format code with black
black mini_memori/

# Lint with flake8
flake8 mini_memori/

# Type check with mypy
mypy mini_memori/ --ignore-missing-imports
```

### 5. Commit Changes

```bash
git add .
git commit -m "feat: add new feature description"
```

#### Commit Message Format:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `test:` - Test additions/changes
- `refactor:` - Code refactoring
- `style:` - Code style changes
- `chore:` - Maintenance tasks

### 6. Push and Create PR

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub.

## Project Structure for Development

```
mini-memori/
├── mini_memori/      # Main source code - edit here
├── tests/            # Test files - add tests here
├── examples/         # Example scripts - add examples here
├── docs/             # Documentation (future)
└── .github/          # GitHub Actions workflows
```

## Common Development Tasks

### Adding a New Feature

1. **Write the feature** in `mini_memori/`
2. **Add tests** in `tests/`
3. **Add example** in `examples/` (if applicable)
4. **Update documentation** in README.md
5. **Run tests**: `pytest tests/`
6. **Commit and push**

### Debugging

#### Enable debug logging:
```python
from mini_memori.config import setup_logging

setup_logging("DEBUG")
```

#### Interactive Python:
```python
python
>>> from mini_memori import MemoryEngine
>>> engine = MemoryEngine(db_path="debug.db")
>>> # Test your code here
```

#### Database inspection:
```bash
sqlite3 memories.db
sqlite> .tables
sqlite> SELECT * FROM messages;
sqlite> .quit
```

### Testing with Mock Data

```python
# In tests, mock OpenAI API:
from unittest.mock import Mock, patch

@patch('mini_memori.embeddings.openai.embeddings.create')
def test_something(mock_create):
    mock_create.return_value = Mock(data=[Mock(embedding=[0.1] * 1536)])
    # Your test code here
```

## IDE Setup

### VS Code

Recommended extensions:
- Python
- Pylance
- Python Test Explorer

#### settings.json:
```json
{
  "python.linting.enabled": true,
  "python.linting.flake8Enabled": true,
  "python.formatting.provider": "black",
  "python.testing.pytestEnabled": true,
  "editor.formatOnSave": true
}
```

### PyCharm

1. Open project
2. Configure Python interpreter (point to venv)
3. Enable pytest as test runner
4. Install black formatter plugin

## Environment Variables

### Required:
- `OPENAI_API_KEY` - Your OpenAI API key

### Optional:
- `DB_PATH` - Database file path (default: "memories.db")
- `EMBEDDING_MODEL` - Embedding model (default: "text-embedding-3-small")
- `CHAT_MODEL` - Chat model (default: "gpt-4o-mini")
- `LOG_LEVEL` - Logging level (default: "INFO")

## Troubleshooting

### Import Errors

```bash
# Make sure package is installed in development mode
pip install -e .
```

### Test Failures

```bash
# Clean up test databases
rm -f test_*.db
rm -f *_test.db

# Clear pytest cache
rm -rf .pytest_cache

# Run tests with verbose output
pytest -v tests/
```

### API Key Issues

```bash
# Check if API key is set
python -c "import os; print(os.getenv('OPENAI_API_KEY'))"

# Test API connection
python -c "import openai; openai.api_key='your-key'; print('OK')"
```

### Database Locked

```bash
# Close all connections or delete database
rm memories.db
```

## Building and Distribution

### Build package:
```bash
python setup.py sdist bdist_wheel
```

### Install locally:
```bash
pip install dist/mini_memori-1.0.0-py3-none-any.whl
```

### Upload to PyPI (maintainers only):
```bash
pip install twine
twine upload dist/*
```

## Resources

- [Python Packaging Guide](https://packaging.python.org/)
- [pytest Documentation](https://docs.pytest.org/)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- [SQLite Documentation](https://www.sqlite.org/docs.html)

## Getting Help

- Check existing [GitHub Issues](https://github.com/yourusername/mini-memori/issues)
- Read the [Contributing Guide](CONTRIBUTING.md)
- Ask questions in Pull Requests
- Contact maintainers

---

Happy developing! 🚀
