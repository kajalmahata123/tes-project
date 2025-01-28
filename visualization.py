# main.py
import logging
from contextlib import asynccontextmanager
import uvicorn
from sqlalchemy import text
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from config import settings
from smart_ql.features.data_analysis.route.analysis_routes import data_analysis_router
from smart_ql.features.document_generator.route.ai_document_route import document_router
from smart_ql.features.query_intent.route.query_intent_route import intent_router
from smart_ql.features.query_suggestion.route.history import history_router
from smart_ql.features.query_suggestion.route.recomendation import query_recomendation_router
from smart_ql.features.schema_analyzer.routes.schema_analysis_endpoint import schema_extraction_router
from smart_ql.db.database import engine
from smart_ql.features.auth.api.auth import user_router
from smart_ql.features.data_source.routes.data_source_endpoint import datasource_router
from smart_ql.features.semantic_search.store_search_api import store_search_router
from smart_ql.routes.health import health_router

# Configure logging
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager for startup and shutdown events"""
    # Startup: Execute when the server starts
    logger.info("Starting up application...")
    try:
        # Test database connection
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            logger.info("Database connection successful!")
    except Exception as e:
        logger.error(f"Database connection failed: {str(e)}")
        raise

    yield  # Server is running and handling requests

    # Shutdown: Execute when the server stops
    logger.info("Shutting down application...")
    try:
        await engine.dispose()
        logger.info("Database connection closed successfully")
    except Exception as e:
        logger.error(f"Error closing database connection: {str(e)}")


async def catch_exceptions_middleware(request, call_next):
    """Global exception handler middleware"""
    try:
        return await call_next(request)
    except HTTPException as e:
        logger.warning(f"HTTP Exception: {str(e)}")
        return JSONResponse(
            status_code=e.status_code,
            content={"detail": e.detail}
        )
    except Exception as e:
        logger.error(f"Unhandled exception: {str(e)}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"}
        )


def create_application() -> FastAPI:
    """Create and configure the FastAPI application"""
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        docs_url=f"{settings.API_V1_STR}/docs",
        redoc_url=f"{settings.API_V1_STR}/redoc",
        lifespan=lifespan,
        openapi_url=f"{settings.API_V1_STR}/openapi.json"
    )

    # Add middlewares
    app.middleware("http")(catch_exceptions_middleware)

    # CORS middleware
    #if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        #allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_origins=["http://localhost:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Trusted Host middleware

    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=settings.ALLOWED_HOSTS
    )
    app.include_router(
        health_router,
        prefix="/health",
        tags=["Health Check"]
    )
    # Register routers
    app.include_router(
        user_router,
        prefix=settings.API_V1_STR,
        tags=["Authentication"]
    )
    app.include_router(
        datasource_router,
        prefix=settings.API_V1_STR+"/datasources",
        tags=["Data Sources"]
    )
    app.include_router(
        schema_extraction_router,
        prefix=settings.API_V1_STR + "/schema/analysis",
        tags=["Schema Analysis"])
    app.include_router(
        store_search_router,
        prefix=settings.API_V1_STR + "/vectorstore",
        tags=["Vector Store and Search And Query Generation"])
    app.include_router(
        intent_router,
        prefix=settings.API_V1_STR + "/query-analysis",
        tags=["Intent Analysis"])
    app.include_router(
        document_router,
        prefix=settings.API_V1_STR + "/document",
        tags=["Document"])
    app.include_router(
        query_recomendation_router,
        prefix=settings.API_V1_STR,
        tags=["Query Recommendation"]
    )
    app.include_router(
        history_router,
        prefix=settings.API_V1_STR,
        tags=["Query History"]
    )
    app.include_router(
        data_analysis_router,
        prefix=settings.API_V1_STR,
        tags=["Data Analysis"]
    )

    return app


def start_server():
    """Start the uvicorn server with port retry logic"""
    ports = settings.ALTERNATE_PORTS
    for port in ports:
        try:
            logger.info(f"Attempting to start server on port {port}...")
            uvicorn.run(
                "main:app",
                host=settings.HOST,
                port=port,
                reload=settings.DEBUG,
                lifespan="on",
                log_level=settings.LOG_LEVEL.lower(),
                access_log=settings.ACCESS_LOG
            )
            break
        except OSError as e:
            if port == ports[-1]:
                logger.error(f"All ports are in use. Last error: {str(e)}")
                raise
            logger.warning(f"Port {port} is in use, trying next port...")
        except Exception as e:
            logger.error(f"Error starting server: {str(e)}", exc_info=True)
            raise


app = create_application()

if __name__ == "__main__":
    start_server()
