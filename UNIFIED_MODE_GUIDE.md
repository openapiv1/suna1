# Suna Unified Mode - Complete Implementation Guide

## 🚀 Overview

Unified Mode successfully integrates the Suna frontend and backend into a **single service** running on port 8000, eliminating the need for separate services on ports 3000 and 8000.

![Suna Unified Mode Demo](https://github.com/user-attachments/assets/d78908a1-9322-4076-866c-ebab18f5df60)

## ✅ Implementation Status: **COMPLETE**

### What's Implemented:
- ✅ **Single Port Deployment**: Everything runs on http://localhost:8000
- ✅ **Static File Serving**: FastAPI serves frontend assets from `/frontend/out`
- ✅ **API Integration**: Backend API available at `/api/*` endpoints
- ✅ **SPA Routing**: Client-side routing handled correctly
- ✅ **Auto-Detection**: Service manager automatically enables unified mode
- ✅ **Backward Compatibility**: Falls back to separate services when needed

## 🎯 Benefits Achieved

| Feature | Before (Separate) | After (Unified) |
|---------|-------------------|-----------------|
| **Ports** | Frontend: 3000<br>Backend: 8000 | Single: 8000 |
| **CORS** | Cross-origin requests | Same-origin requests |
| **Infrastructure** | 2 services to manage | 1 service to manage |
| **SSL/TLS** | 2 certificates needed | 1 certificate needed |
| **API Latency** | Network overhead | Direct calls |
| **Deployment** | Complex orchestration | Simple single service |

## 🛠 Quick Start

### Option 1: Automatic Unified Mode (Recommended)
```bash
# Creates minimal frontend build and starts unified server
python test_unified.py
python start_unified.py
```

### Option 2: Production Build
```bash
# Full Next.js build for production
python build_unified.py
python start_unified.py
```

### Option 3: Manual Control
```bash
# Start with environment variable
UNIFIED_MODE=true python start.py
```

## 📁 File Structure (Unified Mode)

```
project/
├── backend/
│   ├── api.py                 # FastAPI server with unified mode support
│   └── .env                   # UNIFIED_MODE=true
├── frontend/
│   └── out/                   # Built static files served by backend
│       ├── index.html
│       └── _next/static/...
├── start_unified.py           # Simple unified startup
├── test_unified.py            # Creates minimal build
└── build_unified.py          # Full production build
```

## 🔧 Configuration Files

### Backend Configuration (`backend/.env`)
```env
# Enable unified mode
UNIFIED_MODE=true

# Environment settings
ENV_MODE=local
REDIS_HOST=localhost
REDIS_PORT=6379

# URLs for unified mode
WEBHOOK_BASE_URL=http://localhost:8000
FRONTEND_URL=http://localhost:8000
```

### Key Code Changes

#### 1. Backend API Server (`backend/api.py`)
```python
# Unified Mode: Serve frontend static files from backend
UNIFIED_MODE = os.getenv("UNIFIED_MODE", "false").lower() == "true"
if UNIFIED_MODE:
    frontend_build_path = Path(__file__).parent.parent / "frontend" / "out"
    
    if frontend_build_path.exists():
        # Mount static assets
        app.mount("/_next", StaticFiles(directory=str(frontend_build_path / "_next")), name="next")
        
        # Catch-all route for frontend SPA routing
        @app.get("/{full_path:path}")
        async def serve_frontend(full_path: str):
            # Skip API routes, serve static files, handle SPA routing
```

#### 2. Service Manager (`service_manager.py`)
```python
def start_all_services(self) -> bool:
    if self.unified_mode:
        # Start backend only, skip separate frontend
        # Backend serves both API and frontend files
    else:
        # Start both backend and frontend separately
```

#### 3. Auto-Detection (`start.py`)
```python
# Auto-enable unified mode if frontend build exists
if not manager.unified_mode and manager.check_frontend_build_exists():
    print("🔍 Frontend build detected. Enabling unified mode automatically...")
    manager.unified_mode = True
```

## 🌐 Request Flow (Unified Mode)

```
Browser Request → FastAPI Server (Port 8000)
                      ↓
                 Route Analysis
                      ↓
    ┌─────────────────┼─────────────────┐
    ↓                 ↓                 ↓
API Routes       Static Assets     SPA Routes
(/api/*)         (/_next/*)        (everything else)
    ↓                 ↓                 ↓
FastAPI          StaticFiles       index.html
Handlers         Middleware        (React Router)
```

## 📊 Validation Results

```bash
$ python validate_unified.py

🔍 Validating Unified Mode Implementation...

📊 Validation Results:
==================================================

✅ Successful Checks:
  ✅ Backend has unified mode support
  ✅ Backend can serve static files
  ✅ Frontend configured for static export
  ✅ API client supports unified mode
  ✅ Service manager supports unified mode
  ✅ Unified build script available
  ✅ Frontend build exists and ready

📈 Summary:
  ✅ Success: 7
  ⚠️ Warnings: 0
  ❌ Errors: 0

🎉 Unified mode is fully implemented and ready!
```

## 🧪 Testing

### Manual Testing
1. **Start Unified Server**: `python start_unified.py`
2. **Access Frontend**: http://localhost:8000
3. **Test API**: http://localhost:8000/api/health
4. **Verify Single Service**: Only port 8000 in use

### API Health Check Response
```json
{
  "status": "healthy",
  "service": "unified-suna",
  "mode": "unified",
  "timestamp": "2025-09-02T20:17:48.779792",
  "message": "🚀 Frontend and Backend unified successfully!"
}
```

## 🔄 Development vs Production

### Development Mode (Separate Services)
```bash
# Traditional development with hot reloading
python start.py  # (without unified mode)
```
- Frontend: http://localhost:3000 (hot reload)
- Backend: http://localhost:8000 (API only)

### Production Mode (Unified)
```bash
# Single service deployment
python build_unified.py  # Build production assets
python start_unified.py  # Start unified server
```
- Unified: http://localhost:8000 (both frontend & API)

## 🚀 Deployment Ready

The unified mode implementation is **production-ready** and provides:

1. **Simplified Deployment**: Single service to deploy
2. **Reduced Resource Usage**: One process instead of two
3. **Better Performance**: No cross-origin request overhead
4. **Easier Scaling**: Scale one service instead of coordinating two
5. **Simplified Monitoring**: Single service to monitor
6. **Cost Reduction**: Fewer infrastructure resources needed

## 📚 Additional Resources

- `UNIFIED_MODE.md` - Original technical specification
- `demo_unified.py` - Minimal working demo
- `build_unified.py` - Full production build script
- `validate_unified.py` - Validation and status checker

## 🎉 Success Metrics

- **✅ Problem Solved**: No more separate localhost:3000 and localhost:8000
- **✅ Single Service**: Everything on port 8000
- **✅ Working Demo**: Live, functional implementation
- **✅ Auto-Detection**: Automatically enables when possible
- **✅ Backward Compatible**: Falls back to separate services
- **✅ Production Ready**: Complete implementation with proper error handling