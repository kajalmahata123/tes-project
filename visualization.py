from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List, Dict, Any, Optional, TypedDict
from enum import Enum
import logging
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class QueryComplexity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass
class QueryData:
    natural_language_query: str
    sql_query: str
    execution_time: float
    execution_plan: str
    insights: str
    timestamp: datetime
    schema_context: Optional[Dict] = None

    def to_dict(self):
        return asdict(self)


class QueryMetrics(TypedDict):
    avg_execution_time: float
    complexity_score: float
    table_usage_frequency: Dict[str, int]
    join_patterns: List[Dict[str, Any]]


class QueryHistoryRepository:
    def __init__(self, db_session: Session):
        self.db = db_session

    async def get_historical_queries(
            self,
            user_id: str,
            connection_id: str,
            time_window: Optional[int] = 30,
            limit: int = 50
    ) -> List[QueryData]:
        try:
            query = """
            SELECT 
                natural_language_query,
                sql_query,
                execution_time,
                execution_plan,
                insights,
                timestamp
            FROM query_history
            WHERE 
                user_id = :user_id 
                AND connection_id = :connection_id
                AND timestamp >= CURRENT_DATE - :days::interval
            ORDER BY timestamp DESC
            LIMIT :limit
            """

            result = self.db.execute(
                query,
                {
                    "user_id": user_id,
                    "connection_id": connection_id,
                    "days": f"{time_window} days",
                    "limit": limit
                }
            )

            queries = []
            for row in result.fetchall():
                schema_context = await self.get_schema_context(
                    user_id,
                    connection_id,
                    row.natural_language_query
                )
                queries.append(QueryData(
                    **row._mapping,
                    schema_context=schema_context
                ))

            return queries

        except SQLAlchemyError as e:
            logger.error(f"Database error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise

    async def save_query(self, query_data: QueryData, user_id: str, connection_id: str):
        try:
            query = """
            INSERT INTO query_history (
                user_id,
                connection_id,
                natural_language_query,
                sql_query,
                execution_time,
                execution_plan,
                insights,
                timestamp
            ) VALUES (
                :user_id,
                :connection_id,
                :natural_language_query,
                :sql_query,
                :execution_time,
                :execution_plan,
                :insights,
                :timestamp
            )
            """

            self.db.execute(
                query,
                {
                    "user_id": user_id,
                    "connection_id": connection_id,
                    **query_data.to_dict()
                }
            )
            self.db.commit()

        except Exception as e:
            self.db.rollback()
            logger.error(f"Error saving query: {str(e)}")
            raise
