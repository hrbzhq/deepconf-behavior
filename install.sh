#!/bin/bash
# DeepConf-Behavior Installation Script
# =====================================

set -e

echo "🚀 Installing DeepConf-Behavior Framework..."
echo "============================================="

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" = "$required_version" ]; then
    echo "✅ Python $python_version is compatible"
else
    echo "❌ Error: Python $required_version or higher is required. Found: $python_version"
    exit 1
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv deepconf-env
source deepconf-env/bin/activate

# Upgrade pip
echo "🔧 Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Install Ollama (if not present)
if ! command -v ollama &> /dev/null; then
    echo "🔄 Installing Ollama..."
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        curl -fsSL https://ollama.ai/install.sh | sh
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "Please install Ollama from https://ollama.ai/download"
    else
        echo "Please install Ollama manually from https://ollama.ai/download"
    fi
else
    echo "✅ Ollama is already installed"
fi

# Download required model
echo "📥 Downloading required model..."
ollama pull qwen3:0.6b

# Create CLI symlink
echo "🔗 Setting up CLI..."
chmod +x cli.py
ln -sf $(pwd)/cli.py /usr/local/bin/deepconf

echo ""
echo "🎉 Installation completed successfully!"
echo ""
echo "Next steps:"
echo "1. Activate the environment: source deepconf-env/bin/activate"
echo "2. Test the installation: python cli.py run --prompt 'Hello world' --verbose"
echo "3. Or use: deepconf run --prompt 'Hello world' --verbose"
echo ""
echo "For examples and documentation, see:"
echo "- examples/ directory"
echo "- README.md"
echo ""