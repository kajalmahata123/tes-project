from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from sqlalchemy.orm import Session
from smart_ql.db.chroma_client import get_chroma_client
from smart_ql.db.database import get_db
from smart_ql.features.query_suggestion.respository.query_history_repo import QueryHistoryRepository
from smart_ql.features.query_suggestion.respository.query_suggestion_repo import SchemaAwareRepository
from smart_ql.features.query_suggestion.service.prompt_generator_service import PromptGenerator

query_recomendation_router = APIRouter()

class QueryRecommendation(BaseModel):
    query: str = Field(..., description="Natural language query")
    purpose: str = Field(..., description="Purpose of the query")
    tables: List[str] = Field(default_list=[], description="Tables involved")
    frequency: Optional[str] = Field(None, description="Query frequency in history")

class QueryRecommendRequest(BaseModel):
    connection_id: str
    user_id: str
    schema_name: Optional[str] = None
    include_history: bool = True
    time_window: Optional[int] = 30

class QueryRecommendResponse(BaseModel):
    recommended_queries: List[QueryRecommendation]

def get_schema_repository(chroma_client=Depends(get_chroma_client)):
    collection = chroma_client.get_or_create_collection("schema_metadata")
    return SchemaAwareRepository(collection)

def get_history_repository(db: Session = Depends(get_db)):
    return QueryHistoryRepository(db)

def get_prompt_generator():
    return PromptGenerator()

@query_recomendation_router.post("/recommend", response_model=QueryRecommendResponse)
async def get_query_recommendations(
    request: QueryRecommendRequest,
    schema_repo: SchemaAwareRepository = Depends(get_schema_repository),
    hist_repo: QueryHistoryRepository = Depends(get_history_repository),
    prompt_generator: PromptGenerator = Depends(get_prompt_generator)
) -> QueryRecommendResponse:
    try:
        schema_context = await schema_repo.get_schema_context(
            user_id=request.user_id,
            connection_id=request.connection_id,
            schema_name=request.schema_name
        )

        query_history = None
        if request.include_history:
            query_history = await hist_repo.get_historical_queries(
                user_id=request.user_id,
                connection_id=request.connection_id,
                time_window=request.time_window
            )

        recommendations = await prompt_generator.get_query_suggestions(
            schema_context=schema_context,
            query_history=query_history
        )
        return recommendations

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


