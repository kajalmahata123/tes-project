import logging
from typing import Dict, Any, List, Optional
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from app.core.knowledge_base import KnowledgeBase
from langchain.schema import Document
from langchain_community.document_loaders import UnstructuredHTMLLoader, WebBaseLoader

logger = logging.getLogger(__name__)


class HTMLLoader:
    """
    Tool for loading and processing HTML documents.
    Extracts content from HTML files and can scrape content from websites.
    """

    def __init__(self, knowledge_base: KnowledgeBase):
        """
        Initialize the HTML loader.

        Args:
            knowledge_base: Knowledge base to store processed documents
        """
        self.knowledge_base = knowledge_base
        logger.info("Initialized HTML loader")

    async def load_document(self, file_path: str) -> List[Document]:
        """
        Load and parse an HTML document.

        Args:
            file_path: Path to the HTML file or URL to scrape

        Returns:
            List of Document objects containing the HTML content

        Raises:
            ValueError: If file is not a valid HTML file or URL
        """
        logger.info(f"Loading HTML document from {file_path}")

        try:
            # Check if the file_path is a URL
            if self._is_url(file_path):
                return await self._scrape_url(file_path)
            else:
                # Load local HTML file using UnstructuredHTMLLoader
                loader = UnstructuredHTMLLoader(file_path)
                documents = loader.load()
                return documents
        except Exception as e:
            logger.error(f"Error loading HTML document: {e}", exc_info=True)
            raise ValueError(f"Failed to load HTML document: {str(e)}")

    async def _scrape_url(self, url: str) -> List[Document]:
        """
        Scrape content from a URL.

        Args:
            url: URL to scrape

        Returns:
            List of Document objects containing the scraped content
        """
        logger.info(f"Scraping content from URL: {url}")
        
        try:
            # Use WebBaseLoader for scraping
            loader = WebBaseLoader(url)
            documents = loader.load()
            
            # Add URL to metadata
            for doc in documents:
                if not doc.metadata:
                    doc.metadata = {}
                doc.metadata["url"] = url
                doc.metadata["domain"] = urlparse(url).netloc
            
            return documents
        except Exception as e:
            logger.error(f"Error scraping URL {url}: {e}", exc_info=True)
            raise ValueError(f"Failed to scrape URL: {str(e)}")

    def _is_url(self, path: str) -> bool:
        """
        Check if a path is a URL.

        Args:
            path: Path to check

        Returns:
            True if the path is a URL, False otherwise
        """
        try:
            result = urlparse(path)
            return all([result.scheme, result.netloc])
        except:
            return False

    async def process_document(self, documents: List[Document], file_name: str) -> None:
        """
        Process HTML documents and add to knowledge base.

        Args:
            documents: List of Document objects from the HTML file
            file_name: Original filename or URL
        """
        logger.info(f"Processing HTML document: {file_name}")

        try:
            # Add each document to the knowledge base
            for i, doc in enumerate(documents):
                metadata = {
                    "source": file_name,
                    "file_type": "html",
                    "document_type": "html"
                }
                
                # Update metadata with any existing metadata
                if doc.metadata:
                    metadata.update(doc.metadata)
                
                await self.knowledge_base.add_document(doc.page_content, metadata)
            
            logger.info(f"Successfully processed HTML document: {file_name}")
        except Exception as e:
            logger.error(f"Error processing HTML document: {e}", exc_info=True)
            raise 