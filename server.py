#!/usr/bin/env python3
"""
Infinite Faces Web Server
Serves dynamically generated SVG faces based on URL parameters
Each unique URL generates a unique, deterministic face
"""

from flask import Flask, Response, render_template_string, request
import hashlib
import random
import string

# Import the generator
from generate_face import generate_svg

app = Flask(__name__)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Infinite Faces - URL-Based Generator</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }
        h1 {
            text-align: center;
            color: #333;
        }
        .explanation {
            background: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 30px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .highlight {
            background: #fff3cd;
            padding: 15px;
            border-left: 4px solid #ffc107;
            margin: 15px 0;
        }
        .gallery {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        .face-card {
            background: white;
            border-radius: 8px;
            padding: 15px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            text-align: center;
        }
        .face-card img {
            width: 100%;
            height: auto;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
        .seed-code {
            font-family: monospace;
            background: #f0f0f0;
            padding: 8px;
            border-radius: 4px;
            margin-top: 10px;
            font-size: 12px;
            word-break: break-all;
        }
        .url-display {
            background: #e8f5e9;
            padding: 10px;
            border-radius: 4px;
            margin-top: 5px;
            font-size: 11px;
            word-break: break-all;
            color: #2e7d32;
        }
        .controls {
            text-align: center;
            margin: 30px 0;
        }
        button {
            background: #4CAF50;
            color: white;
            border: none;
            padding: 12px 24px;
            font-size: 16px;
            border-radius: 4px;
            cursor: pointer;
            margin: 5px;
        }
        button:hover {
            background: #45a049;
        }
        code {
            background: #f0f0f0;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: monospace;
        }
        .success-box {
            background: #d4edda;
            border: 1px solid #c3e6cb;
            color: #155724;
            padding: 15px;
            border-radius: 4px;
            margin: 15px 0;
        }
    </style>
</head>
<body>
    <h1>🎨 Infinite Faces - URL-Based Generator</h1>
    
    <div class="explanation">
        <h2>The Solution: Dynamic Generation with URL Parameters</h2>
        <p>This is a <strong>single Python script</strong> that generates infinite unique SVG faces based on URL parameters - no JavaScript in the SVG itself!</p>
        
        <div class="highlight">
            <strong>How it works:</strong>
            <ol>
                <li>Each face is accessed via: <code>/face.svg?seed=YOUR_UNIQUE_SEED</code></li>
                <li>The seed is hashed deterministically to select components</li>
                <li>The server generates a pure static SVG (no JS needed)</li>
                <li>Same seed = same face, always</li>
                <li>Different seed = different face</li>
            </ol>
        </div>
        
        <div class="success-box">
            <strong>✅ This solves the JavaScript stripping problem!</strong>
            <ul>
                <li>The SVG itself contains NO JavaScript - it's pure static SVG</li>
                <li>Works as <code>&lt;img&gt;</code> tag anywhere</li>
                <li>Can be embedded in email, social media, WordPress, etc.</li>
                <li>Each unique URL generates a unique face</li>
            </ul>
        </div>
        
        <p><strong>To share a face:</strong> Copy the URL with its seed parameter. Anyone accessing that URL gets the same face!</p>
    </div>

    <div class="controls">
        <button onclick="generateRandomFaces()">Generate 12 Random Faces</button>
        <button onclick="generateFromText()">Generate from Custom Text</button>
    </div>

    <div class="gallery" id="gallery"></div>

    <script>
        function randomSeed() {
            return Math.random().toString(36).substring(2, 15);
        }
        
        function createFaceCard(seed, index) {
            const card = document.createElement('div');
            card.className = 'face-card';
            
            const img = document.createElement('img');
            const url = `/face.svg?seed=${encodeURIComponent(seed)}`;
            img.src = url;
            img.alt = `Face ${index}`;
            
            const seedDiv = document.createElement('div');
            seedDiv.className = 'seed-code';
            seedDiv.textContent = `Seed: ${seed}`;
            
            const urlDiv = document.createElement('div');
            urlDiv.className = 'url-display';
            urlDiv.textContent = window.location.origin + url;
            
            card.appendChild(img);
            card.appendChild(seedDiv);
            card.appendChild(urlDiv);
            return card;
        }
        
        function generateRandomFaces() {
            const gallery = document.getElementById('gallery');
            gallery.innerHTML = '';
            
            for (let i = 0; i < 12; i++) {
                const seed = randomSeed();
                gallery.appendChild(createFaceCard(seed, i + 1));
            }
        }
        
        function generateFromText() {
            const text = prompt('Enter any text to generate a face (name, phrase, random string, etc.):');
            if (text && text.trim()) {
                const gallery = document.getElementById('gallery');
                gallery.innerHTML = '';
                gallery.appendChild(createFaceCard(text.trim(), 1));
            }
        }
        
        // Generate initial faces
        generateRandomFaces();
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    """Main page with gallery"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/face.svg')
def serve_face():
    """Generate and serve a unique SVG face based on seed parameter"""
    seed = request.args.get('seed', 'default')
    svg_content = generate_svg(seed)
    return Response(svg_content, mimetype='image/svg+xml')

@app.route('/random')
def random_face():
    """Redirect to a random face"""
    random_seed = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Random Face</title>
        <style>
            body {{
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                background: #f5f5f5;
                font-family: Arial, sans-serif;
            }}
            .container {{
                text-align: center;
            }}
            img {{
                max-width: 400px;
                border: 2px solid #333;
                border-radius: 8px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }}
            .info {{
                margin-top: 20px;
                background: white;
                padding: 15px;
                border-radius: 8px;
            }}
            code {{
                background: #f0f0f0;
                padding: 4px 8px;
                border-radius: 4px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <img src="/face.svg?seed={random_seed}" alt="Random Face">
            <div class="info">
                <p><strong>Seed:</strong> <code>{random_seed}</code></p>
                <p><strong>URL:</strong><br><code>{request.host_url}face.svg?seed={random_seed}</code></p>
                <p><a href="/random">Generate Another Random Face</a> | <a href="/">Back to Gallery</a></p>
            </div>
        </div>
    </body>
    </html>
    '''

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    print("🎨 Infinite Faces Server Starting...")
    print(f"📍 Server will run on port: {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
