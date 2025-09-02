#!/usr/bin/env python3
"""
Minimal unified mode demonstration
Shows FastAPI serving static frontend files
"""

try:
    from fastapi import FastAPI, Request
    from fastapi.staticfiles import StaticFiles
    from fastapi.responses import FileResponse, JSONResponse
    import uvicorn
    from pathlib import Path
    from datetime import datetime
    
    # Create FastAPI app
    app = FastAPI(title="Suna Unified Mode Demo")
    
    # Path to frontend build
    frontend_build_path = Path(__file__).parent / "frontend" / "out"
    
    print(f"🔍 Looking for frontend build at: {frontend_build_path}")
    
    if frontend_build_path.exists():
        print("✅ Frontend build found!")
        
        # Mount static assets
        if (frontend_build_path / "_next").exists():
            app.mount("/_next", StaticFiles(directory=str(frontend_build_path / "_next")), name="next")
            print("📦 Mounted Next.js static assets")
        
        # API routes
        @app.get("/api/health")
        async def health_check():
            return JSONResponse({
                "status": "healthy",
                "service": "unified-suna",
                "mode": "unified",
                "timestamp": datetime.now().isoformat(),
                "message": "🚀 Frontend and Backend unified successfully!"
            })
        
        # Catch-all for frontend SPA
        @app.get("/{full_path:path}")
        async def serve_frontend(full_path: str):
            """Serve frontend files and handle SPA routing"""
            # Skip API routes
            if full_path.startswith("api/"):
                return JSONResponse({"error": "API route not found"}, status_code=404)
            
            # Try to serve the exact file first
            file_path = frontend_build_path / full_path
            if file_path.is_file():
                return FileResponse(file_path)
            
            # Try with .html extension
            html_path = frontend_build_path / f"{full_path}.html"
            if html_path.is_file():
                return FileResponse(html_path)
            
            # For all other routes, serve index.html (SPA routing)
            index_path = frontend_build_path / "index.html"
            if index_path.is_file():
                return FileResponse(index_path)
            
            return JSONResponse({"error": "Page not found"}, status_code=404)
        
        print("🌐 Starting Unified Suna Server...")
        print("🔗 Frontend and Backend served from: http://localhost:8000")
        print("📡 API available at: http://localhost:8000/api/health")
        print("🛑 Press Ctrl+C to stop")
        
        # Start server
        uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
        
    else:
        print("❌ Frontend build not found!")
        print("💡 Run 'python test_unified.py' first to create a test build")

except ImportError as e:
    print(f"❌ Missing dependency: {e}")
    print("💡 This is a minimal demo. The full backend has more dependencies.")
    print("🔧 For full functionality, use the actual backend with proper setup.")

except KeyboardInterrupt:
    print("\n🛑 Server stopped by user")

except Exception as e:
    print(f"❌ Error: {e}")