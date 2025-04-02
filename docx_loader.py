from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, BackgroundTasks, Form
from fastapi.responses import JSONResponse
import logging
import uuid
import os
import shutil
from pathlib import Path
import tempfile
from typing import Optional
from app.dependencies import get_agent_factory, verify_api_key, get_knowledge_base
from app.core.agent_factory import AgentFactory
from app.core.knowledge_base import KnowledgeBase
from app.tools.document_loader_factory import DocumentLoaderFactory

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/upload")
async def upload_document(
        background_tasks: BackgroundTasks,
        file: Optional[UploadFile] = File(None),
        url: Optional[str] = Form(None),
        agent_factory: AgentFactory = Depends(get_agent_factory),
        knowledge_base: KnowledgeBase = Depends(get_knowledge_base)
):
    """
    Upload and process a document file or scrape content from a URL.
    The content will be loaded into the knowledge base for agent use.
    Supports various file types including OpenAPI, PDF, text, Word, and HTML.
    Also supports scraping content from websites.
    """
    if not file and not url:
        raise HTTPException(
            status_code=400,
            detail="Either a file or a URL must be provided"
        )
    
    if file and url:
        raise HTTPException(
            status_code=400,
            detail="Please provide either a file or a URL, not both"
        )
    
    try:
        if file:
            logger.info(f"Received file upload: {file.filename}")
            
            # Create temp file
            temp_dir = Path(tempfile.gettempdir())
            file_ext = os.path.splitext(file.filename)[1].lower()
            temp_file = temp_dir / f"{uuid.uuid4()}{file_ext}"

            # Save uploaded file
            with open(temp_file, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            # Process file in background
            background_tasks.add_task(
                process_document_file,
                str(temp_file),
                file.filename,
                knowledge_base
            )
            
            return JSONResponse(
                status_code=202,
                content={
                    "message": "Document accepted for processing",
                    "filename": file.filename
                }
            )
        else:
            logger.info(f"Received URL for scraping: {url}")
            
            # Process URL in background
            background_tasks.add_task(
                process_document_file,
                url,
                url,
                knowledge_base
            )
            
            return JSONResponse(
                status_code=202,
                content={
                    "message": "URL accepted for scraping",
                    "url": url
                }
            )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error handling document upload: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Error processing document: {str(e)}"
        )
    finally:
        if file:
            file.file.close()


async def process_document_file(file_path: str, original_filename: str, knowledge_base: KnowledgeBase):
    """
    Process a document file or URL and load into knowledge base.
    """
    try:
        logger.info(f"Processing document: {original_filename}")

        # Ensure knowledge base is initialized
        if not knowledge_base.vectorstore:
            logger.info("Knowledge base not initialized in background task, initializing now")
            await knowledge_base.initialize()

        # Get the appropriate loader for this file type or URL
        loader = DocumentLoaderFactory.get_loader(file_path, knowledge_base)
        
        # Check if this is an OpenAPI loader (which has a different interface)
        if hasattr(loader, 'load_spec'):
            # Load and validate the spec
            spec = await loader.load_spec(file_path)
            
            # Process the spec and add to knowledge base
            await loader.process_spec(spec, original_filename)
        else:
            # Load the document
            documents = await loader.load_document(file_path)
            
            # Process the document and add to knowledge base
            await loader.process_document(documents, original_filename)

        logger.info(f"Successfully processed document: {original_filename}")

    except ValueError as e:
        logger.error(f"Error processing document {original_filename}: {e}", exc_info=True)
    except Exception as e:
        logger.error(f"Error processing document {original_filename}: {e}", exc_info=True)
    finally:
        # Clean up temporary file if it exists and is not a URL
        if not DocumentLoaderFactory._is_url(file_path):
            try:
                if os.path.exists(file_path):
                    os.unlink(file_path)
            except Exception as e:
                logger.error(f"Error removing temporary file {file_path}: {e}")


# Keep the original OpenAPI-specific endpoint for backward compatibility
@router.post("/openapi-spec")
async def upload_openapi_spec(
        background_tasks: BackgroundTasks,
        file: UploadFile = File(...),
        agent_factory: AgentFactory = Depends(get_agent_factory),
        knowledge_base: KnowledgeBase = Depends(get_knowledge_base)
):
    """
    Upload and process an OpenAPI specification file.
    The file will be loaded into the knowledge base for agent use.
    """
    logger.info(f"Received OpenAPI file upload: {file.filename}")

    try:
        # Validate file extension
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in ['.json', '.yaml', '.yml']:
            raise HTTPException(
                status_code=400,
                detail="Invalid file format. Only JSON and YAML OpenAPI files are supported."
            )

        # Create temp file
        temp_dir = Path(tempfile.gettempdir())
        temp_file = temp_dir / f"{uuid.uuid4()}{file_ext}"

        # Save uploaded file
        with open(temp_file, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Process file in background
        background_tasks.add_task(
            process_document_file,
            str(temp_file),
            file.filename,
            knowledge_base
        )

        return JSONResponse(
            status_code=202,
            content={
                "message": "OpenAPI specification accepted for processing",
                "filename": file.filename
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error handling OpenAPI upload: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Error processing OpenAPI file"
        )
    finally:
        file.file.close()
