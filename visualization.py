from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Text
from sqlalchemy.orm import relationship

from smart_ql.features.data_source.repositories.data_source_entity import BaseEntity


class SchemaAnalysisEntity(BaseEntity):
    __tablename__ = 'schema_analyses'

    connection_id = Column(Integer, ForeignKey('database_connections.id', ondelete='CASCADE'), nullable=False)
    schema_name = Column(String(255), nullable=False)
    schema_analysis = Column(Text, nullable=False)  # Store the overall schema analysis
    analyzed_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    status = Column(String(20), default='completed')

    # Relationship to table analyses
    table_analyses = relationship("TableAnalysisEntity", back_populates="schema_analysis", cascade="all, delete-orphan")
    # Relationship to database connection
    connection = relationship("DatabaseConnectionEntity", back_populates="schema_analyses")

    __table_args__ = (
        {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4', 'mysql_collate': 'utf8mb4_unicode_ci'}
    )

class TableAnalysisEntity(BaseEntity):
    __tablename__ = 'table_analyses'

    schema_analysis_id = Column(Integer, ForeignKey('schema_analyses.id', ondelete='CASCADE'), nullable=False)
    table_name = Column(String(255), nullable=False)
    analysis = Column(Text, nullable=False)  # Store the table-specific analysis
    analyzed_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)

    # Relationship to schema analysis
    schema_analysis = relationship("SchemaAnalysisEntity", back_populates="table_analyses")

    __table_args__ = (
        {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4', 'mysql_collate': 'utf8mb4_unicode_ci'}
    )
