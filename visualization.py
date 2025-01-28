from typing import Optional, Dict
from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from smart_ql.db.database import get_db
from smart_ql.features.query_suggestion.respository.query_history_repo import QueryHistoryRepository
history_router = APIRouter()

class HistoryRequest(BaseModel):
    connection_id: str
    user_id: str
    schema_name: Optional[str] = None

@history_router.post("/history")
async def get_query_history(
        request: HistoryRequest,
        db: Session = Depends(get_db)
) -> Dict:
    try:
        repository=QueryHistoryRepository(db);
        history = await repository.get_historical_queries(
            user_id=request.user_id,
            connection_id=request.connection_id
        )
        return {"history": [query.to_dict() for query in history]}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
