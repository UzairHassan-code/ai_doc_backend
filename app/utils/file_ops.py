# File path: doc_intel_backend/app/utils/file_ops.py

import shutil
import uuid
from pathlib import Path
from fastapi import UploadFile, HTTPException
from app.core.config import settings

ALLOWED_CONTENT_TYPES = ["application/pdf", "image/png", "image/jpeg", "image/jpg"]

async def save_upload_file(file: UploadFile) -> tuple[str, str]:
    """
    Validates and saves an uploaded file to the local disk.
    
    Args:
        file: The uploaded file object from FastAPI.
        
    Returns:
        tuple: (unique_file_id, absolute_file_path)
    
    Raises:
        HTTPException: If file type is invalid or save fails.
    """
    
    # 1. Validate File Type
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid file type: {file.content_type}. Allowed: PDF, PNG, JPEG."
        )

    # 2. Generate Unique Filename
    # We use UUID to prevent filename collisions
    file_extension = Path(file.filename).suffix
    if not file_extension:
        # Fallback if no extension provided
        file_extension = ".pdf" if file.content_type == "application/pdf" else ".png"
        
    file_id = str(uuid.uuid4())
    unique_filename = f"{file_id}{file_extension}"
    destination_path = settings.UPLOAD_DIR / unique_filename

    # 3. Save to Disk (Async safe)
    try:
        # We use a context manager to ensure the file is closed properly
        with open(destination_path, "wb") as buffer:
            # copyfileobj is efficient for large files
            shutil.copyfileobj(file.file, buffer)
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")
    finally:
        # Close the underlying file handle from the request
        await file.close()

    return file_id, str(destination_path)