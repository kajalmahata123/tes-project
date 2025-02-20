from fastapi import FastAPI, HTTPException, Depends
from typing import List, Dict, Any
import anthropic
import json
from datetime import datetime

class ISOSpecProcessor:
    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)

    async def process_chunk(self, content: str) -> Dict[str, Any]:
        """Process a content chunk using Claude"""
        try:
            full_prompt = f"""
You are tasked with analyzing ISO message specifications for payment networks and identifying any parameter value changes. 
Please analyze the following specification document to identify fields, subfields, datasets, TLV fields structure, and parameter value changes.

Input Format:
[ISO message specification document with:
- Fields as F02, F03
- Subfields as F03.01, F03.02
- Datasets with IDs
- TLV fields within datasets
- Parameter values for fields]

Requirements:
1. Identify all fields (F02, F03, etc.)
2. For each field, analyze:
   - Subfields (e.g., F03.01, F03.02)
   - Datasets with their IDs
   - TLV fields within datasets
   - Parameter values and their changes
3. Include format, length, and data type specifications
4. Return results in the specified JSON format

Expected Response Format:
{{
  "fields": [
    {{
      "field_number": string,     // e.g., "F02", "F03"
      "field_name": string,       // e.g., "Primary Account Number"
      "field_type": string,       // "FIXED" | "VARIABLE" | "TLV"
      "specification": {{
        "length": string,         // e.g., "LLVAR", "16"
        "format": string,         // e.g., "n", "an", "b"
        "description": string,    // Field description
        "mandatory": boolean,     // true | false
        "parameters": [
          {{
            "name": string,       // e.g., "maximum_length", "minimum_length"
            "value": string,      // Current value
            "is_changed": boolean,  // true if value has changed
            "previous_value": string // Only present if is_changed is true
          }}
        ]
      }},
      "subfields": [
        {{
          "tag": string,          // e.g., "F03.01", "F03.02"
          "tag_name": string,     // e.g., "Transaction Currency Code"
          "specification": {{
            "length": string,
            "format": string,
            "description": string,
            "mandatory": boolean,
            "parameters": [
              {{
                "name": string,
                "value": string,
                "is_changed": boolean,
                "previous_value": string
              }}
            ]
          }}
        }}
      ],
      "datasets": [
        {{
          "dataset_id": string,    // e.g., "DS-01", "DS-02"
          "dataset_name": string,  // e.g., "Card Data"
          "specification": {{
            "length": string,
            "format": string,
            "description": string,
            "mandatory": boolean,
            "parameters": [
              {{
                "name": string,
                "value": string,
                "is_changed": boolean,
                "previous_value": string
              }}
            ]
          }},
          "tlv_fields": [
            {{
              "tag": string,       // e.g., "9F02", "9F03"
              "tag_name": string,  // e.g., "Amount, Authorized"
              "specification": {{
                "length": string,
                "format": string,
                "description": string,
                "mandatory": boolean,
                "parameters": [
                  {{
                    "name": string,
                    "value": string,
                    "is_changed": boolean,
                    "previous_value": string
                  }}
                ]
              }}
            }}
          ]
        }}
      ]
    }}
  ],
  "metadata": {{
    "total_fields": number,           
    "total_subfields": number,        
    "total_datasets": number,         
    "total_tlv_fields": number,       
    "total_parameter_changes": number,
    "document_version": string,     
    "analysis_timestamp": string    
  }}
}}

ANALYZE THE FOLLOWING ISO MESSAGE SPECIFICATION AND PROVIDE THE OUTPUT IN THE EXACT JSON FORMAT SPECIFIED ABOVE:

{content}
"""
            message = await self.client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=4096,
                temperature=0,
                messages=[
                    {
                        "role": "user",
                        "content": full_prompt
                    }
                ]
            )
            
            return json.loads(message.content[0].text)
        except Exception as e:
            print(f"Error processing chunk: {e}")
            return None

    async def process_search_results(self, search_results: List[Any]) -> Dict[str, Any]:
        """Process search results and return structured field data"""
        all_fields = []
        seen_fields = set()
        total_subfields = 0
        total_datasets = 0
        total_tlv_fields = 0
        total_parameter_changes = 0

        for result in search_results:
            content = result.content if hasattr(result, 'content') else str(result)
            processed_result = await self.process_chunk(content)
            
            if processed_result and "fields" in processed_result:
                for field in processed_result["fields"]:
                    if field["field_number"] not in seen_fields:
                        all_fields.append(field)
                        seen_fields.add(field["field_number"])
                        
                        # Count components
                        total_subfields += len(field.get("subfields", []))
                        total_datasets += len(field.get("datasets", []))
                        
                        # Count TLV fields
                        for dataset in field.get("datasets", []):
                            total_tlv_fields += len(dataset.get("tlv_fields", []))
                            
                        # Count parameter changes
                        for param in field["specification"].get("parameters", []):
                            if param.get("is_changed", False):
                                total_parameter_changes += 1

        return {
            "fields": all_fields,
            "metadata": {
                "total_fields": len(all_fields),
                "total_subfields": total_subfields,
                "total_datasets": total_datasets,
                "total_tlv_fields": total_tlv_fields,
                "total_parameter_changes": total_parameter_changes,
                "document_version": "1.0",  # Update as needed
                "analysis_timestamp": datetime.utcnow().isoformat()
            }
        }

app = FastAPI()

# Dependencies
async def get_search_results():
    """Get search results from your vector store"""
    # Replace this with your actual vector store search logic
    filters = {}
    search_results = await vector_store.search(filters=filters)
    return search_results

@app.get("/api/iso-specs")
async def get_iso_specifications(search_results: List[Any] = Depends(get_search_results)):
    """
    GET endpoint to process and return ISO message specifications
    """
    try:
        processor = ISOSpecProcessor(api_key="your-anthropic-api-key")
        results = await processor.process_search_results(search_results)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Example usage:
"""
# Call the endpoint:
GET /api/iso-specs

# Response will be in the format:
{
    "fields": [
        {
            "field_number": "F02",
            "field_name": "Primary Account Number",
            ...
        }
    ],
    "metadata": {
        "total_fields": 1,
        "total_subfields": 2,
        "total_datasets": 1,
        "total_tlv_fields": 3,
        "total_parameter_changes": 2,
        "document_version": "1.0",
        "analysis_timestamp": "2025-02-19T..."
    }
}
"""
