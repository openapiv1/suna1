#!/usr/bin/env python3
"""
Unified Mode Validation Script
Validates that all components for unified deployment are correctly configured
"""

import os
from pathlib import Path

def validate_unified_mode():
    """Validate unified mode implementation"""
    project_root = Path(__file__).parent
    errors = []
    warnings = []
    success = []
    
    print("🔍 Validating Unified Mode Implementation...\n")
    
    # Check backend modifications
    backend_api = project_root / "backend" / "api.py"
    if backend_api.exists():
        with open(backend_api) as f:
            content = f.read()
            if "UNIFIED_MODE" in content:
                success.append("✅ Backend has unified mode support")
            else:
                errors.append("❌ Backend missing unified mode code")
                
            if "StaticFiles" in content:
                success.append("✅ Backend can serve static files")
            else:
                errors.append("❌ Backend missing static file serving")
    else:
        errors.append("❌ Backend API file not found")
    
    # Check frontend configuration
    frontend_config = project_root / "frontend" / "next.config.ts"
    if frontend_config.exists():
        with open(frontend_config) as f:
            content = f.read()
            if "export" in content and "UNIFIED_MODE" in content:
                success.append("✅ Frontend configured for static export")
            else:
                warnings.append("⚠️ Frontend may need export configuration")
    else:
        warnings.append("⚠️ Frontend config not found")
    
    # Check API client updates
    api_client = project_root / "frontend" / "src" / "lib" / "api-client.ts"
    if api_client.exists():
        with open(api_client) as f:
            content = f.read()
            if "isUnifiedMode" in content:
                success.append("✅ API client supports unified mode")
            else:
                warnings.append("⚠️ API client may need unified mode support")
    else:
        warnings.append("⚠️ API client not found")
    
    # Check service manager
    service_manager = project_root / "service_manager.py"
    if service_manager.exists():
        with open(service_manager) as f:
            content = f.read()
            if "unified_mode" in content:
                success.append("✅ Service manager supports unified mode")
            else:
                warnings.append("⚠️ Service manager may need unified mode support")
    else:
        warnings.append("⚠️ Service manager not found")
    
    # Check build tools
    build_script = project_root / "build_unified.py"
    if build_script.exists():
        success.append("✅ Unified build script available")
    else:
        warnings.append("⚠️ Build script not found")
    
    # Check frontend build
    frontend_build = project_root / "frontend" / "out"
    if frontend_build.exists():
        index_file = frontend_build / "index.html"
        if index_file.exists():
            success.append("✅ Frontend build exists and ready")
        else:
            warnings.append("⚠️ Frontend build incomplete")
    else:
        warnings.append("⚠️ No frontend build found (run build_unified.py)")
    
    # Print results
    print("📊 Validation Results:")
    print("=" * 50)
    
    if success:
        print("\n✅ Successful Checks:")
        for item in success:
            print(f"  {item}")
    
    if warnings:
        print("\n⚠️ Warnings:")
        for item in warnings:
            print(f"  {item}")
    
    if errors:
        print("\n❌ Errors:")
        for item in errors:
            print(f"  {item}")
    
    # Summary
    print(f"\n📈 Summary:")
    print(f"  ✅ Success: {len(success)}")
    print(f"  ⚠️ Warnings: {len(warnings)}")
    print(f"  ❌ Errors: {len(errors)}")
    
    if errors:
        print(f"\n🚨 Unified mode has critical issues that need to be resolved.")
        return False
    elif warnings:
        print(f"\n⚠️ Unified mode is mostly ready but may need attention to warnings.")
        return True
    else:
        print(f"\n🎉 Unified mode is fully implemented and ready!")
        return True

def print_usage_guide():
    """Print usage guide for unified mode"""
    print("\n" + "=" * 60)
    print("🚀 HOW TO USE UNIFIED MODE")
    print("=" * 60)
    
    print("\n1. 📦 Build Frontend (if needed):")
    print("   python build_unified.py")
    print("   # OR create test build: python test_unified.py")
    
    print("\n2. 🔧 Configure Environment:")
    print("   echo 'UNIFIED_MODE=true' >> backend/.env")
    
    print("\n3. 🚀 Start Unified Application:")
    print("   UNIFIED_MODE=true python start.py")
    print("   # OR manually: cd backend && UNIFIED_MODE=true python api.py")
    
    print("\n4. 🌐 Access Application:")
    print("   Frontend: http://localhost:8000")
    print("   API: http://localhost:8000/api")
    
    print("\n5. 🔄 Development Mode (separate services):")
    print("   python start.py  # (without UNIFIED_MODE)")
    
    print("\n📋 Benefits:")
    print("  • Single port deployment")
    print("  • Simplified CORS configuration") 
    print("  • Reduced infrastructure complexity")
    print("  • Faster API calls (same origin)")

if __name__ == "__main__":
    is_ready = validate_unified_mode()
    
    if is_ready:
        print_usage_guide()
    else:
        print("\n🔧 Please address the errors above before using unified mode.")