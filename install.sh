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
        echo "Or use: brew install ollama"
    else
        echo "Please install Ollama manually from https://ollama.ai/download"
    fi
else
    echo "✅ Ollama is already installed"
fi

# Download required model
echo "📥 Downloading required model..."
ollama pull qwen:0.6b

# Create CLI symlink (optional)
if [[ "$1" == "--global" ]]; then
    echo "🔗 Setting up global CLI access..."
    chmod +x cli.py
    if [[ -w "/usr/local/bin" ]]; then
        ln -sf $(pwd)/cli.py /usr/local/bin/deepconf
        echo "✅ Global CLI installed: deepconf"
    else
        echo "⚠️  Need sudo for global install:"
        echo "   sudo ln -sf $(pwd)/cli.py /usr/local/bin/deepconf"
    fi
fi

echo ""
echo "🎉 Installation completed successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Activate the environment: source deepconf-env/bin/activate"
echo "2. Test basic functionality: python cli.py run --prompt 'Hello world' --verbose"
echo "3. Run benchmark suite: python benchmark.py"
echo "4. Try integrated analysis: python cli.py integrated --prompt 'Career advice' --profile examples/career.json"
echo ""
echo "📚 Documentation:"
echo "- Examples: ./examples/"
echo "- README: ./README.md"
echo "- Paper: ./paper/"
echo ""
echo "🌐 For support and updates:"
echo "- GitHub: https://github.com/hrbzhq/deepconf-behavior"
echo "- Issues: https://github.com/hrbzhq/deepconf-behavior/issues"
echo ""