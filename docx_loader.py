import os
import logging
from typing import List, Dict, Any, Optional
import json
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.schema import Document
import time

from app.config import get_settings

logger = logging.getLogger(__name__)


class KnowledgeBase:
    """
    Knowledge base for storing and retrieving documents using vector search.
    Handles loading, chunking, and querying API documentation.
    """

    def __init__(self, docs_path: Optional[str] = None, embedding_model: Optional[str] = None):
        """
        Initialize the knowledge base.

        Args:
            docs_path: Path to documentation files
            embedding_model: OpenAI embedding model name
        """
        self.instance_id = id(self)
        logger.info(f"Creating KnowledgeBase instance {self.instance_id}")
        self.settings = get_settings()
        self.docs_path = docs_path or self.settings.DOCS_PATH
        self.embedding_model = embedding_model or self.settings.EMBEDDING_MODEL
        self.persist_dir = self.settings.CHROMA_PERSIST_DIRECTORY
        self.vectorstore = None
        self.embeddings = None
        self._initialized = False
        
        # Document batching mechanism
        self._document_buffer = []
        self._batch_size = 10  # Process documents in batches of 10
        self._last_batch_time = time.time()
        self._batch_timeout = 5  # Process batch after 5 seconds even if not full
        
        logger.info(f"Initializing knowledge base with docs path: {self.docs_path}")

    async def initialize(self) -> None:
        """Initialize the knowledge base resources."""
        try:
            # Ensure directories exist
            os.makedirs(self.persist_dir, exist_ok=True)
            os.makedirs(self.docs_path, exist_ok=True)

            logger.info(f"Initializing embeddings with model: {self.embedding_model}")
            # Initialize embeddings
            self.embeddings = OpenAIEmbeddings(
                model=self.embedding_model,
                openai_api_key=self.settings.OPENAI_API_KEY
            )
            logger.info("Embeddings initialized successfully")

            try:
                # Try creating a test embedding to verify API access
                logger.info("Testing embedding API connection...")
               # test_embedding = await self.embeddings.aembed_query("test")
                #logger.info(f"Test embedding successful, dimension: {len(test_embedding)}")
            except Exception as e:
                logger.error(f"Error testing embeddings API: {e}", exc_info=True)
                raise RuntimeError(f"Failed to connect to OpenAI Embeddings API: {e}")

            logger.info(f"Initializing vector store at {self.persist_dir}")
            try:
                self.vectorstore = Chroma(
                    persist_directory=self.persist_dir,
                    embedding_function=self.embeddings
                )
                logger.info("Vector store initialized successfully")
            except Exception as e:
                logger.error(f"Error initializing Chroma vector store: {e}", exc_info=True)
                raise RuntimeError(f"Failed to initialize Chroma: {e}")

            self._initialized = True
            logger.info("Knowledge base fully initialized")

        except Exception as e:
            logger.error(f"Failed to initialize knowledge base: {e}", exc_info=True)
            self.vectorstore = None
            raise

    async def load_documents(self) -> None:
        """
        Load documents from the docs path, chunk them, and add to the vector store.
        """
        try:
            # Create document loader
            loader = DirectoryLoader(
                self.docs_path,
                glob="**/*.{json,md,txt}",
                loader_cls=TextLoader
            )

            # Load documents
            documents = loader.load()
            logger.info(f"Loaded {len(documents)} documents from {self.docs_path}")

            # Create text splitter
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=self.settings.DOCS_CHUNK_SIZE,
                chunk_overlap=self.settings.DOCS_CHUNK_OVERLAP,
                separators=["\n\n", "\n", " ", ""]
            )

            # Split documents into chunks
            chunks = text_splitter.split_documents(documents)
            logger.info(f"Split into {len(chunks)} chunks")

            # Add metadata to chunks
            for chunk in chunks:
                # Extract relative path for better identification
                rel_path = os.path.relpath(chunk.metadata["source"], self.docs_path)
                chunk.metadata["path"] = rel_path

                # Add file type
                chunk.metadata["filetype"] = os.path.splitext(rel_path)[1]

                # Try to identify section from JSON files
                if chunk.metadata["filetype"] == ".json":
                    try:
                        content_json = json.loads(chunk.page_content)
                        if "info" in content_json:
                            chunk.metadata["api_version"] = content_json.get("info", {}).get("version", "unknown")
                            chunk.metadata["api_title"] = content_json.get("info", {}).get("title", "unknown")
                    except json.JSONDecodeError:
                        pass

            # Use batch processing for embeddings
            logger.info(f"Adding {len(chunks)} chunks to vector store using batch processing")
            
            # Add chunks to vector store in batches
            batch_size = 100  # Process in batches of 100 chunks
            for i in range(0, len(chunks), batch_size):
                batch = chunks[i:i+batch_size]
                logger.info(f"Processing batch {i//batch_size + 1} of {(len(chunks) + batch_size - 1)//batch_size} ({len(batch)} chunks)")
                self.vectorstore.add_documents(batch)

            # Persist vector store
            self.vectorstore.persist()
            logger.info("Documents processed and added to vector store")

        except Exception as e:
            logger.error(f"Error loading documents: {e}", exc_info=True)
            raise

    async def search(self, query: str, top_k: int = 5, filter_criteria: Optional[Dict[str, Any]] = None) -> List[
        Document]:
        """
        Search the knowledge base for relevant documents.

        Args:
            query: Search query
            top_k: Number of results to return
            filter_criteria: Optional filter criteria for metadata

        Returns:
            List of relevant documents
        """
        if not self._initialized or not self.vectorstore:
            logger.warning("Knowledge base not fully initialized, returning empty results")
            return []

        try:
            # Use batch processing for embeddings
            logger.info(f"Searching for '{query[:50]}...' using batch processing")
            
            results = self.vectorstore.similarity_search(
                query=query,
                k=top_k,
                filter=filter_criteria
            )
            logger.info(f"Search for '{query[:50]}...' returned {len(results)} results")
            return results
        except Exception as e:
            logger.error(f"Error searching knowledge base: {e}", exc_info=True)
            return []

    async def add_document(self, content: str, metadata: Dict[str, Any]) -> None:
        """
        Add a new document to the knowledge base.
        Documents are collected in a buffer and processed in batches for efficiency.
        """
        logger.info(f"Adding document to KnowledgeBase instance {self.instance_id}")

        if not hasattr(self, 'vectorstore') or self.vectorstore is None:
            logger.error(f"Failed to initialize vector store for add_document")
            # Try to reinitialize
            try:
                logger.info(f"Attempting to reinitialize vectorstore in instance {self.instance_id}")
                await self.initialize()
            except Exception as e:
                logger.error(f"Reinitialization failed: {e}")
                return

        if not hasattr(self, 'vectorstore') or self.vectorstore is None:
            logger.error(f"Vector store still not available after reinitialization")
            return

        try:
            # Create document
            document = Document(page_content=content, metadata=metadata)
            
            # Add to buffer
            self._document_buffer.append(document)
            
            # Check if we should process the batch
            current_time = time.time()
            time_since_last_batch = current_time - self._last_batch_time
            
            # Process batch if buffer is full or timeout reached
            if len(self._document_buffer) >= self._batch_size or time_since_last_batch >= self._batch_timeout:
                await self._process_document_batch()
                
        except Exception as e:
            logger.error(f"Error adding document: {e}", exc_info=True)
    
    async def _process_document_batch(self) -> None:
        """
        Process the current document buffer in a batch.
        """
        if not self._document_buffer:
            return
            
        try:
            # Create text splitter
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=self.settings.DOCS_CHUNK_SIZE,
                chunk_overlap=self.settings.DOCS_CHUNK_OVERLAP
            )
            
            # Split all documents in the buffer
            all_chunks = []
            for doc in self._document_buffer:
                chunks = text_splitter.split_documents([doc])
                all_chunks.extend(chunks)
            
            # Log batch processing
            logger.info(f"Processing batch of {len(self._document_buffer)} documents, creating {len(all_chunks)} chunks")
            
            # Process in smaller sub-batches if needed
            sub_batch_size = 100
            for i in range(0, len(all_chunks), sub_batch_size):
                sub_batch = all_chunks[i:i+sub_batch_size]
                logger.info(f"Adding sub-batch {i//sub_batch_size + 1} of {(len(all_chunks) + sub_batch_size - 1)//sub_batch_size} ({len(sub_batch)} chunks)")
                self.vectorstore.add_documents(sub_batch)
            
            # Persist changes
            self.vectorstore.persist()
            
            # Clear buffer and update last batch time
            self._document_buffer = []
            self._last_batch_time = time.time()
            
            logger.info(f"Successfully processed batch of documents")
            
        except Exception as e:
            logger.error(f"Error processing document batch: {e}", exc_info=True)
            # Keep documents in buffer for retry
            logger.info("Keeping documents in buffer for retry")
