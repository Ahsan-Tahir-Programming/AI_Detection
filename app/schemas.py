"""Pydantic v2 schemas for request/response validation and OpenAPI documentation."""
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field, HttpUrl, ConfigDict


class DetectionRequest(BaseModel):
    """Request schema for URL-based detection endpoint."""
    modelname: str = Field(default="zyn", description="Model name (e.g., 'zyn')")
    project: str = Field(..., description="Project name")
    routeId: str = Field(..., description="Route identifier")
    imageKey: str = Field(..., description="Image key identifier")
    imageUrl: HttpUrl = Field(..., description="Public HTTP/HTTPS URL of the image to process")
    categoryName: str = Field(..., description="Category of the product")
    visitDate: str = Field(default="", description="Visit date (YYYY-MM-DD format)")
    confidence: Optional[float] = Field(default=None, ge=0.01, le=1.0, description="Detection confidence threshold")
    iou: Optional[float] = Field(default=None, ge=0.01, le=1.0, description="IOU threshold for NMS")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "modelname": "zyn",
                "project": "ai",
                "routeId": "route_001",
                "imageKey": "img_123",
                "imageUrl": "https://images.unsplash.com/photo-1542291026-7eec264c27ff",
                "categoryName": "product",
                "visitDate": "2026-10-27",
                "confidence": 0.5,
                "iou": 0.7
            }
        }
    )


class DetectedItem(BaseModel):
    """Schema for individual detection item."""
    class_id: int = Field(..., description="Numerical class ID")
    class_name: str = Field(..., description="Human-readable class name")
    confidence: float = Field(..., description="Prediction confidence score (0.0 - 1.0)")
    bbox: List[float] = Field(..., description="Bounding box [x_min, y_min, x_max, y_max]")
    coordinates: Dict[str, int] = Field(..., description="Box coordinates {x, y, w, h}")


class SKUInfo(BaseModel):
    """Schema for SKU detection summary."""
    detected: bool
    count: Optional[int] = None
    coordinates: Optional[List[Dict[str, int]]] = None


class DetectionResponse(BaseModel):
    """Response schema for detection result."""
    id: Optional[int] = None
    requestId: str = Field(..., description="Unique detection request ID")
    project: str
    routeId: str
    imageKey: List[str]
    imageSize: List[int] = Field(..., description="Image dimensions [width, height]")
    visitDate: str
    originalImageUrl: str
    processedImageUrl: str
    detectedSKU: Dict[str, SKUInfo]
    detections: List[DetectedItem]
    createdAt: Optional[str] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": 1,
                "requestId": "abc-123-def",
                "project": "ai",
                "routeId": "route_001",
                "imageKey": ["img_123"],
                "imageSize": [1920, 1080],
                "visitDate": "2026-10-27",
                "originalImageUrl": "https://example.com/image.jpg",
                "processedImageUrl": "http://127.0.0.1:8000/download/route_001_2026-10-27_abc-123-def_processed.jpg",
                "detectedSKU": {
                    "sheet_damaged": {
                        "detected": True,
                        "count": 1,
                        "coordinates": [{"x": 100, "y": 200, "w": 50, "h": 60}]
                    }
                },
                "detections": [
                    {
                        "class_id": 2,
                        "class_name": "BWU Damage",
                        "confidence": 0.88,
                        "bbox": [100.0, 200.0, 150.0, 260.0],
                        "coordinates": {"x": 100, "y": 200, "w": 50, "h": 60}
                    }
                ]
            }
        }
    )


class ModelInfo(BaseModel):
    """Metadata regarding a discovered YOLO model."""
    name: str = Field(..., description="Model identifier for detection requests")
    filename: str = Field(..., description="Filename on disk")
    size_mb: float = Field(..., description="Model file size in Megabytes")
    loaded: bool = Field(..., description="True if loaded into memory cache")


class ModelsResponse(BaseModel):
    """Response schema for list of available models."""
    models: List[str]
    details: List[ModelInfo]


class PaginatedDetectionsResponse(BaseModel):
    """Response schema for paginated detections."""
    success: bool = True
    data: Dict[str, Any] = Field(..., description="Contains 'items' list and 'total' count")


class HealthCheckResponse(BaseModel):
    """Health check response schema."""
    status: str = Field(default="ok", description="Service health status")
    service: str = Field(default="AI Detection API", description="Service title")
    version: str = Field(default="1.0.0", description="API version")


class DeleteResponse(BaseModel):
    """Response for delete operations."""
    success: bool
    message: Optional[str] = None


class ErrorResponse(BaseModel):
    """Standardized error response schema."""
    success: bool = False
    error: str = Field(..., description="Descriptive error explanation")
