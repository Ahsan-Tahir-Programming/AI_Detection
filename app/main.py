from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.logger import logger
from app.core.config import DOWNLOAD_DIR
from app.services.inference import inference_service
from app.api.routes import router

# --- Lifespan: Load Models on Startup ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("App is starting up...")
    # Initialize database and preload ML models
    try:
        from app.services import db as db_service
        db_service.init_db()
        logger.info("Database initialized")
    except Exception as e:
        logger.error(f"DB init failed: {e}", exc_info=True)

    inference_service.preload_models()
    yield
    logger.info("App is shutting down...")

# --- App Initialization ---
app = FastAPI(lifespan=lifespan)

# --- CORS Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition", "Content-Type"],  # Allow download headers
)

# --- Mount Static Files ---
app.mount("/download", StaticFiles(directory=DOWNLOAD_DIR), name="download")

# --- Include Routers ---
app.include_router(router)