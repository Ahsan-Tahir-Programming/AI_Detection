"""FastAPI API route definitions."""
import os
from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Query
from fastapi.responses import FileResponse
from starlette.concurrency import run_in_threadpool

from app.core.logger import logger
from app.core.config import DOWNLOAD_DIR
from app.services.inference import inference_service
from app.services import db
from app.schemas import (
    DetectionRequest,
    DetectionResponse,
    PaginatedDetectionsResponse,
    HealthCheckResponse,
    DeleteResponse,
    ModelsResponse,
)

router = APIRouter()


@router.get("/", tags=["health"])
async def root():
    """Root endpoint verifying API availability."""
    return {"message": "AI Detection API is running", "docs": "/docs"}


@router.get("/health", response_model=HealthCheckResponse, tags=["health"])
async def health_check():
    """Health check endpoint for container and deployment monitoring."""
    return {"status": "ok", "service": "AI Detection API", "version": "1.0.0"}


@router.get("/models", response_model=ModelsResponse, tags=["models"])
async def list_models():
    """Returns all discovered and loaded YOLO models in the system."""
    try:
        data = inference_service.get_available_models()
        return data
    except Exception as e:
        logger.error(f"Error fetching models: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analytics/stats", tags=["analytics"])
async def get_analytics():
    """Returns aggregated compliance and defect statistics across all historical audits."""
    try:
        stats = db.get_analytics_summary()
        return {"success": True, "data": stats}
    except Exception as e:
        logger.error(f"Error computing analytics stats: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/detect/", response_model=DetectionResponse, tags=["detection"])
async def detect_from_url(request: DetectionRequest):
    """Process detection request using a remote image URL.

    Accepts image URL and parameters, executes YOLO inference, saves
    annotated image and records to database, and returns detection results.
    """
    logger.info(f"Incoming /detect/ request for Route: {request.routeId} | Model: {request.modelname}")
    try:
        visit_date = request.visitDate or datetime.now(timezone.utc).strftime("%Y-%m-%d")
        result = await run_in_threadpool(
            inference_service.process_detection,
            request.modelname,
            request.project,
            request.imageKey,
            str(request.imageUrl),
            request.routeId,
            visit_date,
            request.confidence,
            request.iou,
        )
        saved = db.save_detection(result)
        return saved
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unhandled error in /detect/: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Inference failure: {str(e)}")


@router.post("/detect/upload", response_model=DetectionResponse, tags=["detection"])
async def detect_from_upload(
    file: UploadFile = File(..., description="Image file to analyze"),
    modelname: str = Form(default="zyn", description="Model name (e.g., 'zyn')"),
    project: str = Form(default="ai", description="Project name"),
    routeId: str = Form(default="route_001", description="Route identifier"),
    imageKey: str = Form(default="upload_img", description="Image key"),
    categoryName: str = Form(default="general", description="Category name"),
    visitDate: Optional[str] = Form(default=None, description="Visit date (YYYY-MM-DD)"),
    confidence: Optional[float] = Form(default=None, description="Confidence threshold (0.01 - 1.0)"),
    iou: Optional[float] = Form(default=None, description="IOU threshold (0.01 - 1.0)"),
):
    """Process detection request by directly uploading an image file."""
    if file.content_type and not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Uploaded file must be a valid image format.")

    logger.info(f"Incoming /detect/upload request for Route: {routeId} | Filename: {file.filename}")
    try:
        file_bytes = await file.read()
        if not file_bytes:
            raise HTTPException(status_code=400, detail="Uploaded file is empty.")

        visit_date_val = visitDate or datetime.now(timezone.utc).strftime("%Y-%m-%d")
        result = await run_in_threadpool(
            inference_service.process_uploaded_detection,
            file_bytes,
            modelname,
            project,
            imageKey,
            routeId,
            visit_date_val,
            file.filename or "upload.jpg",
            confidence,
            iou,
        )
        saved = db.save_detection(result)
        return saved
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unhandled error in /detect/upload: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Upload inference failure: {str(e)}")


@router.get("/detections/", response_model=PaginatedDetectionsResponse, tags=["detection"])
async def list_detections(
    page: int = Query(default=1, ge=1, description="Page number (1-indexed)"),
    page_size: int = Query(default=12, ge=1, le=100, description="Items per page"),
):
    """Returns paginated saved detections."""
    try:
        items, total = db.get_detections(page=page, page_size=page_size)
        return {"success": True, "data": {"items": items, "total": total}}
    except Exception as e:
        logger.error(f"Error fetching detections: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/detections/{request_id}", response_model=DeleteResponse, tags=["detection"])
async def delete_detection(request_id: str):
    """Delete a detection record and its processed image by request ID."""
    try:
        ok = db.delete_detection(request_id)
        if not ok:
            raise HTTPException(status_code=404, detail=f"Detection with requestId '{request_id}' not found.")
        return {"success": True, "message": "Detection deleted successfully."}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting detection: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/download-image/{filename}", tags=["download"])
async def download_image(filename: str):
    """Download image file with Content-Disposition header and path-traversal prevention."""
    try:
        # Prevent directory traversal attacks
        safe_filename = os.path.basename(filename)
        file_path = os.path.join(DOWNLOAD_DIR, safe_filename)
        resolved_path = os.path.abspath(file_path)
        resolved_dir = os.path.abspath(DOWNLOAD_DIR)

        if not resolved_path.startswith(resolved_dir) or not os.path.exists(resolved_path):
            raise HTTPException(status_code=404, detail="Requested image file was not found.")

        return FileResponse(
            path=resolved_path,
            media_type="image/jpeg",
            headers={"Content-Disposition": f"attachment; filename=\"{safe_filename}\""}
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error serving image download: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))