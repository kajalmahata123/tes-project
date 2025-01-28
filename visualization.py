from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
from pydantic import BaseModel
from smart_ql.features.query_intent.service.query_intent_service import QueryIntentAnalyzer
from smart_ql.features.semantic_search.vector_store import SchemaStore
intent_router = APIRouter()


class QueryAnalysisRequest(BaseModel):
    query: str
    connection_id: str
    user_id: str
    include_embeddings: bool = True


class QueryAnalysisResponse(BaseModel):
    query_understanding: Dict[str, Any]
    transformation_steps: list
    generated_sql: str
    natural_explanation: str
    alternative_approaches: list
    complexity_analysis: Dict[str, Any]


@intent_router.post("/analyze", response_model=QueryAnalysisResponse)
async def analyze_query(
        request: QueryAnalysisRequest,
        schema_store: SchemaStore = Depends(SchemaStore),
        query_analyzer: QueryIntentAnalyzer = Depends(QueryIntentAnalyzer)
) -> Dict[str, Any]:
    """
    Analyze natural language query and generate SQL with detailed explanations
    """
    try:
        # Get schema context
        schema_context = await schema_store.search_schema(
            query=request.query,
            user_id=request.user_id,
            connection_id=request.connection_id,
            include_embeddings=True
        )

        if not schema_context:
            raise HTTPException(
                status_code=404,
                detail="No relevant schema found for the query"
            )

        # Analyze query intent
        analysis_result = await query_analyzer.analyze_query_intent(
            request.query,
            schema_context
        )

        return analysis_result

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing query: {str(e)}"
        )
