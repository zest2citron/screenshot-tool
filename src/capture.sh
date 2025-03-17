#!/bin/bash

# Screenshot Tool for Windsurf and Cascade
# A simple tool to capture web pages and share them easily

# Default values
URL="http://localhost:8000"
PORT="8080"
OPEN_EDITOR=true
EDITOR_CMD="windsurf"
START_SERVER=true

# Get the script directory (works with symlinks)
SCRIPT_DIR="$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")" && pwd)"
PARENT_DIR="$(dirname "$SCRIPT_DIR")"

# Parse command line arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --url)
      URL="$2"
      shift 2
      ;;
    --port)
      PORT="$2"
      shift 2
      ;;
    --no-editor)
      OPEN_EDITOR=false
      shift
      ;;
    --editor)
      EDITOR_CMD="$2"
      shift 2
      ;;
    --no-server)
      START_SERVER=false
      shift
      ;;
    *)
      echo "Unknown option: $1"
      echo "Usage: $0 [--url URL] [--port PORT] [--no-editor] [--editor CMD] [--no-server]"
      exit 1
      ;;
  esac
done

# Create captures directory if it doesn't exist
CAPTURES_DIR="$PARENT_DIR/captures"
mkdir -p "$CAPTURES_DIR"

# Generate a timestamp for the filename
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
SCREENSHOT_FILE="$CAPTURES_DIR/screenshot_$TIMESTAMP.png"
MARKDOWN_FILE="$CAPTURES_DIR/screenshot_$TIMESTAMP.md"
SHARE_FILE="$PARENT_DIR/screenshot_to_share.md"

# Display banner
echo "╔════════════════════════════════════════════════════╗"
echo "║                                                    ║"
echo "║  📸 Screenshot Tool for Windsurf and Cascade       ║"
echo "║                                                    ║"
echo "╚════════════════════════════════════════════════════╝"
echo ""
echo "📌 URL to capture: $URL"
echo "🖼️  Output file: $SCREENSHOT_FILE"
echo "📄 Markdown file: $MARKDOWN_FILE"
echo ""

# Take the screenshot using Node.js script
echo "📸 Taking screenshot of $URL..."
node "$SCRIPT_DIR/screenshot.js" "$URL" "$SCREENSHOT_FILE" "$MARKDOWN_FILE"

# Check if the screenshot was successful
if [ ! -f "$SCREENSHOT_FILE" ]; then
  echo "❌ Failed to capture screenshot. Please check the URL and try again."
  exit 1
fi

# Copy the markdown file to the share location
cp "$MARKDOWN_FILE" "$SHARE_FILE"
echo "✅ Screenshot captured successfully!"
echo "📄 Markdown file created: $MARKDOWN_FILE"
echo "📄 Share file created: $SHARE_FILE"

# Start the image server if requested
if [ "$START_SERVER" = true ]; then
  echo ""
  echo "🖥️  Starting image server on port $PORT..."
  echo "📊 Server URL: http://localhost:$PORT"
  echo "Press Ctrl+C to stop the server"
  echo ""
  
  # Start the server in the background
  python3 "$SCRIPT_DIR/image_server.py" "$CAPTURES_DIR" "$PORT" &
  SERVER_PID=$!
  
  # Give the server a moment to start
  sleep 1
  
  # Open the editor if requested
  if [ "$OPEN_EDITOR" = true ]; then
    echo "🖊️  Opening editor: $EDITOR_CMD $SHARE_FILE"
    $EDITOR_CMD "$SHARE_FILE" &
    EDITOR_PID=$!
  fi
  
  # Wait for user to press Ctrl+C
  trap "kill $SERVER_PID 2>/dev/null; [ -n \"$EDITOR_PID\" ] && kill $EDITOR_PID 2>/dev/null; echo ''; echo '🛑 Server stopped'; exit 0" INT
  wait $SERVER_PID
else
  # Open the editor if requested
  if [ "$OPEN_EDITOR" = true ]; then
    echo "🖊️  Opening editor: $EDITOR_CMD $SHARE_FILE"
    $EDITOR_CMD "$SHARE_FILE"
  fi
fi

echo ""
echo "✨ Done! You can now share the screenshot using the markdown file."
echo "📄 $SHARE_FILE"
