from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import os
import logging
from app.config import settings
from app.routers.chat import router as chat_router
from app.routers.document import router as document_router
from app.dependencies import get_chroma_service

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code goes here (previously in on_event("startup"))
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    # Initialize Chroma DB on startup
    get_chroma_service()
    logger.info("ChromaDB initialized successfully")
    yield
# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Agent-based chatbot using LangGraph and FastAPI",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include chat router only
app.include_router(chat_router)
app.include_router(document_router)

# Create necessary directories
os.makedirs(settings.VECTOR_DB_DIR, exist_ok=True)



@app.get("/")
async def root():
    return {
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )