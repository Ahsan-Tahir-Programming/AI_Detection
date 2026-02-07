# Pydantic Integration Guide

## Overview
Successfully integrated Pydantic models into the FastAPI backend for improved type safety, request validation, and automatic OpenAPI documentation.

## Changes Made

### 1. Backend - New Pydantic Schemas (`app/schemas.py`)

Created comprehensive Pydantic models:

#### Request Models
- **`DetectionRequest`** - Validates all incoming detection request fields:
  - `modelname`: Model selection (zyn, nestle_chiller, etc.)
  - `project`: Project identifier
  - `routeId`: Route identifier
  - `imageKey`: Image key identifier
  - `imageUrl`: Image URL (validated as HttpUrl)
  - `categoryName`: Product category
  - `visitDate`: Visit date (optional, defaults to today)

#### Response Models
- **`DetectedItem`** - Individual detection object with class info, confidence, and bbox
- **`SKUInfo`** - SKU detection information with detection count and coordinates
- **`DetectionResponse`** - Complete detection result with:
  - Request metadata (id, requestId, project, routeId, etc.)
  - Image information (size, URLs)
  - Detection results and detected SKUs
  - Timestamp

#### Utility Response Models
- **`PaginatedDetectionsResponse`** - Paginated gallery listing response
- **`DeleteResponse`** - Response for delete operations
- **`HealthCheckResponse`** - Health check endpoint response
- **`ErrorResponse`** - Standardized error response format

### 2. Backend - Updated Routes (`app/api/routes.py`)

#### Key Changes:
- **`POST /detect/`**: Changed from multiple Form fields to single `DetectionRequest` body
  - Automatic request validation via Pydantic
  - Type-safe field access
  - Automatic OpenAPI documentation with example payloads
  
- **`GET /health`**: Added `response_model=HealthCheckResponse`
  
- **`GET /detections/`**: Added `response_model=PaginatedDetectionsResponse`
  
- **`DELETE /detections/{request_id}`**: Added `response_model=DeleteResponse`
  
- **`GET /download-image/{filename}`**: Added proper documentation and tags

#### Benefits:
- Automatic validation of all request data
- Type hints for better IDE support
- Auto-generated Swagger/OpenAPI documentation
- Consistent error responses
- Standardized response structure

### 3. Frontend Updates

#### DetectionForm.tsx
- Updated to send JSON instead of FormData
- Introduced `DetectionFormData` interface matching Pydantic model
- Simplified `handleSubmit` to pass object directly

#### App.tsx
- Added `DetectionFormData` interface
- Updated `handleDetection` to:
  - Send JSON with `Content-Type: application/json` header
  - JSON.stringify the form data
  - Handle Pydantic response models properly
- Improved response handling

## Migration Notes

### Request Format Change
**Before:**
```
POST /detect/
Content-Type: multipart/form-data

(FormData with individual fields)
```

**After:**
```
POST /detect/
Content-Type: application/json

{
  "modelname": "zyn",
  "project": "ai",
  "routeId": "route_001",
  "imageKey": "img_123",
  "imageUrl": "https://example.com/image.jpg",
  "categoryName": "product",
  "visitDate": "2026-02-07"
}
```

### Response Format
All successful responses now return the Pydantic model directly:

```json
{
  "requestId": "abc-123",
  "project": "ai",
  "routeId": "route_001",
  "imageKey": ["img_123"],
  "imageSize": [1920, 1080],
  "visitDate": "2026-02-07",
  "originalImageUrl": "https://...",
  "processedImageUrl": "http://localhost:8000/download/...",
  "detectedSKU": {...},
  "detections": [...]
}
```

## API Documentation

Fast start with automatic Swagger UI:
1. Start the backend: `python -m uvicorn app.main:app --reload`
2. Visit: `http://localhost:8000/docs`
3. All endpoints are documented with request/response schemas and examples

## Type Safety Benefits

### For Backend:
- Request data is automatically validated on arrival
- Type hints enable IDE autocomplete
- Serialization is handled consistently
- OpenAPI/Swagger docs generated automatically

### For Frontend:
- TypeScript interfaces match backend models
- Better autocomplete when accessing response data
- Response structure is predictable
- Type checking catches errors before runtime

## Deployment Considerations

### Environment Variables Support (if needed)
If you need to add configuration to Pydantic models, use Pydantic settings:

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    api_key: str
    debug: bool = False
    
    class Config:
        env_file = ".env"
```

### Validation Rules
Add custom validators if needed:

```python
from pydantic import field_validator

class DetectionRequest(BaseModel):
    imageUrl: HttpUrl
    
    @field_validator('imageUrl')
    @classmethod
    def validate_url_accessible(cls, v):
        # Add custom validation logic
        return v
```

## Testing with Pydantic Models

### Using curl:
```bash
curl -X POST http://localhost:8000/detect/ \
  -H "Content-Type: application/json" \
  -d '{
    "modelname": "zyn",
    "project": "ai",
    "routeId": "test_route",
    "imageKey": "test_img",
    "imageUrl": "https://example.com/image.jpg",
    "categoryName": "test",
    "visitDate": "2026-02-07"
  }'
```

### Using Python requests:
```python
import requests

payload = {
    "modelname": "zyn",
    "project": "ai",
    "routeId": "test_route",
    "imageKey": "test_img",
    "imageUrl": "https://example.com/image.jpg",
    "categoryName": "test",
    "visitDate": "2026-02-07"
}

response = requests.post("http://localhost:8000/detect/", json=payload)
print(response.json())
```

## Verification Checklist

- ✅ Python syntax validated for schemas.py
- ✅ Frontend TypeScript build passed
- ✅ All routes updated with Pydantic models
- ✅ Frontend updated to send JSON
- ✅ Response handling updated
- ✅ API documentation tags added to all endpoints

## Future Enhancements

1. **Field Validators**: Add custom validation for specific fields
   ```python
   @field_validator('visitDate')
   @classmethod
   def validate_date_format(cls, v):
       # Custom date validation
       pass
   ```

2. **Discriminated Unions**: If you have multiple detection types
   ```python
   from pydantic import Field
   
   class Detection(BaseModel):
       type: Literal["sku", "defect"]
       # Different fields based on type
   ```

3. **Serialization Aliases**: For snake_case/camelCase conversion
   ```python
   class DetectionRequest(BaseModel):
       image_key: str = Field(alias="imageKey")
       
       class Config:
           populate_by_name = True
   ```

4. **Database Integration**: Use Pydantic for ORM serialization
   ```python
   from pydantic import ConfigDict
   
   class DetectionResponse(BaseModel):
       model_config = ConfigDict(from_attributes=True)
   ```

## Resources

- [Pydantic Documentation](https://docs.pydantic.dev/latest/)
- [FastAPI with Pydantic](https://fastapi.tiangolo.com/tutorial/body/)
- [OpenAPI Schema Generation](https://fastapi.tiangolo.com/tutorial/response-model/)
