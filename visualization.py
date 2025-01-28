import asyncio
import anthropic
from typing import Dict, Tuple, List, Any
import logging
import json
logger = logging.getLogger(__name__)

class QueryIntentAnalyzer:
    def __init__(self):
        self.client = anthropic.Client(api_key='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')

    async def analyze_query_intent(
        self,
        natural_query: str,
        schema_context: List[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Analyze natural language query intent and provide detailed explanation
        of the transformation process to SQL.
        """
        try:
            schema_info = "Available tables and their structures:\n"
            if schema_context:
                for table in schema_context:
                    schema_info += f"\nTable: {table['table_name']}\n"
                    for col in table['columns']:
                        schema_info += f"- {col['name']} ({col['type']})"
                        if col.get('description'):
                            schema_info += f": {col['description']}"
                        schema_info += "\n"

            prompt = f"""
            As an expert in database query analysis and natural language processing,
            analyze this query and provide a comprehensive breakdown of the transformation process.

            Natural Language Query: {natural_query}

            Database Schema Context:
            {schema_info}

            Provide a detailed analysis in the following JSON format:

            {{
                "query_understanding": {{
                    "identified_entities": ["list of main entities/tables involved"],
                    "relationships": ["identified relationships between entities"],
                    "conditions": ["identified conditions or filters"],
                    "aggregations": ["identified aggregations or calculations"]
                }},
                "transformation_steps": [
                    {{
                        "step": "step number",
                        "action": "what is being done",
                        "explanation": "detailed explanation of this step",
                        "sql_component": "corresponding SQL component being generated"
                    }}
                ],
                "generated_sql": "the complete SQL query",
                "natural_explanation": "A natural language explanation of what the SQL query does",
                "alternative_approaches": [
                    {{
                        "sql": "alternative SQL query",
                        "explanation": "why this might be a good alternative",
                        "trade_offs": "performance/complexity trade-offs"
                    }}
                ],
                "complexity_analysis": {{
                    "level": "simple/moderate/complex",
                    "factors": ["factors contributing to complexity"],
                    "optimization_opportunities": ["potential areas for optimization"]
                }}
            }}
            """

            response = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=2000,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            # Extract and parse the JSON response
            content = response.content[0].text
            result = self._extract_json_response(content)
            
            if not result:
                raise ValueError("Failed to parse Claude's response")

            # Validate the generated SQL by checking for basic SQL keywords
            sql = result.get("generated_sql", "")
            if not any(keyword in sql.upper() for keyword in ["SELECT", "FROM", "INSERT", "UPDATE", "DELETE"]):
                raise ValueError("Generated SQL appears to be invalid")

            return result

        except Exception as e:
            logger.error(f"Error analyzing query intent: {str(e)}")
            raise

    def _extract_json_response(self, content: str) -> Dict[str, Any]:
        """Extract and parse JSON from Claude's response"""
        try:
            # Look for JSON structure in the response
            import re
            json_match = re.search(r'\{[\s\S]*\}', content)
            if json_match:
                return json.loads(json_match.group())
            return {}
        except Exception as e:
            logger.error(f"Error parsing Claude response: {str(e)}")
            return {}


async def query_analyzer():
    """Simple test function for QueryIntentAnalyzer"""
    try:
        # Initialize the analyzer
        analyzer = QueryIntentAnalyzer()

        # Sample schema context
        sample_schema = [
            {
                "table_name": "orders",
                "columns": [
                    {"name": "order_id", "type": "integer", "description": "Primary key"},
                    {"name": "customer_id", "type": "integer", "description": "Foreign key to customers"},
                    {"name": "total_amount", "type": "decimal", "description": "Order total"}
                ]
            },
            {
                "table_name": "customers",
                "columns": [
                    {"name": "customer_id", "type": "integer", "description": "Primary key"},
                    {"name": "name", "type": "varchar", "description": "Customer name"},
                    {"name": "email", "type": "varchar", "description": "Customer email"}
                ]
            }
        ]

        # Test cases
        test_queries = [
            "Show me total sales for each customer",
            "Find all orders over $1000",
            "List customers who haven't placed any orders"

        ]

        print("\nStarting Query Intent Analyzer Test")
        print("=" * 50)

        for query in test_queries:
            print(f"\nTesting query: {query}")
            print("-" * 30)

            try:
                result = await analyzer.analyze_query_intent(query, sample_schema)

                # Print the analysis results
                print("\nQuery Understanding:")
                print("Entities:", ", ".join(result["query_understanding"]["identified_entities"]))
                print("Generated SQL:", result["generated_sql"])
                print("Natural Explanation:", result["natural_explanation"])
                print("Complexity Level:", result["complexity_analysis"]["level"])

            except Exception as e:
                print(f"Error analyzing query: {str(e)}")

        print("\nTest completed successfully!")

    except Exception as e:
        print(f"Test failed with error: {str(e)}")


if __name__ == "__main__":
    asyncio.run(query_analyzer())
