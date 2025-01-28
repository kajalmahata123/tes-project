from enum import Enum
from fastapi import APIRouter, Depends
from typing import Dict, Optional, List
from pydantic import BaseModel, Field
from smart_ql.features.document_generator.service.ai_doc_generator import AIDocumentationGenerator
from smart_ql.features.semantic_search.vector_store import SchemaStore
document_router = APIRouter()

class DocumentContext(str, Enum):
    GETTING_STARTED = "getting_started"
    BEST_PRACTICES = "best_practices"
    USE_CASES = "use_cases"
    INTEGRATION = "integration"
    TROUBLESHOOTING = "troubleshooting"
    PERFORMANCE = "performance"
    SECURITY = "security"
    DATA_MODEL = "data_model"
    API_USAGE = "api_usage"
    DEPLOYMENT = "deployment"
class DocGenRequest(BaseModel):
    connection_id: str
    user_id: str
    schema_name: str
    contexts: Optional[List[DocumentContext]] = Field(
        default=[],
        max_items=5,
        description="Optional list of contexts for documentation"
    )

@document_router.post("/technical")
async def generate_technical_docs(
        request: DocGenRequest,
        schema_store: SchemaStore = Depends(SchemaStore),
        doc_generator: AIDocumentationGenerator = Depends(AIDocumentationGenerator)
) -> Dict:
    schema = await schema_store.get_schema(
        request.user_id, request.connection_id, request.schema_name
    )
    return await doc_generator._generate_technical_docs(schema)

@document_router.post("/api")
async def generate_api_docs(
        request: DocGenRequest,
        schema_store: SchemaStore = Depends(SchemaStore),
        doc_generator: AIDocumentationGenerator = Depends(AIDocumentationGenerator)
) -> Dict:
    schema = await schema_store.get_schema(
        request.user_id, request.connection_id, request.schema_name
    )
    return await doc_generator._generate_api_docs(schema)

@document_router.post("/developer")
async def generate_developer_guides(
        request: DocGenRequest,
        schema_store: SchemaStore = Depends(SchemaStore),
        doc_generator: AIDocumentationGenerator = Depends(AIDocumentationGenerator)
) -> Dict:
    schema = await schema_store.get_schema(
        request.user_id, request.connection_id, request.schema_name
    )
    return await doc_generator._generate_developer_guides(schema, request.context)

@document_router.post("/diagrams")
async def generate_diagrams(
        request: DocGenRequest,
        schema_store: SchemaStore = Depends(SchemaStore),
        doc_generator: AIDocumentationGenerator = Depends(AIDocumentationGenerator)
) -> Dict:
    schema = await schema_store.get_schema(
        request.user_id, request.connection_id, request.schema_name
    )
    return await doc_generator._generate_diagrams(schema)

@document_router.post("/examples")
async def generate_examples(
        request: DocGenRequest,
        schema_store: SchemaStore = Depends(SchemaStore),
        doc_generator: AIDocumentationGenerator = Depends(AIDocumentationGenerator)
) -> Dict:
    schema = await schema_store.get_schema(
        request.user_id, request.connection_id, request.schema_name
    )
    return await doc_generator._generate_examples(schema)
