import asyncio
from dataclasses import dataclass, asdict
from typing import Dict, List
import json
from anthropic import Anthropic
import logging

logger = logging.getLogger(__name__)


@dataclass
class DocumentationPackage:
    """Complete schema documentation package"""
    technical_docs: Dict
    api_docs: Dict
    developer_guides: Dict
    admin_guides: Dict
    diagrams: Dict
    examples: Dict

    def to_dict(self):
        """Convert the documentation package to a dictionary"""
        return asdict(self)


class AIDocumentationGenerator:
    """Advanced AI-powered documentation generation."""

    def __init__(self):

        self.client = Anthropic(api_key='')
        self.model = "claude-3-sonnet-20240229"



    async def _generate_technical_docs(self, schema: Dict) -> Dict:
        """Generate technical documentation."""
        prompt = f"""
        Generate comprehensive technical documentation for:
        {json.dumps(schema, indent=2)}

        Include:
        1. Schema overview
        2. Table relationships
        3. Constraints and indexes
        4. Performance considerations
        5. Security measures

        Format the response as a JSON object with the following structure:
        {{
            "content": {{
                "overview": "string - Schema overview section",
                "relationships": "string - Table relationships section",
                "constraints": "string - Constraints and indexes section",
                "performance": "string - Performance considerations section",
                "security": "string - Security measures section"
            }},
            "metadata": {{
                "version": "string - Documentation version",
                "last_updated": "string - ISO timestamp",
                "schema_hash": "string - Hash of input schema"
            }}
        }}

        Ensure all sections are properly formatted in Markdown.
        """

        response =  self.client.messages.create(
            max_tokens=4096,
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )

        # Parse the response content as JSON
        try:
            return json.loads(response.content[0].text)
        except json.JSONDecodeError:
            # Fallback to raw text if JSON parsing fails
            return {"content": response.content[0].text}

    async def _generate_api_docs(self, schema: Dict) -> Dict:
        """Generate API documentation."""
        prompt = f"""
        Create API documentation based on this schema:
        {json.dumps(schema, indent=2)}

        Include:
        1. REST endpoints
        2. Request/response formats
        3. Authentication methods
        4. Error handling
        5. Rate limiting

        Format the response as a JSON object with the following structure:
        {{
            "content": {{
                "endpoints": [{{
                    "path": "string",
                    "method": "string",
                    "description": "string",
                    "request_format": "string",
                    "response_format": "string",
                    "examples": [{{
                        "request": "string",
                        "response": "string"
                    }}]
                }}],
                "authentication": "string",
                "error_handling": "string",
                "rate_limiting": "string"
            }},
            "metadata": {{
                "version": "string",
                "last_updated": "string"
            }}
        }}

        Include complete example requests and responses.
        """

        response =  self.client.messages.create(
            max_tokens=4096,
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )

        try:
            return json.loads(response.content[0].text)
        except json.JSONDecodeError:
            return {"content": response.content[0].text}

    async def _generate_developer_guides(self, schema: Dict, context: str) -> Dict:
        """Generate developer guides with contextual information."""
        prompt = f"""
        Generate developer guides based on this schema and context:
        Schema: {json.dumps(schema, indent=2)}
        Context: {context}

        Include:
        1. Getting started guide
        2. Best practices
        3. Common use cases
        4. Integration examples
        5. Troubleshooting

        Format the response as a JSON object with the following structure:
        {{
            "content": {{
                "getting_started": "string",
                "best_practices": "string",
                "use_cases": [{{
                    "title": "string",
                    "description": "string",
                    "implementation": "string"
                }}],
                "integration": "string",
                "troubleshooting": [{{
                    "problem": "string",
                    "solution": "string"
                }}]
            }},
            "metadata": {{
                "context": "string",
                "last_updated": "string"
            }}
        }}
        """

        response =  self.client.messages.create(
            max_tokens=4096,
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )

        try:
            return json.loads(response.content[0].text)
        except json.JSONDecodeError:
            return {"content": response.content[0].text}

    async def _generate_admin_guides(self, schema: Dict) -> Dict:
        """Generate administration guides."""
        prompt = f"""
        Generate administration guides for this schema:
        {json.dumps(schema, indent=2)}

        Include:
        1. System requirements
        2. Installation steps
        3. Configuration
        4. Maintenance procedures
        5. Backup and recovery
        6. Security management

        Format the response as a JSON object with the following structure:
        {{
            "content": {{
                "requirements": {{
                    "hardware": "string",
                    "software": "string"
                }},
                "installation": [{{
                    "step": "string",
                    "description": "string",
                    "commands": "string"
                }}],
                "configuration": "string",
                "maintenance": "string",
                "backup_recovery": "string",
                "security": "string"
            }},
            "metadata": {{
                "version": "string",
                "last_updated": "string"
            }}
        }}
        """

        response =  self.client.messages.create(
            max_tokens=4096,
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )

        try:
            return json.loads(response.content[0].text)
        except json.JSONDecodeError:
            return {"content": response.content[0].text}

    async def _generate_diagrams(self, schema: Dict) -> Dict:
        """Generate system diagrams from schema."""
        prompt = f"""
        Generate system diagrams for this schema:
        {json.dumps(schema, indent=2)}

        Include:
        1. Entity Relationship Diagram (ERD)
        2. System Architecture Diagram
        3. Data Flow Diagram
        4. Component Interaction Diagram

        Format the response as a JSON object with the following structure:
        {{
            "content": {{
                "erd": {{
                    "description": "string",
                    "nodes": [{{
                        "name": "string",
                        "type": "string",
                        "attributes": ["string"]
                    }}],
                    "relationships": [{{
                        "from": "string",
                        "to": "string",
                        "type": "string"
                    }}]
                }},
                "architecture": {{
                    "description": "string",
                    "components": [{{
                        "name": "string",
                        "purpose": "string",
                        "connections": ["string"]
                    }}]
                }},
                "dataflow": {{
                    "description": "string",
                    "flows": [{{
                        "source": "string",
                        "destination": "string",
                        "data": "string",
                        "direction": "string"
                    }}]
                }},
                "component_interaction": {{
                    "description": "string",
                    "interactions": [{{
                        "component1": "string",
                        "component2": "string",
                        "interaction_type": "string",
                        "description": "string"
                    }}]
                }}
            }},
            "metadata": {{
                "version": "string",
                "last_updated": "string",
                "diagram_format": "string"
            }}
        }}
        """

        response =  self.client.messages.create(
            max_tokens=4096,
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )

        try:
            return json.loads(response.content[0].text)
        except json.JSONDecodeError:
            return {"content": response.content[0].text}

    async def _generate_examples(self, schema: Dict) -> Dict:
        """Generate code examples from schema."""
        prompt = f"""
        Generate code examples for this schema:
        {json.dumps(schema, indent=2)}

        Include:
        1. CRUD operations
        2. Common queries
        3. Data validation
        4. Error handling
        5. Best practices

        Format the response as a JSON object with the following structure:
        {{
            "content": {{
                "crud_examples": [{{
                    "operation": "string",
                    "language": "string",
                    "code": "string",
                    "description": "string"
                }}],
                "queries": [{{
                    "purpose": "string",
                    "language": "string",
                    "code": "string",
                    "explanation": "string"
                }}],
                "validation": [{{
                    "scenario": "string",
                    "language": "string",
                    "code": "string",
                    "notes": "string"
                }}],
                "error_handling": [{{
                    "error_type": "string",
                    "language": "string",
                    "code": "string",
                    "description": "string"
                }}],
                "best_practices": [{{
                    "title": "string",
                    "description": "string",
                    "code_example": "string"
                }}]
            }},
            "metadata": {{
                "languages": ["string"],
                "total_examples": "number",
                "last_updated": "string"
            }}
        }}

        Provide examples in Python, SQL, and REST API formats.
        """

        response =  self.client.messages.create(
            max_tokens=4096,
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )

        try:
            return json.loads(response.content[0].text)
        except json.JSONDecodeError:
            return {"content": response.content[0].text}
        """Generate administration guides."""
        prompt = f"""
        Generate administration guides for this schema:
        {json.dumps(schema, indent=2)}

        Include:
        1. System requirements
        2. Installation steps
        3. Configuration
        4. Maintenance procedures
        5. Backup and recovery
        6. Security management

        Format the response as a JSON object with the following structure:
        {{
            "content": {{
                "requirements": {{
                    "hardware": "string",
                    "software": "string"
                }},
                "installation": [{{
                    "step": "string",
                    "description": "string",
                    "commands": "string"
                }}],
                "configuration": "string",
                "maintenance": "string",
                "backup_recovery": "string",
                "security": "string"
            }},
            "metadata": {{
                "version": "string",
                "last_updated": "string"
            }}
        }}
        """

        response =  self.client.messages.create(
            max_tokens=4096,
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )

        try:
            return json.loads(response.content[0].text)
        except json.JSONDecodeError:
            return {"content": response.content[0].text}


async def main():
    # Sample healthcare schema
    healthcare_schema = {
        "tables": {
            "patients": {
                "columns": {
                    "id": {"type": "integer", "primary_key": True},
                    "mrn": {"type": "varchar", "unique": True},
                    "name": {"type": "varchar"},
                    "dob": {"type": "date"}
                }
            },
            "encounters": {
                "columns": {
                    "id": {"type": "integer", "primary_key": True},
                    "patient_id": {"type": "integer"},
                    "date": {"type": "timestamp"},
                    "notes": {"type": "text"}
                }
            }
        },
        "relationships": [
            {
                "from_table": "encounters",
                "to_table": "patients",
                "from_column": "patient_id",
                "to_column": "id"
            }
        ]
    }

    # Initialize Anthropic client
    ai_client = Anthropic(api_key="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")

    # Initialize documentation generator
    doc_generator = AIDocumentationGenerator(ai_client)

    print("\nGenerating Healthcare Documentation Package...")
    healthcare_docs = await doc_generator.he(
        healthcare_schema,
        "HIPAA-compliant healthcare data platform"
    )

    # Convert to dictionary and print
    docs_dict = healthcare_docs.to_dict()
    print("Healthcare Documentation Package Generated:")
    print(json.dumps(docs_dict, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
