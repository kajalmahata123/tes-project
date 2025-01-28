import anthropic
from typing import Dict, List
from pydantic import BaseModel

from smart_ql.assistants.sql_assistant.schema_extractors.schemas import ColumnInfo, TableInfo, DatabaseSchema


class TableAnalysis(BaseModel):
    table_name: str
    analysis: str

class SchemaAnalysisResponse(BaseModel):
    schema_name: str
    schema_analysis: str
    table_analyses: List[TableAnalysis]

class SchemaAnalyzer:
    def __init__(self):
        self.client = anthropic.Anthropic(
            api_key='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'
        )

    def _get_column_info(self, column: ColumnInfo) -> str:
        """Format column information for analysis."""
        description = []
        description.append(f"{column.name} ({column.native_type})")

        if column.is_primary_key:
            description.append("[PRIMARY KEY]")

        if column.is_foreign_key and column.foreign_key_reference:
            description.append(f"[FOREIGN KEY -> {column.foreign_key_reference}]")

        if not column.is_nullable:
            description.append("[NOT NULL]")

        if column.max_length:
            description.append(f"[LENGTH: {column.max_length}]")

        return " ".join(description)

    def _create_table_analysis_prompt(self, table: TableInfo) -> str:
        """Create prompt for table analysis."""
        columns_info = [self._get_column_info(col) for col in table.columns]
        indexes_info = [
            f"- {idx.get('name', 'unnamed')}: {', '.join(idx.get('column_names', []))}"
            for idx in table.indexes
        ]

        return f"""Analyze this database table for semantic search improvements:

TABLE INFORMATION:
Name: {table.name}
Schema: {table.db_schema}

COLUMNS:
{chr(10).join('- ' + col for col in columns_info)}

PRIMARY KEYS: {', '.join(table.primary_keys)}
FOREIGN KEYS: {table.foreign_keys}
INDEXES:
{chr(10).join(indexes_info)}

Analyze the table and provide:
1. Semantic Context:
   - What business concepts does this table represent?
   - What is the primary purpose of this table?
   - What types of queries might users ask about this data?

2. Search Improvements:
   - How can we enrich the semantic description of this table?
   - What additional metadata would help in search?
   - How should we chunk this table's information?

3. Natural Language Mapping:
   - What natural language terms map to this table's concepts?
   - What synonyms or related terms should be included?
   - How can we make technical terms more searchable?

4. Relationship Context:
   - How does this table relate to other tables?
   - What business workflows involve this table?
   - What hierarchical relationships exist?

5. Specific Recommendations:
   - Suggest concrete improvements for semantic search
   - Identify missing metadata that would help searches
   - Propose chunking strategies"""

    async def analyze_table(self, table: TableInfo) -> TableAnalysis:
        """Analyze a single table and get improvement suggestions."""
        try:
            prompt = self._create_table_analysis_prompt(table)

            response = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=2000,
                temperature=0,
                system="You are an expert database architect and semantic search specialist.",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            print('Analyzing table', table.name)
            return TableAnalysis(
                table_name=table.name,
                analysis=response.content[0].text
            )

        except Exception as e:
            print(f"Error analyzing table {table.name}: {str(e)}")
            raise

    def _create_schema_analysis_prompt(self, schema: DatabaseSchema) -> str:
        """Create prompt for overall schema analysis."""
        relationships_info = []
        for rel in schema.relationships:
            source_table = rel.get('source_table', 'Unknown')
            source_column = rel.get('source_column', 'Unknown')
            target_table = rel.get('target_table', 'Unknown')
            target_column = rel.get('target_column', 'Unknown')
            rel_type = rel.get('type', 'Unknown')

            relationships_info.append(
                f"- {source_table}.{source_column} -> "
                f"{target_table}.{target_column} ({rel_type})"
            )

        print(relationships_info)
        return f"""Analyze this database schema for semantic search improvements:

DATABASE: {schema.name}
VENDOR: {schema.vendor}

TABLES:
{chr(10).join(f"- {t.name}" for t in schema.tables)}

RELATIONSHIPS:
{chr(10).join(relationships_info)}

DATABASE METADATA:
{chr(10).join(f'- {k}: {v}' for k, v in schema.metadata.items())}

Analyze the schema and provide:
1. Domain Model:
   - What is the core business domain?
   - What are the main entities and concepts?
   - How are concepts related?

2. Search Patterns:
   - What types of searches would users perform?
   - What natural language patterns map to schema concepts?
   - How can we optimize for common queries?

3. Semantic Organization:
   - How should we organize tables for semantic search?
   - What metadata hierarchy makes sense?
   - How can we chunk information effectively?

4. Improvement Recommendations:
   - What metadata should we add?
   - How can we enrich semantic descriptions?
   - What normalizations would help search?"""

    async def analyze_schema(self, schema: DatabaseSchema) -> SchemaAnalysisResponse:
        """Analyze entire schema and suggest improvements."""
        try:
            # Analyze each table
            table_analyses = []
            for table in schema.tables:
                table_analysis = await self.analyze_table(table)
                table_analyses.append(table_analysis)

            # Analyze overall schema
            schema_prompt = self._create_schema_analysis_prompt(schema)
            schema_analysis = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=2000,
                temperature=0,
                system="You are an expert database architect and semantic search specialist.",
                messages=[
                    {"role": "user", "content": schema_prompt}
                ]
            )

            return SchemaAnalysisResponse(
                schema_name=schema.name,
                schema_analysis=schema_analysis.content[0].text,
                table_analyses=table_analyses
            )

        except Exception as e:
            print(f"Error analyzing schema: {str(e)}")
            raise


# Example usage
async def main():
    analyzer = SchemaAnalyzer("your-anthropic-key")

    # Your schema
    schema = {
        "name": "alpha_ai_service",
        "vendor": "mysql",
        "tables": [
            {
                "name": "api_keys",
                "db_schema": "alpha_ai_service",
                "columns": [
                    {
                        "name": "id",
                        "data_type": "INTEGER",
                        "is_primary_key": True,
                        "is_nullable": False
                    },
                    {
                        "name": "key",
                        "data_type": "STRING",
                        "is_nullable": False
                    },
                    {
                        "name": "name",
                        "data_type": "STRING",
                        "is_nullable": False
                    },
                    {
                        "name": "created_at",
                        "data_type": "TIMESTAMP",
                        "is_nullable": True
                    }
                ],
                "primary_keys": ["id"],
                "foreign_keys": {"application_id": "applications.id"}
            },
            {
                "name": "applications",
                "db_schema": "alpha_ai_service",
                "columns": [
                    {
                        "name": "id",
                        "data_type": "INTEGER",
                        "is_primary_key": True,
                        "is_nullable": False
                    },
                    {
                        "name": "name",
                        "data_type": "STRING",
                        "is_nullable": False
                    },
                    {
                        "name": "status",
                        "data_type": "ENUM",
                        "is_nullable": True
                    }
                ],
                "primary_keys": ["id"],
                "foreign_keys": {}
            }
        ],
        "relationships": [
            {
                "source_table": "api_keys",
                "source_column": "application_id",
                "target_table": "applications",
                "target_column": "id",
                "type": "many_to_one"
            }
        ]
    }

    # Analyze schema
    analysis = await analyzer.analyze_schema(schema)

    # Print analysis
    print("\nSchema Analysis:")
    print(analysis['schema_analysis'])

    print("\nTable Analyses:")
    for table_analysis in analysis['table_analyses']:
        print(f"\nTable: {table_analysis['table_name']}")
        print(table_analysis['analysis'])


if __name__ == "__main__":
    import asyncio

    #asyncio.run(main())
