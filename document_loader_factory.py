import logging
import os
from typing import Dict, Type, Any
from urllib.parse import urlparse
from app.core.knowledge_base import KnowledgeBase
from app.tools.openapi_loader import OpenAPILoader
from app.tools.pdf_loader import PDFLoader
from app.tools.text_loader import TextDocumentLoader
from app.tools.docx_loader import DocxLoader
from app.tools.html_loader import HTMLLoader

logger = logging.getLogger(__name__)


class DocumentLoaderFactory:
    """
    Factory for creating document loaders based on file type.
    """

    # Map of file extensions to loader classes
    LOADER_MAP: Dict[str, Type[Any]] = {
        # OpenAPI files
        '.json': OpenAPILoader,
        '.yaml': OpenAPILoader,
        '.yml': OpenAPILoader,
        
        # PDF files
        '.pdf': PDFLoader,
        
        # Text files
        '.txt': TextDocumentLoader,
        '.md': TextDocumentLoader,
        '.csv': TextDocumentLoader,
        
        # Word documents
        '.docx': DocxLoader,
        '.doc': DocxLoader,
        
        # HTML files
        '.html': HTMLLoader,
        '.htm': HTMLLoader,
    }

    @classmethod
    def get_loader(cls, file_path: str, knowledge_base: KnowledgeBase) -> Any:
        """
        Get the appropriate loader for a file based on its extension.

        Args:
            file_path: Path to the file or URL
            knowledge_base: Knowledge base to store processed documents

        Returns:
            An instance of the appropriate loader

        Raises:
            ValueError: If no loader is available for the file type
        """
        # Check if the file_path is a URL
        if cls._is_url(file_path):
            # For URLs, we'll use the HTML loader for web scraping
            logger.info(f"Detected URL: {file_path}, using HTML loader for scraping")
            return HTMLLoader(knowledge_base)
        
        # Get file extension
        ext = os.path.splitext(file_path)[1].lower()
        
        # Check if we have a loader for this extension
        if ext not in cls.LOADER_MAP:
            supported_extensions = ', '.join(cls.LOADER_MAP.keys())
            raise ValueError(
                f"Unsupported file type: {ext}. "
                f"Supported file types are: {supported_extensions}"
            )
        
        # Get the loader class
        loader_class = cls.LOADER_MAP[ext]
        
        # Create and return an instance
        logger.info(f"Creating {loader_class.__name__} for file: {file_path}")
        return loader_class(knowledge_base)
    
    @staticmethod
    def _is_url(path: str) -> bool:
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