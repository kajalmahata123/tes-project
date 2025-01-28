from typing import List
from sqlalchemy.orm import Session
from smart_ql.features.schema_analyzer.entity.schema_analysis_entity import SchemaAnalysisEntity
from smart_ql.features.schema_analyzer.repository.schema_analysis_repository import \
    SchemaAnalysisRepository


class SchemaAnalysisService:
    def __init__(self, db: Session):
        """
        Initialize the services with a database session.

        :param db: SQLAlchemy Session object for database operations.
        """
        self.db = db
        self.schema_analysis_repo = SchemaAnalysisRepository(db)

    async def store_analysis_results(self, connection_id: int,
                                     schema_name: str, schema_analysis: dict,
                                     table_analyses: List[dict]) -> SchemaAnalysisEntity:
        """
        Store the schema analysis results and associated table analyses in the database.

        :param connection_id: ID of the database connection.
        :param schema_name: Name of the schema being analyzed.
        :param schema_analysis: Analysis result of the schema.
        :param table_analyses: List of table analysis results, each containing table name and analysis.
        :return: The created SchemaAnalysisEntity object.
        """
        # Format table analyses

        formatted_table_analyses = [
            {
                'table_name': analysis['table_name'],
                'analysis': analysis['analysis']
            }
            for analysis in table_analyses
        ]

        # Store in database
        return self.schema_analysis_repo.create_analysis(
            connection_id=connection_id,
            schema_name=schema_name,
            schema_analysis=schema_analysis,
            table_analyses=formatted_table_analyses
        )
