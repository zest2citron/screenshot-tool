#!/usr/bin/env python3
from http.server import HTTPServer, SimpleHTTPRequestHandler
import os
import sys
import webbrowser
import socket
import json
import argparse
from urllib.parse import parse_qs, urlparse
from datetime import datetime

class ImageServer(SimpleHTTPRequestHandler):
    def __init__(self, *args, directory=None, **kwargs):
        self.directory = directory
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        # Handle GET requests
        if self.path == '/' or self.path.startswith('/?'):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            # List available images
            images = [f for f in os.listdir(self.directory) if f.endswith(('.png', '.jpg', '.jpeg', '.gif'))]
            
            # Get selected image or use screenshot.png as default
            query_components = parse_qs(urlparse(self.path).query)
            selected_image = query_components.get('image', ['screenshot.png'])[0]
            
            # Check if image exists
            image_path = os.path.join(self.directory, selected_image)
            image_exists = os.path.exists(image_path)
            
            # Get image information
            if image_exists:
                image_size = os.path.getsize(image_path) / 1024  # Size in KB
                image_mtime = datetime.fromtimestamp(os.path.getmtime(image_path)).strftime('%Y-%m-%d %H:%M:%S')
            else:
                image_size = 0
                image_mtime = 'N/A'
            
            # Create option elements for the select dropdown
            options_html = ""
            for img in images:
                selected = "selected" if img == selected_image else ""
                options_html += f'<option value="{img}" {selected}>{img}</option>'
            
            # Create image preview HTML
            if image_exists:
                timestamp = os.path.getmtime(image_path) if image_exists else "0"
                image_preview = f'<img class="image-preview" src="/{selected_image}?t={timestamp}" alt="Image preview">'
            else:
                image_preview = '<p>The selected image does not exist.</p>'
            
            # Create image URL
            image_url = f"http://{self.server.server_address[0]}:{self.server.server_address[1]}/{selected_image}"
            
            html_content = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>MCP Image Server</title>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <style>
                    :root {
                        --primary-color: #4361ee;
                        --secondary-color: #3a0ca3;
                        --accent-color: #f72585;
                        --bg-color: #f8f9fa;
                        --text-color: #2b2d42;
                        --card-bg: #ffffff;
                        --border-radius: 8px;
                        --box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                    }
                    
                    @media (prefers-color-scheme: dark) {
                        :root {
                            --bg-color: #121212;
                            --text-color: #e0e0e0;
                            --card-bg: #1e1e1e;
                            --box-shadow: 0 4px 12px rgba(0,0,0,0.3);
                        }
                    }
                    
                    * {
                        margin: 0;
                        padding: 0;
                        box-sizing: border-box;
                    }
                    
                    body { 
                        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
                        background-color: var(--bg-color);
                        color: var(--text-color);
                        line-height: 1.6;
                        padding: 20px;
                        transition: background-color 0.3s ease;
                    }
                    
                    h1, h2 { 
                        color: var(--primary-color);
                        margin-bottom: 1rem;
                    }
                    
                    .container {
                        max-width: 1200px;
                        margin: 0 auto;
                    }
                    
                    .header {
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                        margin-bottom: 2rem;
                        flex-wrap: wrap;
                        gap: 1rem;
                    }
                    
                    .actions {
                        display: flex;
                        gap: 10px;
                    }
                    
                    .btn {
                        background-color: var(--primary-color);
                        color: white;
                        border: none;
                        padding: 10px 15px;
                        border-radius: var(--border-radius);
                        cursor: pointer;
                        font-weight: 500;
                        transition: all 0.2s ease;
                        text-decoration: none;
                        display: inline-block;
                    }
                    
                    .btn:hover {
                        background-color: var(--secondary-color);
                        transform: translateY(-2px);
                    }
                    
                    .card {
                        background-color: var(--card-bg);
                        border-radius: var(--border-radius);
                        box-shadow: var(--box-shadow);
                        padding: 20px;
                        margin-bottom: 20px;
                        transition: transform 0.3s ease, box-shadow 0.3s ease;
                    }
                    
                    .card:hover {
                        transform: translateY(-5px);
                        box-shadow: 0 8px 24px rgba(0,0,0,0.15);
                    }
                    
                    .image-container {
                        margin-top: 20px;
                        overflow: hidden;
                    }
                    
                    .image-preview {
                        width: 100%;
                        border-radius: var(--border-radius);
                        transition: transform 0.3s ease;
                    }
                    
                    .image-preview:hover {
                        transform: scale(1.01);
                    }
                    
                    .image-info {
                        margin-top: 15px;
                        display: grid;
                        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                        gap: 15px;
                    }
                    
                    .info-item {
                        padding: 10px;
                        background-color: rgba(67, 97, 238, 0.1);
                        border-radius: var(--border-radius);
                    }
                    
                    .info-label {
                        font-weight: bold;
                        color: var(--primary-color);
                        margin-bottom: 5px;
                    }
                    
                    .image-selector {
                        margin-bottom: 20px;
                    }
                    
                    select {
                        padding: 10px;
                        border-radius: var(--border-radius);
                        border: 1px solid #ddd;
                        background-color: var(--card-bg);
                        color: var(--text-color);
                        width: 100%;
                        max-width: 300px;
                    }
                    
                    .copy-btn {
                        background-color: var(--accent-color);
                    }
                    
                    .copy-btn:hover {
                        background-color: #d90166;
                    }
                    
                    .url-display {
                        padding: 10px;
                        background-color: rgba(0,0,0,0.05);
                        border-radius: var(--border-radius);
                        font-family: monospace;
                        word-break: break-all;
                        margin-top: 10px;
                    }
                    
                    @media (max-width: 768px) {
                        .header {
                            flex-direction: column;
                            align-items: flex-start;
                        }
                        
                        .image-info {
                            grid-template-columns: 1fr;
                        }
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>MCP Image Server</h1>
                        <div class="actions">
                            <button class="btn" onclick="location.reload()">Refresh</button>
                            <button class="btn copy-btn" onclick="copyImageUrl()">Copy URL</button>
                        </div>
                    </div>
                    
                    <div class="card">
                        <div class="image-selector">
                            <h2>Select an image</h2>
                            <select id="imageSelect" onchange="changeImage(this.value)">
                                {options_html}
                            </select>
                        </div>
                        
                        <div class="image-container">
                            <h2>Image preview</h2>
                            {image_preview}
                            
                            <div class="image-info">
                                <div class="info-item">
                                    <div class="info-label">Filename</div>
                                    <div>{selected_image}</div>
                                </div>
                                
                                <div class="info-item">
                                    <div class="info-label">Size</div>
                                    <div>{image_size:.2f} KB</div>
                                </div>
                                
                                <div class="info-item">
                                    <div class="info-label">Last modified</div>
                                    <div>{image_mtime}</div>
                                </div>
                                
                                <div class="info-item">
                                    <div class="info-label">Image URL</div>
                                    <div class="url-display" id="imageUrl">{image_url}</div>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="card">
                        <h2>How to use this image with Cascade</h2>
                        <p>To share this image with Cascade, you can:</p>
                        <ol style="margin-left: 20px; margin-top: 10px;">
                            <li>Copy the image URL by clicking the "Copy URL" button</li>
                            <li>Share the URL with Cascade in your conversation</li>
                            <li>Or use the generated Markdown file that already contains the embedded image</li>
                        </ol>
                    </div>
                </div>
                
                <script>
                    function changeImage(imageName) {
                        window.location.href = '/?image=' + encodeURIComponent(imageName);
                    }
                    
                    function copyImageUrl() {
                        const urlElement = document.getElementById('imageUrl');
                        const textArea = document.createElement('textarea');
                        textArea.value = urlElement.textContent;
                        document.body.appendChild(textArea);
                        textArea.select();
                        document.execCommand('copy');
                        document.body.removeChild(textArea);
                        
                        // Visual feedback
                        urlElement.style.backgroundColor = 'rgba(67, 97, 238, 0.2)';
                        setTimeout(() => {
                            urlElement.style.backgroundColor = 'rgba(0,0,0,0.05)';
                        }, 500);
                        
                        alert('URL copied to clipboard!');
                    }
                </script>
            </body>
            </html>
            """
            
            # Format the HTML with the dynamic values
            formatted_html = html_content.format(
                options_html=options_html,
                image_preview=image_preview,
                selected_image=selected_image,
                image_size=image_size,
                image_mtime=image_mtime,
                image_url=image_url
            )
            
            self.wfile.write(formatted_html.encode())
            return
        
        # For all other requests, use the default handler
        return super().do_GET()

def get_ip():
    """Get local IP address"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # No need for real connection
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def run_server(port=8080, directory=None, open_browser=True):
    """Start HTTP server"""
    if directory is None:
        directory = os.getcwd()
    
    # Check if port is available
    while True:
        try:
            server_address = ('', port)
            handler = lambda *args, **kwargs: ImageServer(*args, directory=directory, **kwargs)
            httpd = HTTPServer(server_address, handler)
            break
        except OSError:
            print(f"Port {port} is already in use. Trying port {port+1}...")
            port += 1
    
    ip = get_ip()
    print(f"Server started at http://{ip}:{port}")
    print(f"Base URL for images: http://{ip}:{port}/")
    print("Press Ctrl+C to stop the server")
    
    # Open browser
    if open_browser:
        webbrowser.open(f"http://localhost:{port}")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Server stopped")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MCP Image Server")
    parser.add_argument("-p", "--port", type=int, default=8080, help="Server port (default: 8080)")
    parser.add_argument("-d", "--directory", type=str, default=None, help="Directory containing images (default: current directory)")
    parser.add_argument("--no-browser", action="store_true", help="Don't open browser automatically")
    
    args = parser.parse_args()
    run_server(port=args.port, directory=args.directory, open_browser=not args.no_browser)
