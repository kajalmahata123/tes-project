import logging
from typing import Dict, Any, List
import os
from app.core.knowledge_base import KnowledgeBase
from langchain.schema import Document
from langchain_community.document_loaders import Docx2txtLoader

logger = logging.getLogger(__name__)


class DocxLoader:
    """
    Tool for loading and processing Word documents.
    Extracts content from DOCX files.
    """

    def __init__(self, knowledge_base: KnowledgeBase):
        """
        Initialize the Word document loader.

        Args:
            knowledge_base: Knowledge base to store processed documents
        """
        self.knowledge_base = knowledge_base
        logger.info("Initialized Word document loader")

    async def load_document(self, file_path: str) -> List[Document]:
        """
        Load and parse a Word document.

        Args:
            file_path: Path to the DOCX file

        Returns:
            List of Document objects containing the document content

        Raises:
            ValueError: If file is not a valid DOCX file
        """
        logger.info(f"Loading Word document from {file_path}")

        try:
            # Load DOCX using Docx2txtLoader
            loader = Docx2txtLoader(file_path)
            documents = loader.load()
            
            return documents
        except Exception as e:
            logger.error(f"Error loading Word document: {e}", exc_info=True)
            raise ValueError(f"Failed to load Word document: {str(e)}")

    async def process_document(self, documents: List[Document], file_name: str) -> None:
        """
        Process Word documents and add to knowledge base.

        Args:
            documents: List of Document objects from the DOCX file
            file_name: Original filename
        """
        logger.info(f"Processing Word document: {file_name}")

        try:
            # Add each document to the knowledge base
            for i, doc in enumerate(documents):
                metadata = {
                    "source": file_name,
                    "file_type": "docx",
                    "document_type": "word"
                }
                
                # Update metadata with any existing metadata
                if doc.metadata:
                    metadata.update(doc.metadata)
                
                await self.knowledge_base.add_document(doc.page_content, metadata)
            
            logger.info(f"Successfully processed Word document: {file_name}")
        except Exception as e:
            logger.error(f"Error processing Word document: {e}", exc_info=True)
            raise 