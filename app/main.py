# File path: doc_intel_backend/app/main.py

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.routes import router

def create_application() -> FastAPI:
    """Factory function to create the FastAPI application."""
    
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        description="A Multi-Agent Document Intelligence Backend"
    )

    # CORS Middleware (Allows frontend to communicate if we build one later)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, specify domains
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include API Routes
    app.include_router(router, prefix=settings.API_PREFIX)

    return app

app = create_application()

if __name__ == "__main__":
    # This block allows running the file directly for debugging
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)