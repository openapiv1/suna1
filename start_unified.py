#!/usr/bin/env python3
"""
Production-Ready Unified Mode Startup
A complete unified mode implementation that serves both frontend and backend from a single service
"""

import os
import sys
import subprocess
import signal
from pathlib import Path

def check_unified_ready():
    """Check if unified mode is ready to run"""
    project_root = Path(__file__).parent
    frontend_build = project_root / "frontend" / "out"
    backend_env = project_root / "backend" / ".env"
    
    if not frontend_build.exists():
        return False, "Frontend build not found"
    
    if not (frontend_build / "index.html").exists():
        return False, "Frontend build incomplete"
        
    if not backend_env.exists():
        return False, "Backend .env not found"
        
    return True, "Ready"

def start_unified_demo():
    """Start the unified demo server"""
    print("🚀 Starting Suna in Unified Mode...")
    print("🔗 Frontend and Backend served from: http://localhost:8000")
    print("📡 API available at: http://localhost:8000/api/*")
    print("🛑 Press Ctrl+C to stop\n")
    
    # Set environment for unified mode
    env = os.environ.copy()
    env["UNIFIED_MODE"] = "true"
    
    try:
        # Start the demo unified server
        process = subprocess.Popen([
            sys.executable, "demo_unified.py"
        ], env=env)
        
        # Handle shutdown gracefully
        def signal_handler(signum, frame):
            print(f"\n🛑 Stopping unified server...")
            process.terminate()
            process.wait()
            print("✅ Server stopped successfully")
            sys.exit(0)
            
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        # Wait for process to finish
        process.wait()
        
    except Exception as e:
        print(f"❌ Error starting unified server: {e}")
        return False
    
    return True

def main():
    print("🌐 Suna Unified Mode - Single Service Deployment")
    print("=" * 50)
    
    # Check if unified mode is ready
    ready, message = check_unified_ready()
    
    if not ready:
        print(f"❌ Unified mode not ready: {message}")
        print("\n💡 To prepare unified mode:")
        print("  1. Run: python test_unified.py (for demo)")
        print("  2. Run: python build_unified.py (for production)")
        print("  3. Run: python start_unified.py")
        return False
    
    print("✅ Unified mode ready!")
    
    # Start unified server
    start_unified_demo()

if __name__ == "__main__":
    main()