# Unified Mode Integration - Implementation Guide

## Overview

This implementation merges the Next.js frontend and FastAPI backend into a single unified application that can be deployed and served from a single port (8000), while maintaining development flexibility.

## Implementation Details

### 1. Backend Changes (FastAPI)

#### Static File Serving
- **File**: `backend/api.py`
- **Key Changes**:
  - Added imports: `FileResponse`, `StaticFiles`
  - Added unified mode detection via `UNIFIED_MODE` environment variable
  - Added static file mounting for Next.js assets (`/_next/static`)
  - Added catch-all route handler for SPA routing
  - Serves `index.html` for client-side routing

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
            # Handle SPA routing logic...
```

### 2. Frontend Changes (Next.js)

#### Export Configuration
- **File**: `frontend/next.config.ts`
- **Key Changes**:
  - Added unified mode detection
  - Configured `output: 'export'` for static generation
  - Disabled rewrites in unified mode
  - Added image optimization settings for export

#### API Client Updates
- **File**: `frontend/src/lib/api-client.ts`
- **Key Changes**:
  - Added dynamic API URL detection
  - Uses same origin in unified mode
  - Falls back to environment variable in development

#### Environment Detection
- **File**: `frontend/src/lib/config.ts`
- **Added**: `isUnifiedMode()` function

### 3. Service Management

#### Service Manager Updates
- **File**: `service_manager.py`
- **Key Changes**:
  - Added unified mode detection from environment and .env files
  - Modified service startup logic to skip frontend in unified mode
  - Added frontend build validation
  - Updated status messages for unified deployment

#### Build System
- **File**: `build_unified.py`
- **Features**:
  - Automated frontend build in export mode
  - Environment variable configuration
  - Build validation and error handling
  - Backend environment updates

## Usage

### Development Mode (Separate Services)
```bash
# Traditional development with hot reloading
python start.py
```
- Frontend: http://localhost:3000
- Backend: http://localhost:8000

### Unified Mode (Single Service)
```bash
# Build frontend for unified deployment
python build_unified.py

# Start unified application
UNIFIED_MODE=true python start.py
```
- Unified App: http://localhost:8000 (serves both frontend and API)

### Manual Unified Mode
```bash
# 1. Build frontend
cd frontend
NEXT_OUTPUT=export UNIFIED_MODE=true npm run build

# 2. Start backend with unified mode
cd ../backend
UNIFIED_MODE=true python api.py
```

## Benefits

### Production Benefits
1. **Single Port Deployment**: Entire application runs on port 8000
2. **Simplified CORS**: No cross-origin requests needed
3. **Reduced Infrastructure**: One service instead of two
4. **Better Performance**: Faster API calls (same origin)
5. **SSL/TLS Simplicity**: Single certificate needed

### Development Benefits
1. **Flexible Development**: Keep separate services for hot reloading
2. **Easy Testing**: Quick switch between modes
3. **Minimal Changes**: Existing development workflow unchanged

## Technical Architecture

### Request Flow in Unified Mode
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

### File Structure in Unified Mode
```
backend/
├── api.py (serves both API and frontend)
└── ...

frontend/
├── out/ (built static files)
│   ├── index.html
│   ├── _next/static/... (assets)
│   └── ...
└── ...
```

## Environment Variables

### Required for Unified Mode
- `UNIFIED_MODE=true` - Enables unified mode
- `NEXT_OUTPUT=export` - For frontend build process
- `NEXT_PUBLIC_UNIFIED_MODE=true` - For frontend runtime

### Configuration Files
- `backend/.env`: Add `UNIFIED_MODE=true`
- `frontend/.env.local`: Add `NEXT_PUBLIC_UNIFIED_MODE=true`

## Limitations and Considerations

### Next.js Limitations in Export Mode
1. **API Routes**: Next.js API routes don't work with static export
   - Solution: Moved to FastAPI backend
2. **Server-Side Rendering**: Limited SSR capabilities
   - Solution: Client-side rendering for dynamic content
3. **Dynamic Routes**: Require `generateStaticParams()` for all routes
   - Solution: Generated empty params for SPA routing

### Development vs Production
- **Development**: Keep separate services for optimal DX
- **Production**: Use unified mode for simplified deployment

## Testing

### Test Unified Mode
```bash
# Create minimal test build
python test_unified.py

# Demo unified server (requires dependencies)
python demo_unified.py
```

## Next Steps

1. **Complete Static Export**: Fix remaining Next.js dynamic route issues
2. **Production Testing**: Test with full backend dependencies
3. **Documentation**: Update deployment guides
4. **CI/CD Integration**: Add unified build to deployment pipelines
5. **Performance Optimization**: Optimize static asset serving

## File Changes Summary

### Modified Files
- `backend/api.py` - Added static file serving
- `frontend/next.config.ts` - Export configuration
- `frontend/src/lib/api-client.ts` - Dynamic API URLs
- `frontend/src/lib/config.ts` - Environment detection
- `frontend/src/app/layout.tsx` - Font loading fixes
- `service_manager.py` - Unified mode support

### New Files
- `build_unified.py` - Build automation
- `test_unified.py` - Testing utilities
- `demo_unified.py` - Demonstration script

This implementation provides a solid foundation for unified deployment while maintaining development flexibility.