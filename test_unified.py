#!/usr/bin/env python3
"""
Simple unified mode test - creates a minimal frontend build for testing
"""

import os
import sys
from pathlib import Path

# Create a minimal HTML file that we can serve from the backend
def create_minimal_frontend():
    project_root = Path(__file__).parent
    frontend_dir = project_root / "frontend"
    build_dir = frontend_dir / "out"
    
    # Create build directory
    build_dir.mkdir(exist_ok=True)
    
    # Create a minimal index.html
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Suna - Unified Mode Test</title>
    <style>
        body { 
            font-family: system-ui, -apple-system, sans-serif; 
            margin: 0; 
            padding: 20px;
            background: #000;
            color: #fff;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }
        .container { 
            text-align: center; 
            max-width: 600px;
        }
        h1 { 
            color: #00ff88; 
            font-size: 3rem;
            margin-bottom: 1rem;
        }
        p { 
            font-size: 1.2rem;
            margin-bottom: 2rem;
            opacity: 0.8;
        }
        .success {
            background: #00ff88;
            color: #000;
            padding: 1rem 2rem;
            border-radius: 8px;
            display: inline-block;
            font-weight: bold;
            margin-bottom: 2rem;
        }
        .api-test {
            background: #333;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
        }
        button {
            background: #00ff88;
            color: #000;
            border: none;
            padding: 12px 24px;
            border-radius: 6px;
            font-size: 1rem;
            font-weight: bold;
            cursor: pointer;
            margin: 10px;
        }
        button:hover { background: #00cc6a; }
        #api-result { 
            margin-top: 15px; 
            padding: 10px;
            background: #222;
            border-radius: 4px;
            font-family: monospace;
            white-space: pre-wrap;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Suna Unified Mode</h1>
        <div class="success">✅ Frontend served from FastAPI Backend!</div>
        <p>This page is being served by the FastAPI backend on port 8000, demonstrating successful integration of frontend and backend into a single unified application.</p>
        
        <div class="api-test">
            <h3>API Connectivity Test</h3>
            <p>Test the API connection to verify everything is working:</p>
            <button onclick="testAPI()">Test API Health</button>
            <div id="api-result"></div>
        </div>
        
        <p><strong>🔗 Unified Mode Benefits:</strong></p>
        <ul style="text-align: left; display: inline-block;">
            <li>Single port deployment (8000)</li>
            <li>Simplified CORS configuration</li>
            <li>Reduced infrastructure complexity</li>
            <li>Faster API calls (same origin)</li>
            <li>Easier SSL/TLS configuration</li>
        </ul>
    </div>

    <script>
        async function testAPI() {
            const resultDiv = document.getElementById('api-result');
            resultDiv.textContent = 'Testing API connection...';
            
            try {
                const response = await fetch('/api/health');
                const data = await response.json();
                
                if (response.ok) {
                    resultDiv.textContent = `✅ API Health Check Success!
Status: ${data.status}
Instance: ${data.instance_id}
Timestamp: ${data.timestamp}`;
                    resultDiv.style.color = '#00ff88';
                } else {
                    throw new Error(`HTTP ${response.status}`);
                }
            } catch (error) {
                resultDiv.textContent = `❌ API Health Check Failed:
Error: ${error.message}

This might be expected if you're not running the full backend.`;
                resultDiv.style.color = '#ff6b6b';
            }
        }
        
        // Auto-test on load
        window.addEventListener('load', () => {
            setTimeout(testAPI, 1000);
        });
    </script>
</body>
</html>"""
    
    # Write the HTML file
    index_path = build_dir / "index.html"
    with open(index_path, 'w') as f:
        f.write(html_content)
    
    # Create _next directory structure for static assets
    next_dir = build_dir / "_next"
    next_dir.mkdir(exist_ok=True)
    static_dir = next_dir / "static" 
    static_dir.mkdir(exist_ok=True)
    
    print(f"✅ Created minimal frontend build at: {build_dir}")
    print(f"📄 Index file: {index_path}")
    return True

if __name__ == "__main__":
    create_minimal_frontend()
    print("\n🧪 Minimal unified mode build ready!")
    print("Now you can test unified mode by running:")
    print("  cd backend && UNIFIED_MODE=true python api.py")