import logging
from typing import Dict, Any, List
import os
from app.core.knowledge_base import KnowledgeBase
from langchain.schema import Document
from langchain_community.document_loaders import PyPDFLoader

logger = logging.getLogger(__name__)


class PDFLoader:
    """
    Tool for loading and processing PDF documents.
    Extracts text content from PDF files.
    """

    def __init__(self, knowledge_base: KnowledgeBase):
        """
        Initialize the PDF loader.

        Args:
            knowledge_base: Knowledge base to store processed documents
        """
        self.knowledge_base = knowledge_base
        logger.info("Initialized PDF loader")

    async def load_document(self, file_path: str) -> List[Document]:
        """
        Load and parse a PDF document.

        Args:
            file_path: Path to the PDF file

        Returns:
            List of Document objects containing the PDF content

        Raises:
            ValueError: If file is not a valid PDF
        """
        logger.info(f"Loading PDF document from {file_path}")

        try:
            # Load PDF using PyPDFLoader
            loader = PyPDFLoader(file_path)
            documents = loader.load()
            
            return documents
        except Exception as e:
            logger.error(f"Error loading PDF document: {e}", exc_info=True)
            raise ValueError(f"Failed to load PDF document: {str(e)}")

    async def process_document(self, documents: List[Document], file_name: str) -> None:
        """
        Process PDF documents and add to knowledge base.

        Args:
            documents: List of Document objects from the PDF
            file_name: Original filename
        """
        logger.info(f"Processing PDF document: {file_name}")

        try:
            # Add each document to the knowledge base
            for i, doc in enumerate(documents):
                metadata = {
                    "source": file_name,
                    "page": i + 1,
                    "file_type": "pdf",
                    "document_type": "pdf"
                }
                
                # Update metadata with any existing metadata
                if doc.metadata:
                    metadata.update(doc.metadata)
                
                await self.knowledge_base.add_document(doc.page_content, metadata)
            
            logger.info(f"Successfully processed PDF document: {file_name}")
        except Exception as e:
            logger.error(f"Error processing PDF document: {e}", exc_info=True)
            raise 