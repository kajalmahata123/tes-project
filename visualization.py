# core/database/chroma_client.py
import chromadb
from chromadb.config import Settings
from functools import lru_cache

@lru_cache()
def get_chroma_client(
    persist_directory: str = '/Users/kajalmahata/smart_QL/chroma_data'
):
    return chromadb.Client(Settings(
        persist_directory=persist_directory,
        anonymized_telemetry=False,
        allow_reset=True,
        is_persistent=True
    ))
