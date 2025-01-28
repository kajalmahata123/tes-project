import json
import re
from typing import Dict, Optional, List
from anthropic import Anthropic

from smart_ql.features.query_suggestion.respository.query_history_repo import QueryData


class PromptGenerator:
    def __init__(self):
        self.client = Anthropic(api_key="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")

    async def get_query_suggestions(
        self,
        schema_context: Dict,
        query_history: Optional[List[QueryData]] = None,
    ) -> Dict:
        try:
            prompt = self.generate_analysis_prompt(schema_context, query_history)
            response = await self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}]
            )
            return self._parse_response(response.content[0].text)
        except Exception as e:
            return {"recommended_queries": []}

    def generate_analysis_prompt(
        self,
        schema_context: Dict,
        query_history: Optional[List[QueryData]] = None,
    ) -> str:
        if query_history:
            return self._generate_history_based_prompt(schema_context, query_history)
        return self._generate_schema_based_prompt(schema_context)

    def _generate_history_based_prompt(
        self,
        schema_context: Dict,
        query_history: List[QueryData],
    ) -> str:
        return f"""
        Based on:
        Schema: {json.dumps(schema_context, indent=2)}
        History: {json.dumps([{
            'query': q.natural_language_query,
            'performance': q.execution_time
        } for q in query_history[-5:]], indent=2)}

        Generate a list of recommended queries in JSON:
        {{
            "recommended_queries": [
                {{
                    "query": "natural language query",
                    "purpose": "query purpose",
                    "tables": ["involved tables"],
                    "frequency": "how often similar queries appear in history"
                }}
            ]
        }}
        """

    def _generate_schema_based_prompt(self, schema_context: Dict) -> str:
        return f"""
        Based on schema:
        {json.dumps(schema_context, indent=2)}

        Generate a list of recommended queries in JSON:
        {{
            "recommended_queries": [
                {{
                    "query": "natural language query",
                    "purpose": "query purpose",
                    "tables": ["involved tables"]
                }}
            ]
        }}
        """

    def _parse_response(self, response: str) -> Dict:
        try:
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            return {"recommended_queries": []}
        except Exception:
            return {"recommended_queries": []}
