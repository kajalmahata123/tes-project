from typing import Dict

from chromadb.api.models.Collection import Collection


class SchemaAwareRepository:
    def __init__(self, chroma_collection: Collection):
        self.collection = chroma_collection

    async def get_schema_context(
            self,
            user_id: str,
            connection_id: str,
            schema_name: str = None,
            query: str = "",
            include_embeddings: bool = False
    ) -> Dict:
        try:
            where_clause = {
                "$and": [
                    {"user_id": {"$eq": user_id}},
                    {"connection_id": {"$eq": connection_id}}
                ]
            }

            if schema_name:
                where_clause["$and"].append({"schema_name": {"$eq": schema_name}})

            if query:
                include = ["documents", "metadatas", "distances"]
                if include_embeddings:
                    include.append("embeddings")

                results = self.collection.query(
                    query_texts=[query],
                    where=where_clause,
                    n_results=5,
                    include=include
                )
            else:
                results = self.collection.get(
                    where=where_clause,
                    include=["documents", "metadatas"]
                )

            schema_context = {
                "tables": [],
                "relationships": []
            }

            documents = results['documents'][0] if query else results['documents']
            metadatas = results['metadatas'][0] if query else results['metadatas']
            distances = results.get('distances', [[0] * len(documents)])[0] if query else [0] * len(documents)

            for i, doc in enumerate(documents):
                metadata = metadatas[i]
                distance = distances[i]

                result_item = {
                    "content": doc,
                    "metadata": metadata,
                    "relevance": 1.0 - (distance / 2) if query else 1.0
                }

                if include_embeddings and 'embeddings' in results:
                    result_item["embedding"] = results['embeddings'][0][i]

                element_type = metadata['type']
                schema_context[f"{element_type}s"].append(result_item)

            return schema_context

        except Exception as e:
            #logger.error(f"Error getting schema context: {str(e)}")
            raise
