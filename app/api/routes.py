# File path: doc_intel_backend/app/api/routes.py

from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from app.api.schemas import UploadResponse, HealthCheck, QueryRequest, QueryResponse
from app.utils.file_ops import save_upload_file
from app.core.config import settings
from app.services.orchestrator import Orchestrator

router = APIRouter()

# Initialize Orchestrator once (Singleton pattern)
orchestrator = Orchestrator()

@router.get("/health", response_model=HealthCheck)
async def health_check():
    return HealthCheck(version=settings.VERSION)

@router.post("/upload", response_model=UploadResponse)
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
):
    """
    1. Saves the file locally.
    2. Returns a File ID immediately.
    3. Triggers the AI Pipeline (Ingestion -> Indexing) in the background.
    """
    # 1. Save File
    file_id, file_path = await save_upload_file(file)

    # 2. Trigger Orchestrator (Background Task)
    # This ensures the UI doesn't freeze while we process large PDFs
    background_tasks.add_task(orchestrator.run_pipeline, file_path, file_id)

    return UploadResponse(
        filename=file.filename,
        file_id=file_id,
        content_type=file.content_type,
        saved_path=file_path,
        message="File uploaded. AI processing started in background."
    )

@router.post("/query/{file_id}", response_model=QueryResponse)
async def ask_question(file_id: str, request: QueryRequest):
    """
    Ask a question about a specific file.
    """
    try:
        # Delegate to Orchestrator
        result = orchestrator.ask(request.question, file_id)
        
        return QueryResponse(
            answer=result["answer"],
            sources=result["sources"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))