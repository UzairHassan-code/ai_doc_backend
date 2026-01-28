# File path: doc_intel_backend/app/core/config.py

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    PROJECT_NAME: str = "DocuMind AI Backend"
    VERSION: str = "1.0.0"
    API_PREFIX: str = "/api/v1"
    
    # Security
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY")

    # Paths (Using pathlib for cross-platform compatibility)
    # resolves to: doc_intel_backend/
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent 
    
    # Data Directories
    DATA_DIR: Path = BASE_DIR / "data"
    UPLOAD_DIR: Path = DATA_DIR / "uploads"
    VECTOR_STORE_DIR: Path = DATA_DIR / "vector_store"

    # Model Configuration
    EMBEDDING_MODEL_NAME: str = "all-MiniLM-L6-v2"

    def __init__(self):
        # Validate critical configuration
        if not self.GOOGLE_API_KEY:
            print("WARNING: GOOGLE_API_KEY is not set in .env file.")

        # Ensure necessary directories exist
        self.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
        self.VECTOR_STORE_DIR.mkdir(parents=True, exist_ok=True)

# Singleton instance
settings = Settings()