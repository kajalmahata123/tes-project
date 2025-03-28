# Content-Craft Visa API Agent - Backend Design Document

## 1. System Overview

The  Visa API Agent is an intelligent chatbot system built to assist users with Visa API-related queries, code generation, and workflow creation. The system uses advanced LLM capabilities (Claude 3.5 Sonnet model) combined with a knowledge base to provide contextually relevant responses.

### 1.1 System Goals

- Provide accurate information about Visa APIs
- Generate code examples for Visa API integration
- Create workflow diagrams and documentation
- Maintain conversation context through sessions
- Securely manage API access through authentication
- Store and retrieve conversation history

## 2. Architecture Overview

The application follows a modern, modular architecture based on:

- **FastAPI** for the web API framework
- **LangChain** for LLM orchestration
- **Chroma DB** for vector storage and semantic search
- **SQLite** for relational data storage (with async support)
- **Anthropic Claude 3.5 Sonnet** as the primary LLM
- **OpenAI** for embeddings (text-embedding-3-large)

### 2.1 High-Level Architecture Diagram

```
┌─────────────────┐     ┌──────────────────┐     ┌───────────────────┐
│                 │     │                  │     │                   │
│  Client         │────▶│  FastAPI Backend │────▶│  Agent System     │
│  (Web/Mobile)   │     │  (RESTful API)   │     │  (LangChain)      │
│                 │     │                  │     │                   │
└─────────────────┘     └──────────────────┘     └───────────────────┘
                                                          │
                                                          │
                                                          ▼
                         ┌──────────────────┐    ┌────────────────────┐
                         │                  │    │                    │
                         │  Vector DB       │◀───│  LLM Services      │
                         │  (ChromaDB)      │    │  (Claude/OpenAI)   │
                         │                  │    │                    │
                         └──────────────────┘    └────────────────────┘
                                │                          │
                                │                          │
                                ▼                          ▼
                         ┌──────────────────┐    ┌────────────────────┐
                         │                  │    │                    │
                         │  Document Store  │    │  Session DB        │
                         │  (API Docs)      │    │  (SQLite)          │
                         │                  │    │                    │
                         └──────────────────┘    └────────────────────┘
```

## 3. Core Components

### 3.1 API Layer (FastAPI)

The API layer is built with FastAPI and provides endpoints for:

- **Chat**: Send messages and receive responses
- **Upload**: Upload documents to the knowledge base
- **API Keys**: Manage authentication keys
- **Health**: Check system status
- **Bootstrap**: Initialize system components

API endpoints follow RESTful principles and include proper authentication, validation, and error handling.

#### Key Endpoints:

- `POST /api/v1/chat/message`: Send a message to the agent
- `POST /api/v1/chat/session`: Create a new chat session
- `GET /api/v1/chat/session/{session_id}`: Get details of a specific session
- `POST /api/v1/upload/document`: Upload a document to the knowledge base
- `GET /api/v1/health/status`: Get system health status

### 3.2 Agent System

The agent system is built around a factory pattern that instantiates different types of agents based on the user's needs:

- **VisaAPIAgent**: Answers questions about Visa APIs
- **CodeGeneratorAgent**: Generates code examples for Visa API integration
- **WorkflowAgent**: Creates workflow diagrams and documentation

Each agent extends a `BaseAgent` class that provides common functionality.

### 3.3 Knowledge Base

The knowledge base is implemented using ChromaDB for vector storage and retrieval. It:

- Processes and stores Visa API documentation
- Chunks documents into manageable pieces
- Creates embeddings for semantic search
- Provides relevant context to agents when answering questions

### 3.4 Session Management

The session manager maintains the state of conversations, including:

- User messages and agent responses
- Session metadata (creation time, expiry)
- Associated agent type
- Conversation context

Sessions are persisted in the SQLite database for durability.

### 3.5 Database Layer

The database layer uses SQLite with async support (aiosqlite) and includes:

- Session storage
- API key management
- User preferences

The database schema is designed for efficient querying and includes appropriate indexes.

## 4. Data Flow

### 4.1 Chat Message Flow

1. Client sends a message to `/api/v1/chat/message` with session ID and content
2. API layer authenticates the request and validates input
3. Session manager retrieves the session context
4. Agent factory instantiates or retrieves the appropriate agent
5. Agent processes the message with LLM support
6. Knowledge base provides relevant context based on query
7. Agent generates a response
8. Session manager updates the session with the new message and response
9. Response is returned to the client

### 4.2 Document Upload Flow

1. Client uploads a document to `/api/v1/upload/document`
2. API layer validates the document format and content
3. Document is stored in the document store
4. Knowledge base processes the document:
   - Splits into chunks
   - Creates embeddings
   - Stores in ChromaDB
5. Success response is returned to the client

### 4.3 API to Agent Interaction Diagram

The following diagram illustrates the detailed flow from REST API endpoints to agents and how responses are generated:

```
┌─────────────────┐         ┌─────────────────┐         ┌─────────────────┐
│                 │         │                 │         │                 │
│  Client         │         │  FastAPI        │         │  SessionManager │
│                 │         │  Endpoints      │         │                 │
│                 │         │                 │         │                 │
└────────┬────────┘         └────────┬────────┘         └────────┬────────┘
         │                           │                           │
         │  1. HTTP Request          │                           │
         │ ────────────────────────▶ │                           │
         │                           │  2. Validate Request      │
         │                           │ ─────────────────┐        │
         │                           │                  │        │
         │                           │ ◀─────────────────┘        │
         │                           │                           │
         │                           │  3. Get/Create Session    │
         │                           │ ────────────────────────▶ │
         │                           │                           │
         │                           │ ◀──────────────────────── │
         │                           │  4. Return Session        │
         │                           │                           │
┌────────┴────────┐         ┌────────┴────────┐         ┌────────┴────────┐
│                 │         │                 │         │                 │
│  Client         │         │  FastAPI        │         │  AgentFactory   │
│                 │         │  Endpoints      │         │                 │
│                 │         │                 │         │                 │
└─────────────────┘         └────────┬────────┘         └────────┬────────┘
                                     │                           │
                                     │  5. Get Agent Instance    │
                                     │ ────────────────────────▶ │
                                     │                           │ 
                                     │ ◀──────────────────────── │
                                     │  6. Return Agent          │
                                     │                           │
         ┌─────────────────────────┬─────────────────────────┬────────────────────────┐
         │                         │                         │                        │
         ▼                         ▼                         ▼                        │
┌─────────────────────┐  ┌─────────────────────┐  ┌─────────────────────┐            │
│                     │  │                     │  │                     │            │
│ VisaAPIAgent        │  │ CodeGeneratorAgent  │  │ WorkflowAgent       │            │
│                     │  │                     │  │                     │            │
└─────────┬───────────┘  └─────────┬───────────┘  └─────────┬───────────┘            │
          │                        │                        │                        │
          │ 7a. Process            │ 7b. Process            │ 7c. Process            │
          │ Query                  │ Query                  │ Query                  │
          │                        │                        │                        │
          ▼                        ▼                        ▼                        │
┌─────────────────────┐  ┌─────────────────────┐  ┌─────────────────────┐            │
│                     │  │                     │  │                     │            │
│ LLM Service         │  │ LLM Service         │  │ LLM Service         │            │
│ (Claude 3.5 Sonnet) │  │ (Claude 3.5 Sonnet) │  │ (Claude 3.5 Sonnet) │            │
│                     │  │                     │  │                     │            │
└─────────┬───────────┘  └─────────┬───────────┘  └─────────┬───────────┘            │
          │                        │                        │                        │
          │ 8a. Response           │ 8b. Response           │ 8c. Response           │
          │                        │                        │                        │
          │                        │                        │                        │
          │                        ▼                        │                        │
          └───────────────────────▶┌─────────────────────┐◀───────────────────────────┘
                                   │                     │
                                   │ AgentFactory        │
                                   │                     │
                                   └─────────┬───────────┘
                                             │
                                             │ 9. Return Response
                                             │
                                             ▼
                                   ┌─────────────────────┐
                                   │                     │
                                   │ SessionManager      │
                                   │                     │
                                   └─────────┬───────────┘
                                             │
                                             │ 10. Save Response
                                             │
                                             ▼
                                   ┌─────────────────────┐         ┌─────────────────┐
                                   │                     │         │                 │
                                   │ FastAPI Endpoints   │         │ Client          │
                                   │                     │         │                 │
                                   └─────────┬───────────┘         └─────────────────┘
                                             │                              ▲
                                             │ 11. HTTP Response            │
                                             └──────────────────────────────┘
```

### 4.4 Agent to Tools Interaction Flow

This diagram shows how agents leverage various tools to enhance their responses:

```
┌────────────────────────────────────────────────────────────────────┐
│                                                                    │
│                            BaseAgent                               │
│                                                                    │
└───────────────────────────────┬────────────────────────────────────┘
                                │
                                │ 1. Process User Query
                                │
                                ▼
┌────────────────────────────────────────────────────────────────────┐
│                                                                    │
│                        Query Understanding                         │
│                                                                    │
└───────────────────────────────┬────────────────────────────────────┘
                                │
                                │ 2. Identify Required Tools
                                │
                                ▼
                ┌───────────────┴───────────────┐
                │                               │
                ▼                               ▼
┌───────────────────────┐           ┌───────────────────────┐
│                       │           │                       │
│ Knowledge Retrieval   │           │ Code Generation       │
│                       │           │                       │
└───────────┬───────────┘           └───────────┬───────────┘
            │                                   │
            ▼                                   ▼
┌───────────────────────┐           ┌───────────────────────┐
│                       │           │                       │
│ Vector Search         │           │ Template Expansion    │
│ (ChromaDB)            │           │                       │
│                       │           │                       │
└───────────┬───────────┘           └───────────┬───────────┘
            │                                   │
            │                                   │
            ▼                                   ▼
┌───────────────────────┐           ┌───────────────────────┐
│                       │           │                       │
│ Document Context      │           │ Generated Code        │
│                       │           │                       │
└───────────┬───────────┘           └───────────┬───────────┘
            │                                   │
            └───────────────┬───────────────────┘
                            │
                            │ 3. Tool Outputs
                            │
                            ▼
┌────────────────────────────────────────────────────────────────────┐
│                                                                    │
│                             LLM Service                            │
│                           (Claude/OpenAI)                          │
│                                                                    │
└───────────────────────────────┬────────────────────────────────────┘
                                │
                                │ 4. Generate Response
                                │
                                ▼
┌────────────────────────────────────────────────────────────────────┐
│                                                                    │
│                          Final Response                            │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

### 4.5 Agent Tools Ecosystem

The agents have access to various tools that enhance their capabilities:

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│                    Agent Tools Ecosystem                        │
│                                                                 │
└─────────────────────────────────┬───────────────────────────────┘
                                  │
                                  │
         ┌────────────────────────┼────────────────────────┐
         │                        │                        │
         ▼                        ▼                        ▼
┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│                  │    │                  │    │                  │
│ Knowledge Tools  │    │  Code Tools      │    │ Document Tools   │
│                  │    │                  │    │                  │
└──────┬───────────┘    └──────┬───────────┘    └──────┬───────────┘
       │                       │                       │
       ▼                       ▼                       ▼
┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│• Vector Search   │    │• Code Generator  │    │• PDF Parser      │
│• Semantic Search │    │• Syntax Checker  │    │• Markdown Parser │
│• Context Ranking │    │• Code Explainer  │    │• Document Chunker│
│• Fact Extraction │    │• Test Generator  │    │• Table Extractor │
└──────────────────┘    └──────────────────┘    └──────────────────┘
       │                       │                       │
       │                       │                       │
       ▼                       ▼                       ▼
┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│• API Reference   │    │• Language SDKs    │    │• Visualizer     │
│• Documentation   │    │• Code Libraries   │    │• Diagram Creator│
│• Schema Lookup   │    │• Best Practices   │    │• Workflow Tools │
│• Example Search  │    │• Security Patterns│    │• Template Engine│
└──────────────────┘    └──────────────────┘    └──────────────────┘
```

## 5. Security Considerations

### 5.1 Authentication

The system uses API key authentication:
- Keys are transmitted in HTTP headers
- Keys are hashed in the database
- Rate limiting is applied to prevent abuse

### 5.2 Data Protection

- Sensitive data is not persisted unless necessary
- Environment variables are used for secrets
- Database access is restricted to the application

### 5.3 Input Validation

- All user inputs are validated
- Strict schema validation using Pydantic
- Input sanitization to prevent injection attacks

## 6. Performance Considerations

### 6.1 Caching

- Session data is cached for quick access
- LLM responses are cached when appropriate
- Embeddings are pre-computed and stored

### 6.2 Asynchronous Processing

- FastAPI's async capabilities are leveraged
- Database operations are async
- LLM requests are processed asynchronously

### 6.3 Resource Management

- Connection pooling for database access
- Efficient vector search algorithms
- LLM prompt optimization to reduce token usage

## 7. Scalability Considerations

### 7.1 Horizontal Scaling

- Stateless API design allows multiple instances
- Database can be migrated to a distributed system
- Vector store can be scaled independently

### 7.2 Vertical Scaling

- Configurable resource allocation
- Performance monitoring to identify bottlenecks
- Batch processing for high-volume operations

## 8. Testing Strategy

### 8.1 Unit Testing

- Testing individual components in isolation
- Mocking external dependencies
- High test coverage for core logic

### 8.2 Integration Testing

- Testing component interactions
- End-to-end API tests
- Database migration tests

### 8.3 Performance Testing

- Load testing for API endpoints
- Stress testing for concurrent sessions
- Benchmark tests for vector search

## 9. Deployment Considerations

### 9.1 Environment Configuration

- Environment variables for configuration
- Separation of development and production settings
- Infrastructure as code for reproducibility

### 9.2 Monitoring

- Logging of all operations
- Error tracking and alerting
- Performance metrics collection

### 9.3 Continuous Integration/Deployment

- Automated testing in CI pipeline
- Versioned deployments
- Rollback capabilities

## 10. Future Enhancements

- Multi-tenant support
- Additional agent types
- Enhanced document processing capabilities
- Integration with external systems
- Real-time collaboration features

## 11. Technical Dependencies

### Core Dependencies
- FastAPI (0.104.1)
- Pydantic (≥2.7.4, <3.0.0)
- SQLAlchemy (2.0.23)
- LangChain (0.3.20)
- LangChain-Anthropic (0.3.9)
- LangChain-OpenAI (0.3.7)
- LangChain-Chroma (≥0.0.5)
- ChromaDB (0.4.18)
- NumPy (≥1.26.0, <2.0.0)
- Tiktoken (≥0.7.0, <1.0.0)

### Authentication & Security
- bcrypt (4.0.1)
- passlib (1.7.4)
- python-jose (3.3.0)

## 12. API Documentation

The API is self-documenting using OpenAPI standards and can be accessed at:
- Swagger UI: `/api/v1/docs`
- ReDoc: `/api/v1/redoc`
- OpenAPI JSON: `/api/v1/openapi.json`

---

## Appendix A: Database Schema

### Sessions Table
- `id`: UUID (Primary Key)
- `user_id`: String
- `agent_type`: String
- `created_at`: Timestamp
- `updated_at`: Timestamp
- `expires_at`: Timestamp
- `metadata`: JSON
- `app_id`: String

### Messages Table
- `id`: UUID (Primary Key)
- `session_id`: UUID (Foreign Key)
- `role`: String
- `content`: Text
- `timestamp`: Timestamp
- `metadata`: JSON

### API Keys Table
- `id`: UUID (Primary Key)
- `key_hash`: String
- `name`: String
- `created_at`: Timestamp
- `expires_at`: Timestamp
- `is_active`: Boolean
- `permissions`: JSON 