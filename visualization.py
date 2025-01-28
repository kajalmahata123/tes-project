from typing import Optional, List, Dict
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from smart_ql.features.schema_analyzer.entity.schema_analysis_entity import SchemaAnalysisEntity, \
    TableAnalysisEntity


class SchemaAnalysisRepository:
    """
    Repository class for handling schema analysis operations in the database.
    """

    def __init__(self, db: Session):
        """
        Initialize the repository with a database session.

        :param db: SQLAlchemy Session object for database operations.
        """
        self.db = db

    def create_analysis(self, connection_id: int, schema_name: str, schema_analysis: str,
                        table_analyses: List[Dict[str, str]]) -> SchemaAnalysisEntity:
        """
        Create a new schema analysis and associated table analyses in the database.

        :param connection_id: ID of the database connection.
        :param schema_name: Name of the schema being analyzed.
        :param schema_analysis: Analysis result of the schema.
        :param table_analyses: List of table analysis results, each containing table name and analysis.
        :return: The created SchemaAnalysisEntity object.
        :raises SQLAlchemyError: If there is an error during the database operation.
        """
        try:
            # Create schema analysis
            schema_analysis_entity = SchemaAnalysisEntity(
                connection_id=connection_id,
                schema_name=schema_name,
                schema_analysis=schema_analysis,
                status='completed'
            )
            self.db.add(schema_analysis_entity)
            self.db.flush()  # Flush to get the schema_analysis_id

            # Create table analyses
            for table_analysis in table_analyses:
                table_analysis_entity = TableAnalysisEntity(
                    schema_analysis_id=schema_analysis_entity.id,
                    table_name=table_analysis['table_name'],
                    analysis=table_analysis['analysis']
                )
                self.db.add(table_analysis_entity)

            self.db.commit()
            return schema_analysis_entity

        except SQLAlchemyError as e:
            self.db.rollback()
            raise e

    def get_latest_analysis(self, connection_id: int) -> Optional[SchemaAnalysisEntity]:
        """
        Retrieve the latest schema analysis for a given connection ID.

        :param connection_id: ID of the database connection.
        :return: The latest SchemaAnalysisEntity object or None if not found.
        """
        return self.db.query(SchemaAnalysisEntity)\
            .filter(SchemaAnalysisEntity.connection_id == connection_id)\
            .order_by(SchemaAnalysisEntity.analyzed_at.desc())\
            .first()

    def get_table_analyses(self, schema_analysis_id: int) -> List[TableAnalysisEntity]:
        """
        Retrieve all table analyses for a given schema analysis ID.

        :param schema_analysis_id: ID of the schema analysis.
        :return: List of TableAnalysisEntity objects.
        """
        return self.db.query(TableAnalysisEntity)\
            .filter(TableAnalysisEntity.schema_analysis_id == schema_analysis_id)\
            .all()
