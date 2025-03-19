# Backend Dependencies for Content-Craft Visa API Agent
# Updated to support Anthropic Claude 3.5 Sonnet model

# Core web framework
fastapi==0.104.1
uvicorn[standard]==0.23.2
python-dotenv==1.0.0
pydantic==2.4.2
pydantic-settings==2.0.3
sqlalchemy==2.0.23
aiosqlite==0.19.0
aiofiles==23.2.1
python-multipart==0.0.6
httpx==0.25.1

# Authentication and security
bcrypt==4.0.1
passlib==1.7.4
python-jose[cryptography]==3.3.0

# LangChain and ML/AI dependencies (updated for Claude 3.5 Sonnet support)
langchain==0.3.20
langchain-anthropic==0.3.9  # Latest version with Claude 3.5 support
anthropic>=0.46.0  # Latest Anthropic SDK with Claude 3.5 Sonnet support
langchain-openai==0.3.7  # Updated to latest version
langchain-community==0.3.19  # Updated to latest version
openai==1.65.4  # Updated to latest version
chromadb==0.4.18
langgraph>=0.0.25  # Updated for better compatibility
PyYAML==6.0.1
markdown==3.5.1

# Document processing
PyMuPDF==1.23.7  # For PDF processing
docx2txt==0.8    # For Word document processing

# Data processing
numpy==1.26.1
pandas==2.1.2
tiktoken==0.5.1

# API Documentation
swagger-ui-bundle==0.0.9

# Testing and development
pytest==7.4.3
pytest-asyncio==0.21.1
black==23.10.1
isort==5.12.0
mypy==1.6.1

# Visualization
matplotlib==3.8.1
mermaid-diagram==0.1.0   # For generating Mermaid diagrams

# Logging
logging-formatter-colored==1.0.5   # For enhanced logging

# Install instructions:
# pip install -r requirements.txt
