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
        # Gestion des requêtes GET
        if self.path == '/' or self.path.startswith('/?'):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            # Liste des images disponibles
            images = [f for f in os.listdir(self.directory) if f.endswith(('.png', '.jpg', '.jpeg', '.gif'))]
            
            # Obtenir l'image sélectionnée ou utiliser screenshot.png par défaut
            query_components = parse_qs(urlparse(self.path).query)
            selected_image = query_components.get('image', ['screenshot.png'])[0]
            
            # Vérifier si l'image existe
            image_path = os.path.join(self.directory, selected_image)
            image_exists = os.path.exists(image_path)
            
            # Obtenir les informations sur l'image
            if image_exists:
                image_size = os.path.getsize(image_path) / 1024  # Taille en Ko
                image_mtime = datetime.fromtimestamp(os.path.getmtime(image_path)).strftime('%Y-%m-%d %H:%M:%S')
            else:
                image_size = 0
                image_mtime = 'N/A'
            
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Serveur d'images MCP</title>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <style>
                    :root {{
                        --primary-color: #4361ee;
                        --secondary-color: #3a0ca3;
                        --accent-color: #f72585;
                        --bg-color: #f8f9fa;
                        --text-color: #2b2d42;
                        --card-bg: #ffffff;
                        --border-radius: 8px;
                        --box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                    }}
                    
                    @media (prefers-color-scheme: dark) {{
                        :root {{
                            --bg-color: #121212;
                            --text-color: #e0e0e0;
                            --card-bg: #1e1e1e;
                            --box-shadow: 0 4px 12px rgba(0,0,0,0.3);
                        }}
                    }}
                    
                    * {{
                        margin: 0;
                        padding: 0;
                        box-sizing: border-box;
                    }}
                    
                    body {{ 
                        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
                        background-color: var(--bg-color);
                        color: var(--text-color);
                        line-height: 1.6;
                        padding: 20px;
                        transition: background-color 0.3s ease;
                    }}
                    
                    h1, h2 {{ 
                        color: var(--primary-color);
                        margin-bottom: 1rem;
                    }}
                    
                    .container {{
                        max-width: 1200px;
                        margin: 0 auto;
                    }}
                    
                    .header {{
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                        margin-bottom: 2rem;
                        flex-wrap: wrap;
                        gap: 1rem;
                    }}
                    
                    .actions {{
                        display: flex;
                        gap: 10px;
                    }}
                    
                    .btn {{
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
                    }}
                    
                    .btn:hover {{
                        background-color: var(--secondary-color);
                        transform: translateY(-2px);
                    }}
                    
                    .card {{
                        background-color: var(--card-bg);
                        border-radius: var(--border-radius);
                        box-shadow: var(--box-shadow);
                        padding: 20px;
                        margin-bottom: 20px;
                        transition: transform 0.3s ease, box-shadow 0.3s ease;
                    }}
                    
                    .card:hover {{
                        transform: translateY(-5px);
                        box-shadow: 0 8px 24px rgba(0,0,0,0.15);
                    }}
                    
                    .image-container {{
                        margin-top: 20px;
                        overflow: hidden;
                    }}
                    
                    .image-preview {{
                        width: 100%;
                        border-radius: var(--border-radius);
                        transition: transform 0.3s ease;
                    }}
                    
                    .image-preview:hover {{
                        transform: scale(1.01);
                    }}
                    
                    .image-info {{
                        margin-top: 15px;
                        display: grid;
                        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                        gap: 15px;
                    }}
                    
                    .info-item {{
                        padding: 10px;
                        background-color: rgba(67, 97, 238, 0.1);
                        border-radius: var(--border-radius);
                    }}
                    
                    .info-label {{
                        font-weight: bold;
                        color: var(--primary-color);
                        margin-bottom: 5px;
                    }}
                    
                    .image-selector {{
                        margin-bottom: 20px;
                    }}
                    
                    select {{
                        padding: 10px;
                        border-radius: var(--border-radius);
                        border: 1px solid #ddd;
                        background-color: var(--card-bg);
                        color: var(--text-color);
                        width: 100%;
                        max-width: 300px;
                    }}
                    
                    .copy-btn {{
                        background-color: var(--accent-color);
                    }}
                    
                    .copy-btn:hover {{
                        background-color: #d90166;
                    }}
                    
                    .url-display {{
                        padding: 10px;
                        background-color: rgba(0,0,0,0.05);
                        border-radius: var(--border-radius);
                        font-family: monospace;
                        word-break: break-all;
                        margin-top: 10px;
                    }}
                    
                    @media (max-width: 768px) {{
                        .header {{
                            flex-direction: column;
                            align-items: flex-start;
                        }}
                        
                        .image-info {{
                            grid-template-columns: 1fr;
                        }}
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>Serveur d'images MCP</h1>
                        <div class="actions">
                            <button class="btn" onclick="location.reload()">Rafraîchir</button>
                            <button class="btn copy-btn" onclick="copyImageUrl()">Copier l'URL</button>
                        </div>
                    </div>
                    
                    <div class="card">
                        <div class="image-selector">
                            <h2>Sélectionner une image</h2>
                            <select id="imageSelect" onchange="changeImage(this.value)">
                                {
                                    ''.join([f'<option value="{img}" {"selected" if img == selected_image else ""}>{img}</option>' for img in images])
                                }
                            </select>
                        </div>
                        
                        <div class="image-container">
                            <h2>Aperçu de l'image</h2>
                            {
                                f'<img class="image-preview" src="/{selected_image}?t={os.path.getmtime(image_path) if image_exists else "0"}" alt="Image preview">'
                                if image_exists else
                                '<p>L\'image sélectionnée n\'existe pas.</p>'
                            }
                            
                            <div class="image-info">
                                <div class="info-item">
                                    <div class="info-label">Nom du fichier</div>
                                    <div>{selected_image}</div>
                                </div>
                                
                                <div class="info-item">
                                    <div class="info-label">Taille</div>
                                    <div>{image_size:.2f} Ko</div>
                                </div>
                                
                                <div class="info-item">
                                    <div class="info-label">Dernière modification</div>
                                    <div>{image_mtime}</div>
                                </div>
                                
                                <div class="info-item">
                                    <div class="info-label">URL de l'image</div>
                                    <div class="url-display" id="imageUrl">http://{self.server.server_address[0]}:{self.server.server_address[1]}/{selected_image}</div>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="card">
                        <h2>Comment utiliser cette image avec Cascade</h2>
                        <p>Pour partager cette image avec Cascade, vous pouvez:</p>
                        <ol style="margin-left: 20px; margin-top: 10px;">
                            <li>Copier l'URL de l'image en cliquant sur le bouton "Copier l'URL"</li>
                            <li>Partager l'URL avec Cascade dans votre conversation</li>
                            <li>Ou utiliser le fichier Markdown généré qui contient déjà l'image intégrée</li>
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
                        
                        // Feedback visuel
                        urlElement.style.backgroundColor = 'rgba(67, 97, 238, 0.2)';
                        setTimeout(() => {
                            urlElement.style.backgroundColor = 'rgba(0,0,0,0.05)';
                        }, 500);
                        
                        alert('URL copiée dans le presse-papier!');
                    }
                </script>
            </body>
            </html>
            """
            
            self.wfile.write(html_content.encode())
            return
        
        # Pour toutes les autres requêtes, utiliser le gestionnaire par défaut
        return super().do_GET()

def get_ip():
    """Obtenir l'adresse IP locale"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Pas besoin de connexion réelle
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def run_server(port=8080, directory=None, open_browser=True):
    """Démarrer le serveur HTTP"""
    if directory is None:
        directory = os.getcwd()
    
    # Vérifier si le port est disponible
    while True:
        try:
            server_address = ('', port)
            handler = lambda *args, **kwargs: ImageServer(*args, directory=directory, **kwargs)
            httpd = HTTPServer(server_address, handler)
            break
        except OSError:
            print(f"Le port {port} est déjà utilisé. Essai avec le port {port+1}...")
            port += 1
    
    ip = get_ip()
    print(f"Serveur démarré sur http://{ip}:{port}")
    print(f"URL de base pour les images: http://{ip}:{port}/")
    print("Appuyez sur Ctrl+C pour arrêter le serveur")
    
    # Ouvrir le navigateur
    if open_browser:
        webbrowser.open(f"http://localhost:{port}")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Serveur arrêté")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Serveur d'images MCP")
    parser.add_argument("-p", "--port", type=int, default=8080, help="Port du serveur (défaut: 8080)")
    parser.add_argument("-d", "--directory", type=str, default=None, help="Répertoire contenant les images (défaut: répertoire courant)")
    parser.add_argument("--no-browser", action="store_true", help="Ne pas ouvrir le navigateur automatiquement")
    
    args = parser.parse_args()
    run_server(port=args.port, directory=args.directory, open_browser=not args.no_browser)
