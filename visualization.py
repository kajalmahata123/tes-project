import hashlib
import json
import chromadb
from chromadb.api.types import Documents, EmbeddingFunction
from chromadb.config import Settings
import numpy as np
from typing import List, Dict
import re
class BasicEmbeddingFunction(EmbeddingFunction):
    def __init__(self, dimension: int = 512):
        self.dimension = dimension
        self.word_vectors = {}

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        words = re.findall(r'\w+', text)
        return words

    def _hash_word(self, word: str) -> np.ndarray:
        if word not in self.word_vectors:
            seed = int(hashlib.md5(word.encode()).hexdigest(), 16) % (2 ** 32)
            np.random.seed(seed)
            self.word_vectors[word] = np.random.randn(self.dimension)
        return self.word_vectors[word]

    def __call__(self, texts: Documents) -> List[List[float]]:
        embeddings = []
        for text in texts:
            if not text:
                embeddings.append([0.0] * self.dimension)
                continue

            words = self._tokenize(str(text))
            if not words:
                embeddings.append([0.0] * self.dimension)
                continue

            vectors = np.array([self._hash_word(word) for word in words])
            embedding = np.mean(vectors, axis=0)

            norm = float(np.linalg.norm(embedding))
            if norm > 0:
                embedding = embedding / norm

            embeddings.append(embedding.tolist())
        return embeddings
class SchemaStore:
    """Store and search schema using basic embeddings."""

    def __init__(self):
        """Initialize with basic embedding function."""
        self.client = chromadb.Client(Settings(
            persist_directory='/Users/kajalmahata/smart_QL/chroma_data',
            anonymized_telemetry=False,
            allow_reset=True,
            is_persistent=True
        ))

        # Use our basic embedding function
        self.embedding_function = BasicEmbeddingFunction()

        # Create collection
        self.collection = self.client.get_or_create_collection(
            name="schema_metadata",
            embedding_function=self.embedding_function
        )

    def _create_table_text(self, table: Dict, schema_name: str) -> str:
        """Create searchable text for table."""
        columns_info = []
        for col in table['columns']:
            # Basic column info
            col_info = f"{col['name']} ({col['data_type']})"

            # Check for primary key
            if col.get('is_primary_key', False):
                col_info += " [PK]"

            # Check if column name is in foreign keys
            if table.get('foreign_keys', {}).get(col['name']):
                col_info += f" [FK -> {table['foreign_keys'][col['name']]}]"

            columns_info.append(col_info)

        return f"""
        TABLE: {table['name']}
        DATABASE: {schema_name}
        SCHEMA: {table.get('db_schema', schema_name)}
        COLUMNS: {', '.join(columns_info)}
        PRIMARY KEYS: {', '.join(table.get('primary_keys', []))}
        FOREIGN KEYS: {json.dumps(table.get('foreign_keys', {}))}
        DESCRIPTION: Table for managing {table['name'].replace('_', ' ')} data
        """

    async def store_schema(self, schema: Dict, user_id: str, connection_id: str):
        """Store schema information."""
        try:
            documents = []
            metadatas = []
            ids = []

            # Process tables
            for table in schema['tables']:
                # Store table information
                table_doc = self._create_table_text(table, schema['name'])
                table_id = hashlib.md5(
                    f"table_{user_id}_{connection_id}_{table['name']}".encode()
                ).hexdigest()

                table_metadata = {
                    "type": "table",
                    "user_id": user_id,
                    "connection_id": connection_id,
                    "database": schema['name'],
                    "table_name": table['name']
                }

                documents.append(table_doc)
                ids.append(table_id)
                metadatas.append(table_metadata)

            # Process relationships
            for rel in schema.get('relationships', []):
                rel_doc = f"""
                RELATIONSHIP:
                SOURCE: {rel['source_table']}.{rel['source_column']}
                TARGET: {rel['target_table']}.{rel['target_column']}
                TYPE: {rel.get('type', 'unknown')}
                """

                rel_id = hashlib.md5(
                    f"rel_{user_id}_{connection_id}_{rel['source_table']}_{rel['target_table']}".encode()
                ).hexdigest()

                rel_metadata = {
                    "type": "relationship",
                    "user_id": user_id,
                    "connection_id": connection_id,
                    "database": schema['name'],
                    "source_table": rel['source_table'],
                    "target_table": rel['target_table']
                }

                documents.append(rel_doc)
                ids.append(rel_id)
                metadatas.append(rel_metadata)

            # Store in ChromaDB
            self.collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )

            print(f"Successfully stored {len(documents)} schema elements")

        except Exception as e:
            print(e)
            print(f"Error storing schema: {str(e)}")
            raise

        async def search_schema(
                self,
                query: str,
                user_id: str,
                connection_id: str,
                n_results: int = 5,
                include_embeddings: bool = False
        ) -> Dict[str, List[Dict]]:
            try:
                where_clause = {
                    "$and": [
                        {"user_id": {"$eq": user_id}},
                        {"connection_id": {"$eq": connection_id}}
                    ]
                }

                all_docs = self.collection.get(where=where_clause)
                total_docs = len(all_docs['ids'])

                if total_docs == 0:
                    return {"tables": [], "relationships": []}

                n_results = min(n_results, total_docs)
                include = ["documents", "metadatas", "distances"]
                if include_embeddings:
                    include.append("embeddings")

                results = self.collection.query(
                    query_texts=[query],
                    where=where_clause,
                    n_results=n_results,
                    include=include
                )

                schema_context = {
                    "tables": [],
                    "relationships": []
                }

                if results['documents'] and results['documents'][0]:
                    for i in range(len(results['documents'][0])):
                        metadata = results['metadatas'][0][i]
                        content = results['documents'][0][i]
                        distance = float(results['distances'][0][i])

                        result_item = {
                            "content": content,
                            "metadata": metadata,
                            "relevance": float(1.0 - (distance / 2))
                        }

                        if include_embeddings and 'embeddings' in results:
                            result_item["embedding"] = results['embeddings'][0][i]

                        element_type = metadata['type']
                        schema_context[f"{element_type}s"].append(result_item)

                return schema_context

            except Exception as e:
                print(f"Error searching schema: {str(e)}")
                raise

    async def get_schema(
            self,
            user_id: str,
            connection_id: str,
            schema_name: str = None
    ) -> Dict[str, List[Dict]]:
        try:
            where_clause = {
                "$and": [
                    {"user_id": {"$eq": user_id}},
                    {"connection_id": {"$eq": connection_id}}
                ]
            }

            if schema_name:
                where_clause["$and"].append({"schema_name": {"$eq": schema_name}})

            all_docs = self.collection.get(where=where_clause)
            total_docs = len(all_docs['ids'])

            if total_docs == 0:
                return {"tables": [], "relationships": []}

            schema_context = {
                "tables": [],
                "relationships": []
            }

            for i in range(total_docs):
                metadata = all_docs['metadatas'][i]
                content = all_docs['documents'][i]

                result_item = {
                    "content": content,
                    "metadata": metadata
                }

                element_type = metadata['type']
                schema_context[f"{element_type}s"].append(result_item)

            return schema_context

        except Exception as e:
            #logger.error(f"Error getting schema: {str(e)}")
            raise

    async def search_schema(
            self,
            query: str,
            user_id: str,
            connection_id: str,
            n_results: int = 5,
            include_embeddings: bool = False
    ) -> Dict[str, List[Dict]]:
        try:
            where_clause = {
                "$and": [
                    {"user_id": {"$eq": user_id}},
                    {"connection_id": {"$eq": connection_id}}
                ]
            }

            all_docs = self.collection.get(where=where_clause)
            total_docs = len(all_docs['ids'])

            if total_docs == 0:
                return {"tables": [], "relationships": []}

            n_results = min(n_results, total_docs)
            include = ["documents", "metadatas", "distances"]
            if include_embeddings:
                include.append("embeddings")

            results = self.collection.query(
                query_texts=[query],
                where=where_clause,
                n_results=n_results,
                include=include
            )

            schema_context = {
                "tables": [],
                "relationships": []
            }

            if results['documents'] and results['documents'][0]:
                for i in range(len(results['documents'][0])):
                    metadata = results['metadatas'][0][i]
                    content = results['documents'][0][i]
                    distance = float(results['distances'][0][i])

                    result_item = {
                        "content": content,
                        "metadata": metadata,
                        "relevance": float(1.0 - (distance / 2))
                    }

                    if include_embeddings and 'embeddings' in results:
                        result_item["embedding"] = results['embeddings'][0][i]

                    element_type = metadata['type']
                    schema_context[f"{element_type}s"].append(result_item)

            return schema_context

        except Exception as e:
            print(f"Error searching schema: {str(e)}")
            raise
