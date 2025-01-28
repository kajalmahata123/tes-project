# app/schemas/schema_extractor.py
from pydantic import BaseModel
from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from smart_ql.assistants.sql_assistant.config.db_config import DBConfig
from smart_ql.features.schema_analyzer.schema_analyzer import SchemaAnalyzer, SchemaAnalysisResponse
from smart_ql.assistants.sql_assistant.schema_extractors.mysql_extractor import MySQLSchemaExtractor
from smart_ql.db.database import get_db
from smart_ql.features.data_source.repositories.data_source_entity import DatabaseVendor
from smart_ql.features.data_source.services.datasource_service import DatabaseService





class SchemaExtractionResponse(BaseModel):
    schema: Dict[str, Any]
    message: str = "Schema extracted successfully"


schema_extraction_router = APIRouter()


@schema_extraction_router.get("/{connection_id}", response_model=SchemaAnalysisResponse)
async def extract_database_schema(
        connection_id: int,
        db: Session = Depends(get_db)
):
    """Extract database schema for a given connection"""
    try:
        # Get the database connection
        service = DatabaseService(db)
        connection = service.get_connection(connection_id)

        if not connection:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Database connection not found: {connection_id}"
            )

        # Create config from connection details
        config = DBConfig(
            vendor=connection.vendor.value,
            host=connection.config.host,
            port=connection.config.port,
            database=connection.config.database_name,
            username=connection.credentials.username,
            password=connection.credentials.password
        )

        # Extract schema based on vendor
        if connection.vendor == DatabaseVendor.MYSQL:
            extractor = MySQLSchemaExtractor(config)
            schema = await extractor.extract_schema()
            print('Schema Fetched Successfully')

            analyzer = SchemaAnalyzer()
            analysis = await analyzer.analyze_schema(schema)

            return analysis
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported database vendor: {connection.vendor}"
            )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to extract schema: {str(e)}"
        )


# Optional: Add endpoint to extract schema using direct connection details
@schema_extraction_router.post("/analysis/direct", response_model=SchemaAnalysisResponse)
async def extract_schema_direct(
        config: DBConfig
):
    """Extract database schema using direct connection details"""
    try:
        if config.vendor.lower() == "mysql":
            extractor = MySQLSchemaExtractor(config)
            schema = await extractor.extract_schema()
            analyzer = SchemaAnalyzer()
            analysis = await analyzer.analyze_schema(schema)
            return analysis
        if config.vendor.lower() == "oracle":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"SQL Server schema extraction not supported yet")

        if config.vendor.lower() == "sqlserver":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"SQL Server schema extraction not supported yet")
        if config.vendor.lower() == "postgres":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Postgres schema extraction not supported yet")
        if config.vendor.lower() == "sqlite":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"SQLite schema extraction not supported yet")
        if config.vendor.lower() == "db2":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Oracle schema extraction not supported yet")
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported database vendor: {config.vendor}"
            )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to extract schema: {str(e)}"
        )
