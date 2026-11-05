"""Automated backend test suite covering endpoints, model discovery, and database operations."""
import sys
import os
import unittest
import asyncio

# Ensure project root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.api.routes import health_check, list_models, list_detections, root, get_analytics
from app.services.inference import inference_service
from app.services import db


class TestBackend(unittest.TestCase):
    def setUp(self):
        db.init_db()

    def test_health_check(self):
        response = asyncio.run(health_check())
        self.assertEqual(response["status"], "ok")
        self.assertEqual(response["service"], "AI Detection API")

    def test_root_endpoint(self):
        response = asyncio.run(root())
        self.assertIn("message", response)
        self.assertIn("docs", response)

    def test_model_discovery(self):
        models_data = inference_service.get_available_models()
        self.assertIn("models", models_data)
        self.assertIn("details", models_data)
        self.assertIn("zyn", models_data["models"])

    def test_analytics_endpoint(self):
        response = asyncio.run(get_analytics())
        self.assertTrue(response["success"])
        self.assertIn("total_audits", response["data"])
        self.assertIn("compliance_rate", response["data"])

    def test_database_lifecycle(self):
        # Create a test detection record
        test_data = {
            "requestId": "test-uuid-12345",
            "project": "test_project",
            "routeId": "route_test_01",
            "imageKey": ["key_01"],
            "imageSize": [640, 480],
            "visitDate": "2026-10-27",
            "originalImageUrl": "https://example.com/test.jpg",
            "processedImageUrl": "http://127.0.0.1:8000/download/test.jpg",
            "detectedSKU": {"test_sku": {"detected": True, "count": 1, "coordinates": []}},
            "detections": [],
        }

        # 1. Save
        saved = db.save_detection(test_data)
        self.assertEqual(saved["requestId"], "test-uuid-12345")
        self.assertEqual(saved["routeId"], "route_test_01")

        # 2. Query
        items, total = db.get_detections(page=1, page_size=10)
        self.assertGreaterEqual(total, 1)
        found = any(item["requestId"] == "test-uuid-12345" for item in items)
        self.assertTrue(found)

        # 3. Delete
        deleted = db.delete_detection("test-uuid-12345")
        self.assertTrue(deleted)

        # Verify deletion
        items_after, _ = db.get_detections(page=1, page_size=10)
        found_after = any(item["requestId"] == "test-uuid-12345" for item in items_after)
        self.assertFalse(found_after)


if __name__ == "__main__":
    unittest.main()
