#!/bin/bash

# Installation script for the screenshot tool
echo "Installing the screenshot tool for Windsurf and Cascade..."

# Determine the installation directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_DIR="$SCRIPT_DIR"

# Check prerequisites
echo "Checking prerequisites..."

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed."
    echo "Please install Node.js (v14 or higher) from https://nodejs.org/"
    exit 1
else
    NODE_VERSION=$(node -v)
    echo "✅ Node.js is installed (version $NODE_VERSION)"
fi

# Check npm
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed."
    echo "npm is usually installed with Node.js. Please check your installation."
    exit 1
else
    NPM_VERSION=$(npm -v)
    echo "✅ npm is installed (version $NPM_VERSION)"
fi

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed."
    echo "Please install Python 3.6 or higher."
    exit 1
else
    PYTHON_VERSION=$(python3 --version)
    echo "✅ $PYTHON_VERSION is installed"
fi

# Install Node.js dependencies
echo "Installing Node.js dependencies..."
cd "$INSTALL_DIR"
npm install

# Install Playwright
echo "Installing Playwright..."
npx playwright install chromium

# Create directory for captures
mkdir -p "$INSTALL_DIR/captures"

# Make scripts executable
chmod +x "$INSTALL_DIR/src/capture.sh"

# Create ~/bin directory if it doesn't exist
if [ ! -d "$HOME/bin" ]; then
    echo "Creating ~/bin directory..."
    mkdir -p "$HOME/bin"
fi

# Copy capture.sh to ~/bin/capture2IA
echo "Installing capture2IA script to ~/bin..."
cp "$INSTALL_DIR/src/capture.sh" "$HOME/bin/capture2IA"
chmod +x "$HOME/bin/capture2IA"

# Check if PATH includes ~/bin and update .bashrc if needed
if ! echo "$PATH" | grep -q "$HOME/bin"; then
    echo "Updating PATH in .bashrc..."
    echo 'export PATH=~/bin:$PATH' >> "$HOME/.bashrc"
    echo "✅ Added ~/bin to PATH in .bashrc"
    echo "Please run 'source ~/.bashrc' or restart your terminal to apply changes"
else
    echo "✅ ~/bin is already in your PATH"
fi

echo "✅ Installed capture2IA script to ~/bin"

# Configuration for Windsurf integration
echo ""
read -p "Do you want to configure integration with Windsurf? (Y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]] || [[ -z $REPLY ]]; then
    echo "To integrate this tool with Windsurf, follow these steps:"
    echo "1. Open Windsurf"
    echo "2. Go to Extensions > Install from folder"
    echo "3. Select the folder: $INSTALL_DIR"
    echo ""
    echo "Or run the following command if available:"
    echo "windsurf --install-extension \"$INSTALL_DIR\""
fi

echo ""
echo "✅ Installation complete!"
echo ""
echo "To use the screenshot tool:"
echo "1. Start your local web server"
echo "2. Run: capture2IA"
echo ""
echo "Available options:"
echo "  --url URL       URL of the page to capture (default: http://localhost:8000)"
echo "  --port PORT     Port for the image server (default: 8080)"
echo ""
echo "Complete documentation available in the README.md file"
