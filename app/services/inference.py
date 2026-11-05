"""AI inference service for YOLO object detection."""
import os
import uuid
from io import BytesIO
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional
from urllib.parse import urlparse

import requests
from PIL import Image, ImageDraw, ImageFont
from ultralytics import YOLO
from fastapi import HTTPException

from app.core.config import (
    MODELS_DIR,
    DOWNLOAD_DIR,
    FONT_PATH,
    CLASS_COLORS,
    CLASS_NAME_MAP,
    BASE_URL,
    MAX_IMAGE_SIZE_BYTES,
    DEFAULT_CONFIDENCE,
    DEFAULT_IOU,
)
from app.core.logger import logger


class InferenceService:
    """Manages YOLO model caching, preloading, image annotation, and inference execution."""

    def __init__(self):
        self.model_cache: Dict[str, YOLO] = {}

    def get_available_models(self) -> Dict[str, Any]:
        """Scans MODELS_DIR and returns metadata on all available models."""
        models_meta = []
        model_names = []
        if os.path.exists(MODELS_DIR):
            for file in os.listdir(MODELS_DIR):
                if file.endswith(".pt"):
                    name = os.path.splitext(file)[0]
                    file_path = os.path.join(MODELS_DIR, file)
                    size_mb = round(os.path.getsize(file_path) / (1024 * 1024), 2)
                    is_loaded = name in self.model_cache
                    model_names.append(name)
                    models_meta.append({
                        "name": name,
                        "filename": file,
                        "size_mb": size_mb,
                        "loaded": is_loaded,
                    })
        return {"models": model_names, "details": models_meta}

    def preload_models(self):
        """Loads available models from disk into memory on startup."""
        logger.info("Discovering and preloading models from disk...")
        models_info = self.get_available_models()
        for model_name in models_info["models"]:
            model_path = os.path.join(MODELS_DIR, f"{model_name}.pt")
            try:
                self.model_cache[model_name] = YOLO(model_path)
                logger.info(f"Loaded YOLO model '{model_name}' successfully into memory.")
            except Exception as e:
                logger.error(f"Failed to load model '{model_name}' from {model_path}: {e}", exc_info=True)

    def get_model(self, model_name: str) -> YOLO:
        """Retrieves model from cache or loads on-demand if present in MODELS_DIR."""
        normalized_name = model_name.strip().lower()

        # Check in-memory cache
        if normalized_name in self.model_cache:
            return self.model_cache[normalized_name]

        # On-demand loading if file exists on disk
        model_file = os.path.join(MODELS_DIR, f"{normalized_name}.pt")
        if os.path.exists(model_file):
            try:
                logger.info(f"Loading model '{normalized_name}' on-demand from {model_file}...")
                model = YOLO(model_file)
                self.model_cache[normalized_name] = model
                return model
            except Exception as e:
                logger.error(f"Failed to load model file {model_file}: {e}", exc_info=True)
                raise HTTPException(status_code=500, detail=f"Failed to initialize model '{model_name}': {str(e)}")

        # Not found
        available = list(self.model_cache.keys())
        if os.path.exists(MODELS_DIR):
            available.extend([os.path.splitext(f)[0] for f in os.listdir(MODELS_DIR) if f.endswith(".pt")])
        available = sorted(list(set(available)))
        logger.warning(f"Model '{model_name}' requested but not found. Available models: {available}")
        raise HTTPException(
            status_code=404,
            detail=f"Model '{model_name}' not found. Available models: {available or ['None found in app/models']}"
        )

    def _download_image(self, image_url: str) -> Image.Image:
        """Safely downloads an image from a URL with SSRF checks and size limits."""
        parsed = urlparse(image_url)
        if parsed.scheme not in ("http", "https"):
            raise HTTPException(status_code=400, detail="Invalid image URL scheme. Only HTTP and HTTPS are permitted.")

        # Disallow loopback / private IP requests to prevent SSRF
        hostname = (parsed.hostname or "").lower()
        if hostname in ("localhost", "127.0.0.1", "::1", "0.0.0.0") or hostname.startswith("169.254."):
            raise HTTPException(status_code=400, detail="Requests to loopback or metadata addresses are prohibited.")

        try:
            with requests.get(image_url, stream=True, allow_redirects=True, timeout=15) as response:
                response.raise_for_status()

                # Check Content-Length header if provided
                content_length = response.headers.get("Content-Length")
                if content_length and int(content_length) > MAX_IMAGE_SIZE_BYTES:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Image size exceeds maximum allowed limit of {MAX_IMAGE_SIZE_BYTES // (1024 * 1024)}MB."
                    )

                buffer = bytearray()
                for chunk in response.iter_content(chunk_size=64 * 1024):
                    buffer.extend(chunk)
                    if len(buffer) > MAX_IMAGE_SIZE_BYTES:
                        raise HTTPException(
                            status_code=400,
                            detail=f"Image payload exceeded maximum limit of {MAX_IMAGE_SIZE_BYTES // (1024 * 1024)}MB."
                        )

            pil_image = Image.open(BytesIO(buffer)).convert("RGB")
            return pil_image
        except HTTPException:
            raise
        except requests.RequestException as e:
            logger.error(f"Network error fetching image from URL {image_url}: {e}", exc_info=True)
            raise HTTPException(status_code=400, detail=f"Failed to fetch image from URL: {str(e)}")
        except Exception as e:
            logger.error(f"Failed to decode image from {image_url}: {e}", exc_info=True)
            raise HTTPException(status_code=400, detail=f"Invalid image format: {str(e)}")

    def run_inference_on_image(
        self,
        pil_image: Image.Image,
        model_name: str,
        project: str,
        image_key: str,
        route_id: str,
        visit_date: str,
        original_url: str = "",
        confidence: Optional[float] = None,
        iou: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Runs YOLO detection on a PIL Image, annotates it, and returns the response payload."""
        model = self.get_model(model_name)
        conf_val = confidence if confidence is not None else DEFAULT_CONFIDENCE
        iou_val = iou if iou is not None else DEFAULT_IOU

        logger.info(f"Running inference for Route: {route_id} | Model: {model_name} | Conf: {conf_val} | IOU: {iou_val}")
        start_ts = datetime.now(timezone.utc)
        results = model.predict(source=pil_image, save=False, conf=conf_val, iou=iou_val, imgsz=640)
        elapsed = (datetime.now(timezone.utc) - start_ts).total_seconds()
        logger.info(f"Inference for route {route_id} completed in {elapsed:.3f}s")

        # Prepare drawing context
        draw = ImageDraw.Draw(pil_image)
        try:
            font = ImageFont.truetype(FONT_PATH, 16)
        except Exception:
            font = ImageFont.load_default()

        class_names = model.names
        detections: List[Dict[str, Any]] = []

        for result in results[0].boxes.data.cpu().numpy():
            x_min, y_min, x_max, y_max, conf, class_id = result
            class_id = int(class_id)
            class_name = class_names[class_id] if class_id < len(class_names) else f"Class {class_id}"

            color = CLASS_COLORS.get(class_name, (255, 255, 255))

            detections.append({
                "class_id": class_id,
                "class_name": class_name,
                "confidence": round(float(conf), 4),
                "bbox": [float(x_min), float(y_min), float(x_max), float(y_max)],
                "coordinates": {
                    "x": int(x_min),
                    "y": int(y_min),
                    "w": int(x_max - x_min),
                    "h": int(y_max - y_min)
                },
            })

            # Draw bounding box
            draw.rectangle([x_min, y_min, x_max, y_max], outline=color, width=4)

            # Draw label banner with confidence
            label_text = f"{class_name} ({conf * 100:.1f}%)"
            try:
                text_bbox = draw.textbbox((x_min, y_min), label_text, font=font)
                label_h = text_bbox[3] - text_bbox[1]
                label_w = text_bbox[2] - text_bbox[0]
            except Exception:
                label_h = 16
                label_w = len(label_text) * 8

            banner_y1 = max(0, y_min - label_h - 8)
            draw.rectangle([x_min, banner_y1, x_min + label_w + 10, y_min], fill="black")
            draw.text((x_min + 5, banner_y1 + 4), label_text, fill="white", font=font)

        # Save annotated image
        unique_id = str(uuid.uuid4())
        safe_date = visit_date.split()[0] if visit_date else datetime.now(timezone.utc).strftime("%Y-%m-%d")
        image_name = f"{route_id}_{safe_date}_{unique_id}_processed.jpg"
        image_path = os.path.join(DOWNLOAD_DIR, image_name)

        pil_image.save(image_path, format="JPEG", quality=90)
        logger.info(f"Saved processed image: {image_path}")

        processed_url = f"{BASE_URL}/download/{image_name}"

        # Initialize SKU counts based on configuration mapping
        detected_sku = {v: {"detected": False, "count": 0, "coordinates": []} for v in CLASS_NAME_MAP.values()}

        for det in detections:
            mapped_key = CLASS_NAME_MAP.get(det["class_name"])
            if mapped_key:
                if mapped_key not in detected_sku:
                    detected_sku[mapped_key] = {"detected": False, "count": 0, "coordinates": []}
                detected_sku[mapped_key]["detected"] = True
                detected_sku[mapped_key]["count"] += 1
                detected_sku[mapped_key]["coordinates"].append(det["coordinates"])

        return {
            "project": project,
            "routeId": route_id,
            "imageKey": [image_key],
            "imageSize": [pil_image.width, pil_image.height],
            "requestId": unique_id,
            "visitDate": visit_date or safe_date,
            "detectedSKU": detected_sku,
            "detections": detections,
            "originalImageUrl": original_url,
            "processedImageUrl": processed_url,
        }

    def process_detection(
        self,
        model_name: str,
        project: str,
        image_key: str,
        image_url: str,
        route_id: str,
        visit_date: str,
        confidence: Optional[float] = None,
        iou: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Synchronously processes detection from an image URL."""
        pil_image = self._download_image(image_url)
        return self.run_inference_on_image(
            pil_image=pil_image,
            model_name=model_name,
            project=project,
            image_key=image_key,
            route_id=route_id,
            visit_date=visit_date,
            original_url=image_url,
            confidence=confidence,
            iou=iou,
        )

    def process_uploaded_detection(
        self,
        file_bytes: bytes,
        model_name: str,
        project: str,
        image_key: str,
        route_id: str,
        visit_date: str,
        filename: str = "upload.jpg",
        confidence: Optional[float] = None,
        iou: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Synchronously processes detection from uploaded file bytes."""
        if len(file_bytes) > MAX_IMAGE_SIZE_BYTES:
            raise HTTPException(
                status_code=400,
                detail=f"Uploaded file exceeds {MAX_IMAGE_SIZE_BYTES // (1024 * 1024)}MB limit."
            )
        try:
            pil_image = Image.open(BytesIO(file_bytes)).convert("RGB")
        except Exception as e:
            logger.error(f"Failed to decode uploaded image: {e}", exc_info=True)
            raise HTTPException(status_code=400, detail="Invalid image file format.")

        # Save original upload to downloads directory as well so frontend can display both side by side
        safe_orig_name = f"orig_{uuid.uuid4()}_{os.path.basename(filename)}"
        orig_path = os.path.join(DOWNLOAD_DIR, safe_orig_name)
        pil_image.save(orig_path, format="JPEG", quality=90)
        original_url = f"{BASE_URL}/download/{safe_orig_name}"

        return self.run_inference_on_image(
            pil_image=pil_image,
            model_name=model_name,
            project=project,
            image_key=image_key,
            route_id=route_id,
            visit_date=visit_date,
            original_url=original_url,
            confidence=confidence,
            iou=iou,
        )


# Singleton instance
inference_service = InferenceService()