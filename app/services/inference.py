import os
import uuid
import requests
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from datetime import datetime
from ultralytics import YOLO
from fastapi import HTTPException

# Import Clean Configs and Logger
from app.core.config import MODELS_DIR, DOWNLOAD_DIR, FONT_PATH, CLASS_COLORS, CLASS_NAME_MAP
from app.core.logger import logger

class InferenceService:
    def __init__(self):
        self.model_cache = {}

    def preload_models(self):
        """Loads models into memory on startup"""
        logger.info("Preloading models from disk...")
        model_path = os.path.join(MODELS_DIR, "zyn.pt")
        try:
            self.model_cache["zyn"] = YOLO(model_path)
            logger.info("Loaded model: zyn")
        except Exception as e:
            logger.error(f"Failed to load model 'zyn': {e}", exc_info=True)

    def get_model(self, model_name: str):
        if model_name not in self.model_cache:
            logger.warning(f"Model '{model_name}' not found in cache.")
            raise HTTPException(status_code=404, detail=f"Model '{model_name}' not found.")
        return self.model_cache[model_name]

    def process_detection(self, model_name, project, image_key, image_url, route_id, visit_date):
        """Synchronous detection processing. This is intentionally synchronous so it can be
        offloaded to a threadpool from the async route and not block the event loop."""
        # 1. Get Model
        model = self.get_model(model_name)

        # 2. Download Image
        try:
            response = requests.get(image_url, allow_redirects=True, timeout=10)
            response.raise_for_status()
            pil_image = Image.open(BytesIO(response.content)).convert("RGB")
        except Exception as e:
            logger.error(f"Failed to fetch image: {e}", exc_info=True)
            raise HTTPException(status_code=400, detail=f"Failed to fetch image: {str(e)}")

        # 3. Predict
        logger.info(f"Running inference for {route_id}...")
        start_ts = datetime.utcnow()
        results = model.predict(source=pil_image, save=False, conf=0.5, iou=0.7, imgsz=640)
        elapsed = (datetime.utcnow() - start_ts).total_seconds()
        logger.info(f"Inference for {route_id} took {elapsed:.2f}s")

        # 4. Draw & Process
        draw = ImageDraw.Draw(pil_image)
        try:
            font = ImageFont.truetype(FONT_PATH, 14)
        except:
            font = ImageFont.load_default()

        class_names = model.names
        detections = []

        for result in results[0].boxes.data.cpu().numpy():
            x_min, y_min, x_max, y_max, conf, class_id = result
            class_id = int(class_id)
            class_name = class_names[class_id] if class_id < len(class_names) else f"Class {class_id}"

            # Get Color
            color = CLASS_COLORS.get(class_name, (255, 255, 255))

            detections.append({
                "class_id": class_id,
                "bbox": [float(x_min), float(y_min), float(x_max), float(y_max)],
                "coordinates": {"x": int(x_min), "y": int(y_min), "w": int(x_max - x_min), "h": int(y_max - y_min)},
                "class_name": class_name,
                "confidence": float(conf)
            })

            # Draw Box
            draw.rectangle([x_min, y_min, x_max, y_max], outline=color, width=6)

            # Draw Label
            text_bbox = draw.textbbox((x_min, y_min), class_name, font=font)
            label_h = text_bbox[3] - text_bbox[1]
            draw.rectangle([x_min, y_min - label_h - 10, x_min + (text_bbox[2] - text_bbox[0]) + 10, y_min],
                           fill="black")
            draw.text((x_min + 5, y_min - label_h - 5), class_name, fill="white", font=font)

        # 5. Save Image
        unique_id = str(uuid.uuid4())
        safe_date = visit_date.split()[0] if visit_date else "unknown_date"
        image_name = f"{route_id}_{safe_date}_{unique_id}_processed.jpg"
        image_path = os.path.join(DOWNLOAD_DIR, image_name)

        pil_image.save(image_path, format="JPEG")
        logger.info(f"Saved processed image: {image_path}")

        # 6. Prepare Response Logic
        base_url = os.getenv("BASE_URL", "http://127.0.0.1:8000")
        processed_url = f"{base_url}/download/{image_name}"

        # Initialize SKU count
        detected_sku = {v: {"detected": False} for v in CLASS_NAME_MAP.values()}

        for det in detections:
            mapped_key = CLASS_NAME_MAP.get(det["class_name"])
            if mapped_key:
                if not detected_sku[mapped_key]["detected"]:
                    detected_sku[mapped_key].update({"detected": True, "count": 1, "coordinates": [det["coordinates"]]})
                else:
                    detected_sku[mapped_key]["count"] += 1
                    detected_sku[mapped_key]["coordinates"].append(det["coordinates"])

        return {
            "project": project,
            "routeId": route_id,
            "imageKey": [image_key],
            "imageSize": [pil_image.width, pil_image.height],
            "requestId": unique_id,
            "visitDate": visit_date,
            "detectedSKU": detected_sku,
            "detections": detections,
            "originalImageUrl": image_url,
            "processedImageUrl": processed_url
        }

# Initialize singleton instance
inference_service = InferenceService()