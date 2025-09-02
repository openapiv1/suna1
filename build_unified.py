#!/usr/bin/env python3
"""
Build script for unified frontend-backend deployment
Builds the Next.js frontend in export mode and prepares for serving from FastAPI backend
"""

import os
import sys
import subprocess
import shutil
import platform
from pathlib import Path

IS_WINDOWS = platform.system() == "Windows"

class Colors:
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"

def print_info(message: str):
    print(f"{Colors.BLUE}ℹ️  {message}{Colors.ENDC}")

def print_success(message: str):
    print(f"{Colors.GREEN}✅  {message}{Colors.ENDC}")

def print_warning(message: str):
    print(f"{Colors.YELLOW}⚠️  {message}{Colors.ENDC}")

def print_error(message: str):
    print(f"{Colors.RED}❌  {message}{Colors.ENDC}")

def run_command(cmd: list, cwd: str = None, env: dict = None) -> bool:
    """Run a command and return success status"""
    try:
        print_info(f"Running: {' '.join(cmd)}")
        result = subprocess.run(
            cmd, 
            cwd=cwd, 
            shell=IS_WINDOWS, 
            check=True,
            env=env or os.environ
        )
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"Command failed: {' '.join(cmd)}")
        print_error(f"Error: {e}")
        return False

def main():
    print(f"\n{Colors.BOLD}{Colors.BLUE}🏗️  Building Unified Suna Application{Colors.ENDC}\n")
    
    project_root = Path(__file__).parent.absolute()
    frontend_dir = project_root / "frontend"
    backend_dir = project_root / "backend"
    build_dir = frontend_dir / "out"
    
    print_info(f"Project root: {project_root}")
    print_info(f"Frontend directory: {frontend_dir}")
    print_info(f"Backend directory: {backend_dir}")
    
    # Verify directories exist
    if not frontend_dir.exists():
        print_error("Frontend directory not found!")
        return False
    
    if not backend_dir.exists():
        print_error("Backend directory not found!")
        return False
    
    # Clean previous build
    if build_dir.exists():
        print_info("Cleaning previous build...")
        shutil.rmtree(build_dir)
    
    # Step 1: Install frontend dependencies
    print_info("Installing frontend dependencies...")
    if not run_command(["npm", "install"], cwd=str(frontend_dir)):
        return False
    
    # Step 2: Build frontend in export mode
    print_info("Building frontend in export mode...")
    build_env = os.environ.copy()
    build_env["NEXT_OUTPUT"] = "export"
    build_env["UNIFIED_MODE"] = "true"
    
    if not run_command(["npm", "run", "build"], cwd=str(frontend_dir), env=build_env):
        return False
    
    # Step 3: Verify build output
    if not build_dir.exists():
        print_error("Build directory not created!")
        return False
    
    index_file = build_dir / "index.html"
    if not index_file.exists():
        print_error("index.html not found in build output!")
        return False
    
    print_success("Frontend build completed successfully!")
    print_info(f"Build output location: {build_dir}")
    
    # Step 4: Create unified startup script
    print_info("Creating unified startup configuration...")
    
    # Update backend environment for unified mode
    backend_env_path = backend_dir / ".env"
    if backend_env_path.exists():
        # Read existing .env file
        with open(backend_env_path, 'r') as f:
            env_content = f.read()
        
        # Add or update UNIFIED_MODE
        if "UNIFIED_MODE=" in env_content:
            # Replace existing setting
            lines = env_content.split('\n')
            updated_lines = []
            for line in lines:
                if line.startswith("UNIFIED_MODE="):
                    updated_lines.append("UNIFIED_MODE=true")
                else:
                    updated_lines.append(line)
            env_content = '\n'.join(updated_lines)
        else:
            # Add new setting
            env_content += "\n# Unified mode - serve frontend from backend\nUNIFIED_MODE=true\n"
        
        with open(backend_env_path, 'w') as f:
            f.write(env_content)
        
        print_success("Backend environment updated for unified mode")
    else:
        print_warning("Backend .env file not found - you may need to run setup first")
    
    # Summary
    print(f"\n{Colors.GREEN}{Colors.BOLD}✨ Unified Build Complete! ✨{Colors.ENDC}\n")
    print_info("Your application is now ready for unified deployment.")
    print_info("The frontend will be served from the backend on port 8000.")
    print_info("\nTo start the unified application:")
    print_info("  cd backend && python api.py")
    print_info("\nOr use the service manager:")
    print_info("  python start.py")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)