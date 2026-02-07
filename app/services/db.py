import os
import json
from datetime import datetime
from typing import List, Tuple
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import APP_DIR

# Ensure database directory exists
DB_DIR = os.path.join(APP_DIR, 'database')
os.makedirs(DB_DIR, exist_ok=True)
DB_PATH = os.path.join(DB_DIR, 'detections.db')
DB_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Detection(Base):
    __tablename__ = "detections"
    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(String, unique=True, index=True, nullable=False)
    project = Column(String)
    route_id = Column(String)
    image_key = Column(String)
    visit_date = Column(String)
    original_url = Column(Text)
    processed_url = Column(Text)
    image_size = Column(String)
    detected_sku = Column(Text)
    detections = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


def init_db():
    Base.metadata.create_all(bind=engine)


def save_detection(data: dict):
    """Save detection result to DB and return saved record as dict"""
    db = SessionLocal()
    try:
        det = Detection(
            request_id=data.get('requestId') or data.get('request_id') or str(datetime.utcnow().timestamp()),
            project=data.get('project'),
            route_id=data.get('routeId'),
            image_key=','.join(data.get('imageKey') or []) if isinstance(data.get('imageKey'), list) else data.get('imageKey'),
            visit_date=data.get('visitDate'),
            original_url=data.get('originalImageUrl'),
            processed_url=data.get('processedImageUrl'),
            image_size=','.join([str(x) for x in (data.get('imageSize') or [])]),
            detected_sku=json.dumps(data.get('detectedSKU') or {}),
            detections=json.dumps(data.get('detections') or []),
        )
        db.add(det)
        db.commit()
        db.refresh(det)
        return {
            'id': det.id,
            'requestId': det.request_id,
            'project': det.project,
            'routeId': det.route_id,
            'imageKey': det.image_key.split(',') if det.image_key else [],
            'visitDate': det.visit_date,
            'originalImageUrl': det.original_url,
            'processedImageUrl': det.processed_url,
            'imageSize': [int(x) for x in det.image_size.split(',')] if det.image_size else [],
            'detectedSKU': json.loads(det.detected_sku or '{}'),
            'detections': json.loads(det.detections or '[]'),
            'createdAt': det.created_at.isoformat(),
        }
    finally:
        db.close()


def get_detections(page: int = 1, page_size: int = 10) -> Tuple[List[dict], int]:
    db = SessionLocal()
    try:
        total = db.query(Detection).count()
        items = db.query(Detection).order_by(Detection.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
        results = []
        for det in items:
            results.append({
                'id': det.id,
                'requestId': det.request_id,
                'project': det.project,
                'routeId': det.route_id,
                'imageKey': det.image_key.split(',') if det.image_key else [],
                'visitDate': det.visit_date,
                'originalImageUrl': det.original_url,
                'processedImageUrl': det.processed_url,
                'imageSize': [int(x) for x in det.image_size.split(',')] if det.image_size else [],
                'detectedSKU': json.loads(det.detected_sku or '{}'),
                'detections': json.loads(det.detections or '[]'),
                'createdAt': det.created_at.isoformat(),
            })
        return results, total
    finally:
        db.close()


def delete_detection(request_id: str) -> bool:
    db = SessionLocal()
    try:
        det = db.query(Detection).filter(Detection.request_id == request_id).first()
        if not det:
            return False
        # Optionally remove file
        try:
            if det.processed_url:
                # processed_url is like http://.../download/<filename>
                filename = os.path.basename(det.processed_url)
                file_path = os.path.join(os.path.dirname(DB_PATH), '..', 'app', 'download', filename)
                if os.path.exists(file_path):
                    os.remove(file_path)
        except Exception:
            pass
        db.delete(det)
        db.commit()
        return True
    finally:
        db.close()