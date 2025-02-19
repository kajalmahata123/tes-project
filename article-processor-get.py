from fastapi import FastAPI, HTTPException, Depends
from typing import List, Dict, Any
import anthropic
import json
from datetime import datetime

class ArticleProcessor:
    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.prompt_template = """
You are tasked with extracting and structuring information from payment system articles. Follow these rules precisely:

1. Parse the content exactly as per the below JSON schema
2. Include all information present in the article
3. Convert any checkmarks (✓) to boolean true, absence to false
4. Keep all date formats consistent (DD Month YYYY)
5. Extract all impact information even if tables are partially filled

REQUIRED OUTPUT FORMAT:
{
  "articles": [
    {
      "article_id": string,         // Extract from article number (e.g. "1.1")
      "title": string,              // Full article title as shown
      "reference_number": string,   // Format: "APRXX-XXXX"
      "mandatory": boolean,         // true if marked as Mandatory
      "version": {
        "number": string,          
        "type": string,            
        "change_notification": string
      },
      "implementation": {
        "dates": [                 
          {
            "date": string,        
            "time": string,        
            "type": string         
          }
        ]
      },
      "regional_applicability": [   
        {
          "region": string,        
          "acq": boolean,          
          "iss": boolean           
        }
      ],
      "impacts": {
        "system_impact": {
          "systems": [             
            {
              "name": string,      
              "impacted": boolean  
            }
          ]
        },
        "processing_impact": {
          "types": [              
            {
              "name": string,     
              "impacted": boolean 
            }
          ]
        },
        "testing_and_activation_impact": {
          "systems": [
            {
              "name": string,
              "testing_required": boolean,
              "testing_available": boolean,
              "activation_required": boolean
            }
          ]
        }
      },
      "brief": string,            
      "business_overview": string 
    }
  ],
  "metadata": {
    "total_articles": number,     
    "document_version": string,   
    "analysis_timestamp": string  
  }
}

ANALYZE THE FOLLOWING ARTICLE AND PROVIDE THE OUTPUT IN THE EXACT JSON FORMAT SPECIFIED ABOVE:

{article_content}
"""

    async def process_chunk(self, content: str) -> Dict[str, Any]:
        """Process a content chunk using Claude"""
        try:
            message = await self.client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=4096,
                temperature=0,
                messages=[
                    {
                        "role": "user",
                        "content": self.prompt_template.format(article_content=content)
                    }
                ]
            )
            
            return json.loads(message.content[0].text)
        except Exception as e:
            print(f"Error processing chunk: {e}")
            return None

    async def process_search_results(self, search_results: List[Any]) -> Dict[str, Any]:
        """Process search results and return structured article data"""
        all_articles = []
        seen_articles = set()

        for result in search_results:
            content = result.content if hasattr(result, 'content') else str(result)
            processed_result = await self.process_chunk(content)
            if processed_result and "articles" in processed_result:
                for article in processed_result["articles"]:
                    if article["article_id"] not in seen_articles:
                        all_articles.append(article)
                        seen_articles.add(article["article_id"])

        return {
            "articles": all_articles,
            "metadata": {
                "total_articles": len(all_articles),
                "timestamp": datetime.utcnow().isoformat()
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

@app.get("/api/articles")
async def get_articles(search_results: List[Any] = Depends(get_search_results)):
    """
    GET endpoint to process and return article information
    """
    try:
        processor = ArticleProcessor(api_key="your-anthropic-api-key")
        results = await processor.process_search_results(search_results)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Example usage:
"""
# Call the endpoint:
GET /api/articles

# Response will be in the format:
{
    "articles": [
        {
            "article_id": "1.1",
            "title": "Support of Global Processing",
            ...
        }
    ],
    "metadata": {
        "total_articles": 1,
        "timestamp": "2025-02-19T..."
    }
}
"""
