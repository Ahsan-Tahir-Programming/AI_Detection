from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from datetime import datetime
import os
from app.core.logger import logger
from app.core.config import DOWNLOAD_DIR
from app.services.inference import inference_service
from app.services import db
from app.schemas import (
    DetectionRequest, 
    DetectionResponse, 
    PaginatedDetectionsResponse,
    HealthCheckResponse,
    ErrorResponse,
    DeleteResponse
)
from starlette.concurrency import run_in_threadpool

router = APIRouter()

@router.get("/", tags=["health"])
async def root():
    """Root endpoint"""
    return {"message": "Main API is running"}

@router.get("/health", response_model=HealthCheckResponse, tags=["health"])
async def health_check():
    """Health check endpoint for deployment monitoring"""
    return {"status": "ok", "service": "AI Detection API"}

@router.post("/detect/", response_model=DetectionResponse, tags=["detection"])
async def detect(request: DetectionRequest):
    """Process detection request with image analysis
    
    Accepts image URL and model configuration, runs YOLO inference,
    saves results to database, and returns detection metadata.
    """
    logger.info(f"Incoming /detect/ request | RouteId: {request.routeId}")

    try:
        # Offload CPU / blocking work to threadpool so the ASGI event loop is not blocked
        result = await run_in_threadpool(
            inference_service.process_detection,
            request.modelname,
            request.project,
            request.imageKey,
            str(request.imageUrl),
            request.routeId,
            request.visitDate or datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )
        # Save to DB and return as response model
        saved = db.save_detection(result)
        return saved

    except HTTPException as e:
        logger.error(f"HTTP Exception in /detect/: {e.detail}")
        raise
    except Exception as e:
        logger.error(f"Unhandled Exception in /detect/: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.get('/detections/', response_model=PaginatedDetectionsResponse, tags=["detection"])
async def list_detections(page: int = 1, page_size: int = 12):
    """Returns paginated detections saved in the system
    
    Query Parameters:
    - page: Page number (default 1)
    - page_size: Items per page (default 12)
    """
    try:
        items, total = db.get_detections(page=page, page_size=page_size)
        return {"success": True, "data": {"items": items, "total": total}}
    except Exception as e:
        logger.error(f"Error fetching detections: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.delete('/detections/{request_id}', response_model=DeleteResponse, tags=["detection"])
async def delete_detection(request_id: str):
    """Delete a detection by request ID"""
    try:
        ok = db.delete_detection(request_id)
        if not ok:
            raise HTTPException(status_code=404, detail="Detection not found")
        return {"success": True, "message": "Detection deleted successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error deleting detection: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.get('/download-image/{filename}', tags=["download"])
async def download_image(filename: str):
    """Download image file with proper Content-Disposition header
    
    Serves processed detection images for download with attachment disposition.
    Security check ensures files are served only from DOWNLOAD_DIR.
    """
    try:
        file_path = os.path.join(DOWNLOAD_DIR, filename)
        
        # Security check: ensure the file is within DOWNLOAD_DIR
        if not os.path.abspath(file_path).startswith(os.path.abspath(DOWNLOAD_DIR)):
            raise HTTPException(status_code=400, detail="Invalid filename")
        
        # Check if file exists
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not found")
        
        # Return file with attachment disposition to force download
        return FileResponse(
            path=file_path,
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error downloading image: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))