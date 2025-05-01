"""
Setup script for the Storylane Embedded Assistant.

This script installs required dependencies and sets up the environment.
"""

import os
import sys
import subprocess
import platform

def check_python_version():
    """Check if Python version is 3.8 or higher."""
    if sys.version_info < (3, 8):
        print("Error: Python 3.8 or higher is required.")
        sys.exit(1)

def install_dependencies():
    """Install required Python packages."""
    dependencies = [
        "streamlit",
        "anthropic",
        "python-dotenv",
        "langchain",
        "langchain-openai",
        "faiss-cpu",
        "beautifulsoup4",
        "pandas",
        "matplotlib",
        "pillow",
        "requests",
        "sentence-transformers",
        "sounddevice",
        "numpy",
        "openai-agents",
        "scipy",
        "SpeechRecognition",
        "queuelib",
        "pyaudio",
        "pyttsx3",
        "faster_whisper"
    ]
    
    print("Installing dependencies...")
    subprocess.check_call([sys.executable, "-m", "pip", "install"] + dependencies)
    print("Dependencies installed successfully!")

def create_env_file():
    """Create a .env file template if it doesn't exist."""
    if not os.path.exists(".env"):
        print("Creating .env file template...")
        with open(".env", "w") as f:
            f.write("# API Keys for Storylane Embedded Assistant\n")
            f.write("ANTHROPIC_API_KEY=your_anthropic_api_key_here\n")
            f.write("OPENAI_API_KEY=your_openai_api_key_here  # Optional for embeddings\n")
            f.write("SERPER_API_KEY=your_serper_api_key_here  # Optional for web search\n")
        print(".env file created. Please edit it to add your API keys.")
    else:
        print(".env file already exists.")

def main():
    """Main setup function."""
    print("Setting up Storylane Embedded Assistant...")
    
    # Check Python version
    check_python_version()
    
    # Install dependencies
    install_dependencies()
    
    # Create .env file template
    create_env_file()
    
    print("\nSetup complete!")
    print("\nTo run the app:")
    print("1. Edit the .env file to add your API keys")
    print("2. Run: streamlit run storylane_demo_assistant.py")
    print("\nAPI Keys Information:")
    print("- ANTHROPIC_API_KEY: Required for Claude (https://console.anthropic.com)")
    print("- OPENAI_API_KEY: Optional for embeddings (https://platform.openai.com)")
    print("- SERPER_API_KEY: Optional for web search (https://serper.dev)")
    print("\nNote: You can still run the app without OPENAI_API_KEY and SERPER_API_KEY,")
    print("but product knowledge and web search capabilities will be limited.")

if __name__ == "__main__":
    main()
