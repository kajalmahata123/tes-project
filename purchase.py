from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List
from anthropic import Anthropic
import os
import json

from starlette.middleware.cors import CORSMiddleware


app = FastAPI(title="Laptop Shop Assistant API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TransactionData(BaseModel):
    amount: float
    user_id: str
    merchant: str = "Apple Store"
    category: str = "Electronics"


class AnalysisResponse(BaseModel):
    cards: List[Dict]
    transaction: Dict
    status: str


SAMPLE_CARDS = [
    {
        "id": 1,
        "name": "Rewards Plus",
        "network": "Visa",
        "last4": "4567",
        "baseRewards": {
            "Electronics": 2,
            "default": 1
        },
        "offers": {
            "value": 5,
            "description": "5% extra cashback on electronics"
        }
    },
    {
        "id": 2,
        "name": "Travel Elite",
        "network": "Visa",
        "last4": "4589",
        "baseRewards": {
            "Electronics": 1.5,
            "default": 1
        },
        "offers": {
            "value": 2,
            "description": "Double points on electronics"
        }
    }
]


def analyze_with_claude(transaction: TransactionData, cards: List[Dict]) -> Dict:
    anthropic = Anthropic(api_key='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')

    prompt = f"""You are a rewards analysis expert. Analyze this purchase transaction and available payment cards to calculate exact rewards value.

Transaction:
- Amount: ${transaction.amount}
- Merchant: {transaction.merchant}
- Category: {transaction.category}

Cards:
{json.dumps(cards, indent=2)}

1. Calculate for each card:
   - Base rewards value using category-specific or default reward rates
   - Special offer value
   - Total value and effective reward rate
2. Format your response as a JSON object:
   {{
     "cards": [
       {{
         "id": card_id,
         "name": card_name,
         "network": card_network,
         "last4": last_4_digits,
         "rewards": {{
           "baseRewards": {{
             "value": calculated_base_value,
             "description": "X% base cashback on Category"
           }},
           "specialOffer": {{
             "value": calculated_offer_value,
             "description": "offer description"
           }},
           "totalValue": total_calculated_value,
           "effectiveRate": effective_reward_percentage
         }}
       }}
     ],
     "transaction": {{
       "amount": amount,
       "merchant": merchant_name,
       "category": category_name
     }},
     "status": "success"
   }}

Only return the JSON response without any additional text."""

    response = anthropic.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )

    # Parse Claude's JSON response
    try:
        return json.loads(response.content[0].text)
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=500, detail="Failed to parse Claude's response")


@app.post("/api/analyze-purchase")
async def analyze_purchase(transaction: TransactionData) -> Dict:
    try:
        return analyze_with_claude(transaction, SAMPLE_CARDS)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn


    uvicorn.run(app, host="0.0.0.0", port=8000)