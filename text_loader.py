import logging
from typing import Dict, Any, List
import os
from app.core.knowledge_base import KnowledgeBase
from langchain.schema import Document
from langchain_community.document_loaders import TextLoader

logger = logging.getLogger(__name__)


class TextDocumentLoader:
    """
    Tool for loading and processing text documents.
    Extracts content from text files.
    """

    def __init__(self, knowledge_base: KnowledgeBase):
        """
        Initialize the text loader.

        Args:
            knowledge_base: Knowledge base to store processed documents
        """
        self.knowledge_base = knowledge_base
        logger.info("Initialized text loader")

    async def load_document(self, file_path: str) -> List[Document]:
        """
        Load and parse a text document.

        Args:
            file_path: Path to the text file

        Returns:
            List of Document objects containing the text content

        Raises:
            ValueError: If file is not a valid text file
        """
        logger.info(f"Loading text document from {file_path}")

        try:
            # Load text using TextLoader from langchain
            loader = TextLoader(file_path)
            documents = loader.load()
            
            return documents
        except Exception as e:
            logger.error(f"Error loading text document: {e}", exc_info=True)
            raise ValueError(f"Failed to load text document: {str(e)}")

    async def process_document(self, documents: List[Document], file_name: str) -> None:
        """
        Process text documents and add to knowledge base.

        Args:
            documents: List of Document objects from the text file
            file_name: Original filename
        """
        logger.info(f"Processing text document: {file_name}")

        try:
            # Add each document to the knowledge base
            for i, doc in enumerate(documents):
                metadata = {
                    "source": file_name,
                    "file_type": "text",
                    "document_type": "text"
                }
                
                # Update metadata with any existing metadata
                if doc.metadata:
                    metadata.update(doc.metadata)
                
                await self.knowledge_base.add_document(doc.page_content, metadata)
            
            logger.info(f"Successfully processed text document: {file_name}")
        except Exception as e:
            logger.error(f"Error processing text document: {e}", exc_info=True)
            raise 