# Content-Craft Visa API Agent

A specialized application for providing AI-assisted guidance on Visa API implementation and integration. This project consists of a FastAPI backend with LangChain-powered AI agents and a React frontend.

## Application Overview

The Content-Craft Visa API Agent provides:
- AI-powered chat agents specialized in different aspects of Visa API integration
- Code generation for multiple programming languages
- Implementation workflow guidance and visualization
- Documentation search and contextual assistance
- **Powered by Claude 3.5 Sonnet** - State-of-the-art LLM with advanced coding, reasoning, and context understanding capabilities

## Project Structure

```
├── app/                  # Backend FastAPI application
│   ├── agents/           # AI agent implementations
│   ├── api/              # API routes and endpoints
│   ├── core/             # Core functionality
│   ├── data/             # Application data
│   ├── graphs/           # LangGraph agent workflows
│   ├── llm/              # LLM integration services
│   ├── schemas/          # Pydantic models
│   ├── tools/            # Agent tools
│   └── utils/            # Utility functions
├── frontend_app/         # React frontend application
├── data/                 # Database and storage
├── logs/                 # Application logs
└── static/               # Static files
```

## API Keys and Authentication

This application requires API keys for authentication. Below are the default keys for development:

### Admin API Key
```json
{
  "id": "e78e840a-85c5-4a49-8a1d-2da8472e19da",
  "app_id": "Visa_api_Bot",
  "api_key": "sk_7c9a4b792db9296e86fdaf6efc98d550f6cbb3dd11ba16e5",
  "app_name": "Visa API Bot Application",
  "description": "Initial admin API key",
  "is_active": true,
  "created_at": "2025-03-18T02:37:25.268241",
  "expires_at": null,
  "rate_limit": 500
}
```

### Client Application Key
```json
{
  "id": "eb466a71-d649-4620-b2c6-5664e8ba2aae",
  "app_id": "Visa_api_Bot",
  "api_key": "sk_2c23d0795fce8e84bf9f4e3f4401ebf910727a13dd82a0a4",
  "app_name": "ClientApp1",
  "description": "This is a Client Application",
  "is_active": true,
  "created_at": "2025-03-18T03:07:32.397497",
  "last_used_at": null,
  "expires_at": null,
  "rate_limit": 100
}
```

## Installation and Setup

### Backend Setup

1. Clone the repository:
   ```bash
   git clone [repository-url]
   cd content-craft/visa_api_agent
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   ```
   Edit the `.env` file with your API keys and configuration.

5. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```
   The API will be available at http://localhost:8000.

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend_app
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```
   The frontend will be available at http://localhost:3000.

## Development

### Backend Development

- API Documentation: http://localhost:8000/docs
- ReDoc interface: http://localhost:8000/redoc
- Admin interface: http://localhost:8000/api/admin

### Frontend Development

The frontend is built with React, TypeScript, and Tailwind CSS. Key components:
- React Router for navigation
- Axios for API communication
- Tailwind CSS for styling
- Mermaid for diagram rendering
- React Markdown for content rendering

## Environment Variables

Key environment variables:

```
# API Configuration
PROJECT_NAME=Visa API Agent
API_PREFIX=/api
DEBUG=false

# Database
DB_URL=sqlite+aiosqlite:///./app/data/sessions.db

# Security
SECRET_KEY=your-secret-key
API_KEY_HEADER_NAME=X-API-Key
APP_ID_HEADER_NAME=X-App-ID

# LLM Configuration
LLM_PROVIDER=anthropic
ANTHROPIC_MODEL=claude-3-5-sonnet-20240620  # Using Claude 3.5 Sonnet
ANTHROPIC_API_KEY=your-anthropic-key
OPENAI_API_KEY=your-openai-key
```

## License

[License information]

## Contact

For questions or support, contact [contact information].