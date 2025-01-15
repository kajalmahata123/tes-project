# Card Analysis API

FastAPI backend for credit card analysis and recommendations.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

After starting the server, you can access:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Available Endpoints

- GET `/api/checkout-analysis` - Get checkout analysis data
- POST `/api/analyze-transaction` - Analyze a specific transaction
- POST `/api/cards/{card_id}/set-default` - Set default card
- GET `/api/cards/{card_id}/benefits` - Get card benefits

## Development

The project structure is organized as follows:
```
card_analysis/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application initialization
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py    # API endpoints
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py   # Pydantic models
│   └── utils/
│       ├── __init__.py
│       └── sample_data.py # Sample data for development
├── requirements.txt
└── README.md
```