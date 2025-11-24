"""
Installation and verification script for Mini Memori.

Run this script to verify your installation and setup.
"""

import sys
import os
import importlib.util


def check_python_version():
    """Check Python version."""
    print("🐍 Checking Python version...")
    if sys.version_info < (3, 8):
        print("   ❌ Python 3.8 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    print(f"   ✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True


def check_dependencies():
    """Check required dependencies."""
    print("\n📦 Checking dependencies...")
    
    required = {
        'openai': 'openai',
        'numpy': 'numpy',
        'dotenv': 'python-dotenv'
    }
    
    all_installed = True
    for module, package in required.items():
        spec = importlib.util.find_spec(module)
        if spec is None:
            print(f"   ❌ {package} is not installed")
            all_installed = False
        else:
            print(f"   ✅ {package} is installed")
    
    return all_installed


def check_api_key():
    """Check if OpenAI API key is set."""
    print("\n🔑 Checking API key...")
    
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("   ⚠️  OPENAI_API_KEY environment variable is not set")
        print("   Set it with: export OPENAI_API_KEY=your_key_here")
        return False
    
    if api_key.startswith('sk-'):
        print("   ✅ API key is set")
        return True
    else:
        print("   ⚠️  API key format looks incorrect")
        return False


def check_package_installation():
    """Check if mini_memori package is installed."""
    print("\n📚 Checking package installation...")
    
    spec = importlib.util.find_spec('mini_memori')
    if spec is None:
        print("   ❌ mini_memori is not installed")
        print("   Install with: pip install -e .")
        return False
    
    print("   ✅ mini_memori is installed")
    
    # Try importing main classes
    try:
        from mini_memori import MemoryEngine
        print("   ✅ MemoryEngine imported successfully")
        return True
    except Exception as e:
        print(f"   ❌ Error importing: {e}")
        return False


def run_basic_test():
    """Run a basic functionality test."""
    print("\n🧪 Running basic functionality test...")
    
    try:
        import tempfile
        from mini_memori import MemoryEngine
        
        # Create temporary database
        with tempfile.NamedTemporaryFile(delete=False, suffix='.db') as f:
            temp_db = f.name
        
        try:
            # Create engine (will fail if API key is invalid)
            print("   Creating memory engine...")
            engine = MemoryEngine(db_path=temp_db)
            
            # Test save (without generating embedding to avoid API call)
            print("   Testing message save...")
            msg_id = engine.save_message(
                role="user",
                content="Test message",
                generate_embedding=False
            )
            
            print("   Testing database query...")
            history = engine.get_conversation_history("default")
            
            if len(history) > 0:
                print("   ✅ Basic functionality test passed!")
                return True
            else:
                print("   ❌ Test failed: no messages retrieved")
                return False
                
        finally:
            # Clean up
            if os.path.exists(temp_db):
                os.unlink(temp_db)
                
    except Exception as e:
        print(f"   ❌ Test failed: {e}")
        return False


def print_next_steps():
    """Print next steps for the user."""
    print("\n" + "="*60)
    print("🎉 Next Steps:")
    print("="*60)
    print("\n1. Set your OpenAI API key (if not already done):")
    print("   export OPENAI_API_KEY=your_key_here")
    print("\n2. Try the examples:")
    print("   python examples/basic_usage.py")
    print("\n3. Start the interactive chatbot:")
    print("   python -m mini_memori.chatbot")
    print("\n4. Read the documentation:")
    print("   - README.md - Full documentation")
    print("   - QUICKSTART.md - Quick start guide")
    print("   - examples/ - Example scripts")
    print("\n5. Run the tests:")
    print("   pytest tests/")
    print()


def main():
    """Main verification routine."""
    print("\n" + "="*60)
    print("🧠 Mini Memori - Installation Verification")
    print("="*60)
    
    results = []
    
    # Run checks
    results.append(("Python version", check_python_version()))
    results.append(("Dependencies", check_dependencies()))
    results.append(("Package installation", check_package_installation()))
    results.append(("API key", check_api_key()))
    results.append(("Basic functionality", run_basic_test()))
    
    # Summary
    print("\n" + "="*60)
    print("📊 Verification Summary:")
    print("="*60)
    
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {name}")
    
    # Overall result
    all_passed = all(result[1] for result in results)
    
    if all_passed:
        print("\n🎉 All checks passed! You're ready to use Mini Memori.")
        print_next_steps()
        return 0
    else:
        print("\n⚠️  Some checks failed. Please fix the issues above.")
        print("\nFor help, see:")
        print("  - QUICKSTART.md")
        print("  - DEVELOPMENT.md")
        print("  - GitHub Issues: https://github.com/yourusername/mini-memori/issues")
        return 1


if __name__ == "__main__":
    sys.exit(main())
