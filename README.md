# 📸 Screenshot Tool for Windsurf and Cascade

A simple and powerful tool to capture web pages and easily share them in Cascade via Windsurf.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Playwright](https://img.shields.io/badge/playwright-v1.40-green)
![License](https://img.shields.io/badge/license-MIT-orange)

## ✨ Features

- **Automatic capture** of web pages with Playwright
- **Markdown generation** with Base64 embedded images
- **Image server** to easily share captures
- **Modern web interface** with dark mode
- **Shell scripts** for simplified usage
- **User-level installation** with `capture2IA` command

## 🚀 Quick Installation

```bash
# Navigate to the tool directory
cd screenshot-tool

# Install dependencies
./install.sh
```

The installation script will:
1. Install required Node.js dependencies
2. Set up Playwright for browser automation
3. Install the `capture2IA` command in your `~/bin` directory
4. Add `~/bin` to your PATH if needed (in `.bashrc`)

After installation, you can use the tool from anywhere by simply typing `capture2IA`.

## 📋 Prerequisites

- Node.js (v14+)
- Python 3.6+
- npm

## 🔧 Usage

### Simple Capture

```bash
# Capture a screenshot of any web page
capture2IA --url http://localhost:3000
```

### Available Options

```
--url URL       URL of the page to capture (default: http://localhost:8000)
--port PORT     Port for the image server (default: 8080)
--no-editor     Don't open the editor after capture
--editor CMD    Editor command to use (default: windsurf)
--no-server     Don't start the image server
```

## 🔄 Typical Workflow

1. **Start your local web server** with your application
2. **Run the capture**: `capture2IA --url http://localhost:3000`
3. **Share the generated Markdown** in Cascade via Windsurf
4. **View and manage** captures via the MCP image server

## 🔍 Project Structure

```
screenshot-tool/
├── src/
│   ├── screenshot.js     # Capture module with Playwright
│   ├── image_server.py   # MCP server for images
│   └── capture.sh        # Main shell script
├── package.json          # Node.js dependencies
├── install.sh            # Installation script
└── README.md             # Documentation
```

## 📚 JavaScript API

```javascript
const { captureScreenshot } = require('./src/screenshot.js');

async function run() {
  const result = await captureScreenshot('http://localhost:3000', {
    outputPath: './captures',
    fullPage: true,
    generateMarkdown: true
  });
  
  console.log('Capture successful:', result.screenshotPath);
}
```

## 🤝 Contribution

Contributions are welcome! Feel free to improve this tool.

## 📄 License

MIT
