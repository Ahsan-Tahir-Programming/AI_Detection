"""Database persistence layer using SQLAlchemy for detection records."""
import os
import json
from datetime import datetime, timezone
from typing import List, Tuple, Dict, Any, Optional
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import DATABASE_URL, DOWNLOAD_DIR
from app.core.logger import logger

# Initialize engine with SQLite-specific flags only if SQLite is used
connect_args = {"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Detection(Base):
    """SQLAlchemy model for detection metadata."""
    __tablename__ = "detections"

    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(String, unique=True, index=True, nullable=False)
    project = Column(String, nullable=True)
    route_id = Column(String, nullable=True)
    image_key = Column(String, nullable=True)
    visit_date = Column(String, nullable=True)
    original_url = Column(Text, nullable=True)
    processed_url = Column(Text, nullable=True)
    image_size = Column(String, nullable=True)
    detected_sku = Column(Text, nullable=True)
    detections = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


def init_db():
    """Creates database tables if they do not exist."""
    Base.metadata.create_all(bind=engine)


def _detection_to_dict(det: Detection) -> Dict[str, Any]:
    """Helper to convert Detection ORM object into a dictionary matching DetectionResponse."""
    return {
        "id": det.id,
        "requestId": det.request_id,
        "project": det.project or "",
        "routeId": det.route_id or "",
        "imageKey": det.image_key.split(",") if det.image_key else [],
        "visitDate": det.visit_date or "",
        "originalImageUrl": det.original_url or "",
        "processedImageUrl": det.processed_url or "",
        "imageSize": [int(x) for x in det.image_size.split(",")] if det.image_size else [],
        "detectedSKU": json.loads(det.detected_sku or "{}"),
        "detections": json.loads(det.detections or "[]"),
        "createdAt": det.created_at.isoformat() if det.created_at else "",
    }


def save_detection(data: Dict[str, Any]) -> Dict[str, Any]:
    """Saves detection result to the database with transaction safety."""
    db = SessionLocal()
    try:
        req_id = data.get("requestId") or data.get("request_id") or str(datetime.now(timezone.utc).timestamp())
        image_key = data.get("imageKey")
        if isinstance(image_key, list):
            image_key_str = ",".join(str(k) for k in image_key)
        else:
            image_key_str = str(image_key or "")

        det = Detection(
            request_id=req_id,
            project=data.get("project"),
            route_id=data.get("routeId"),
            image_key=image_key_str,
            visit_date=data.get("visitDate"),
            original_url=data.get("originalImageUrl"),
            processed_url=data.get("processedImageUrl"),
            image_size=",".join(str(x) for x in (data.get("imageSize") or [])),
            detected_sku=json.dumps(data.get("detectedSKU") or {}),
            detections=json.dumps(data.get("detections") or []),
        )
        db.add(det)
        db.commit()
        db.refresh(det)
        return _detection_to_dict(det)
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to persist detection in database: {e}", exc_info=True)
        raise
    finally:
        db.close()


def get_detections(page: int = 1, page_size: int = 12) -> Tuple[List[Dict[str, Any]], int]:
    """Retrieves paginated detection records ordered by creation date descending."""
    db = SessionLocal()
    try:
        total = db.query(Detection).count()
        offset = max(0, (page - 1) * page_size)
        items = (
            db.query(Detection)
            .order_by(Detection.created_at.desc())
            .offset(offset)
            .limit(page_size)
            .all()
        )
        results = [_detection_to_dict(det) for det in items]
        return results, total
    except Exception as e:
        logger.error(f"Failed to query detections: {e}", exc_info=True)
        raise
    finally:
        db.close()


def delete_detection(request_id: str) -> bool:
    """Deletes detection record and its processed image from disk."""
    db = SessionLocal()
    try:
        det = db.query(Detection).filter(Detection.request_id == request_id).first()
        if not det:
            return False

        # Safely remove associated processed image from disk
        if det.processed_url:
            try:
                filename = os.path.basename(det.processed_url)
                file_path = os.path.join(DOWNLOAD_DIR, filename)
                if os.path.exists(file_path):
                    os.remove(file_path)
                    logger.info(f"Cleaned up processed image from disk: {file_path}")
            except OSError as img_err:
                logger.warning(f"Failed to remove processed image file on delete: {img_err}")

        db.delete(det)
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to delete detection with requestId '{request_id}': {e}", exc_info=True)
        raise
    finally:
        db.close()


def get_analytics_summary() -> Dict[str, Any]:
    """Computes aggregate analytics over all saved detection records."""
    db = SessionLocal()
    try:
        total_audits = db.query(Detection).count()
        all_records = db.query(Detection).order_by(Detection.created_at.desc()).all()

        total_objects = 0
        total_defects = 0
        clean_audits = 0
        conf_sum = 0.0
        conf_count = 0
        defect_breakdown: Dict[str, int] = {}
        category_breakdown: Dict[str, int] = {}

        # Known defect classes in retail compliance
        defect_class_keys = {
            "Backlit Not Functional", "backlit_not_functional",
            "BWU Damage", "sheet_damaged",
            "CAN Compartment Damage", "compartment_damage",
            "Paint Fade Off", "paint_fade_off",
            "Visibility Hidden With Others Items", "Visibility_hidden_other_items",
            "ZYN Logo Damage", "logo_damage",
            "Asset Available Not Deployed", "non_compliant"
        }

        for det in all_records:
            proj = det.project or "General"
            category_breakdown[proj] = category_breakdown.get(proj, 0) + 1

            try:
                detections_list = json.loads(det.detections or "[]")
            except Exception:
                detections_list = []

            total_objects += len(detections_list)
            audit_has_defect = False

            for item in detections_list:
                cname = item.get("class_name", "")
                conf = item.get("confidence", 0.0)
                if conf:
                    conf_sum += conf
                    conf_count += 1

                if cname in defect_class_keys or "damage" in cname.lower() or "not functional" in cname.lower():
                    audit_has_defect = True
                    total_defects += 1
                    defect_breakdown[cname] = defect_breakdown.get(cname, 0) + 1

            if not audit_has_defect and len(detections_list) > 0:
                clean_audits += 1

        compliance_rate = round((clean_audits / total_audits * 100), 1) if total_audits > 0 else 100.0
        avg_confidence = round((conf_sum / conf_count), 2) if conf_count > 0 else 0.0

        return {
            "total_audits": total_audits,
            "total_objects_detected": total_objects,
            "total_defects": total_defects,
            "clean_audits": clean_audits,
            "compliance_rate": compliance_rate,
            "avg_confidence": avg_confidence,
            "defect_breakdown": defect_breakdown,
            "project_breakdown": category_breakdown,
        }
    except Exception as e:
        logger.error(f"Failed to generate analytics summary: {e}", exc_info=True)
        return {
            "total_audits": 0,
            "total_objects_detected": 0,
            "total_defects": 0,
            "clean_audits": 0,
            "compliance_rate": 100.0,
            "avg_confidence": 0.0,
            "defect_breakdown": {},
            "project_breakdown": {},
        }
    finally:
        db.close()
