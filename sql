# API Keys
ANTHROPIC_API_KEY=sk-ant-api03--TQ-7CJydgAA
OPENAI_API_KEY=sk-proj--DnlspUTHWYUmN0L268vVT4A

# App Configuration
DEBUG=true
HOST=0.0.0.0
PORT=8000

# Vector DB Configuration
VECTOR_DB_DIR=./data/vector_db
EMBEDDING_TYPE=openai  # Options: "chroma_basic", "openai"

# LLM Configuration
ANTHROPIC_MODEL=claude-3-5-sonnet-20240620

# Chat Memory Configuration
MAX_CHAT_SESSIONS=1000
CHAT_SESSION_TTL=86400  # 24 hours in seconds
