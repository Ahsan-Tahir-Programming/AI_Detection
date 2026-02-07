"""Pydantic schemas for request/response validation and OpenAPI documentation"""
from pydantic import BaseModel, Field, HttpUrl
from typing import List, Dict, Optional, Any
from datetime import datetime


class DetectionRequest(BaseModel):
    """Request schema for detection endpoint"""
    modelname: str = Field(..., description="Model name (e.g., 'zyn', 'nestle_chiller')")
    project: str = Field(..., description="Project name")
    routeId: str = Field(..., description="Route identifier")
    imageKey: str = Field(..., description="Image key identifier")
    imageUrl: HttpUrl = Field(..., description="URL of the image to process")
    categoryName: str = Field(..., description="Category of the product")
    visitDate: str = Field(default="", description="Visit date (YYYY-MM-DD format)")

    class Config:
        json_schema_extra = {
            "example": {
                "modelname": "zyn",
                "project": "ai",
                "routeId": "route_001",
                "imageKey": "img_123",
                "imageUrl": "https://example.com/image.jpg",
                "categoryName": "product",
                "visitDate": "2026-02-07"
            }
        }


class DetectedItem(BaseModel):
    """Schema for individual detection item"""
    class_id: int
    class_name: str
    confidence: float
    bbox: List[float] = Field(..., description="Bounding box [x_min, y_min, x_max, y_max]")
    coordinates: Dict[str, int] = Field(..., description="Coordinates {x, y, w, h}")


class SKUInfo(BaseModel):
    """Schema for SKU detection info"""
    detected: bool
    count: Optional[int] = None
    coordinates: Optional[List[Dict[str, int]]] = None


class DetectionResponse(BaseModel):
    """Response schema for detection result"""
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

    class Config:
        json_schema_extra = {
            "example": {
                "requestId": "abc-123",
                "project": "ai",
                "routeId": "route_001",
                "imageKey": ["img_123"],
                "imageSize": [1920, 1080],
                "visitDate": "2026-02-07",
                "originalImageUrl": "https://example.com/image.jpg",
                "processedImageUrl": "http://localhost:8000/download/route_001_2026-02-07_abc-123_processed.jpg",
                "detectedSKU": {
                    "zyn_product": {
                        "detected": True,
                        "count": 2,
                        "coordinates": [{"x": 100, "y": 200, "w": 50, "h": 60}]
                    }
                },
                "detections": []
            }
        }


class PaginatedDetectionsResponse(BaseModel):
    """Response schema for paginated detections"""
    success: bool
    data: Dict[str, Any] = Field(..., description="Contains 'items' list and 'total' count")

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "data": {
                    "items": [],
                    "total": 0
                }
            }
        }


class ErrorResponse(BaseModel):
    """Response schema for errors"""
    success: bool = Field(default=False)
    error: str = Field(..., description="Error message")

    class Config:
        json_schema_extra = {
            "example": {
                "success": False,
                "error": "Model not found"
            }
        }


class HealthCheckResponse(BaseModel):
    """Health check response"""
    status: str = Field(default="ok", description="Service status")
    service: str = Field(..., description="Service name")

    class Config:
        json_schema_extra = {
            "example": {
                "status": "ok",
                "service": "AI Detection API"
            }
        }


class DeleteResponse(BaseModel):
    """Response for delete operations"""
    success: bool
    message: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Detection deleted successfully"
            }
        }
