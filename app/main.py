"""Main FastAPI application entry point with lifespan management and CORS middleware."""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app.core.logger import logger
from app.core.config import DOWNLOAD_DIR, ALLOWED_ORIGINS
from app.services.inference import inference_service
from app.api.routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown event handler."""
    logger.info("Starting up AI Detection Service...")

    # Initialize Database
    try:
        from app.services import db as db_service
        db_service.init_db()
        logger.info("Database initialized successfully.")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}", exc_info=True)

    # Preload YOLO models into memory
    try:
        inference_service.preload_models()
    except Exception as e:
        logger.error(f"Error during model preloading: {e}", exc_info=True)

    yield

    logger.info("Shutting down AI Detection Service...")


# Initialize FastAPI instance with OpenAPI documentation metadata
app = FastAPI(
    title="AI Object Detection API",
    description="Production-grade real-time YOLO object detection with persistence and image annotation.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# CORS Middleware
origins = ALLOWED_ORIGINS if ALLOWED_ORIGINS else ["*"]
allow_all = "*" in origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if allow_all else origins,
    allow_credentials=not allow_all,  # In production, credentials require explicit origin list
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition", "Content-Type"],
)

# Mount Static Files for direct processed image inspection
app.mount("/download", StaticFiles(directory=DOWNLOAD_DIR), name="download")

# Include API Routers
app.include_router(router)