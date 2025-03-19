from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict, Any
from datetime import datetime


class ChatMessage(BaseModel):
    """Chat message model."""
    model_config = ConfigDict(extra="forbid")
    
    role: str = Field(description="Message role (user or assistant)")
    content: str = Field(description="Message content")
    timestamp: str = Field(description="ISO format timestamp")


class ChatRequest(BaseModel):
    """Chat message request model."""
    model_config = ConfigDict(extra="forbid")
    
    message: str = Field(description="User message")
    session_id: Optional[str] = Field(default=None, description="Chat session ID")
    agent_type: Optional[str] = Field(default=None, description="Agent type to use")


class ChatResponse(BaseModel):
    """Chat message response model."""
    model_config = ConfigDict(extra="forbid")
    
    message_id: str = Field(description="Unique message ID")
    session_id: str = Field(description="Chat session ID")
    response: str = Field(description="Assistant response")
    agent_type: str = Field(description="Agent type used")
    app_id: Optional[str] = Field(default=None, description="Application ID that owns this session")


class SessionInfo(BaseModel):
    """Chat session information model."""
    model_config = ConfigDict(extra="forbid")
    
    session_id: str = Field(description="Chat session ID")
    agent_type: str = Field(description="Agent type")
    created_at: str = Field(description="ISO format timestamp of creation time")
    last_activity: str = Field(description="ISO format timestamp of last activity")
    message_count: int = Field(description="Number of messages in session")
    app_id: Optional[str] = Field(default=None, description="Application ID that owns this session")
    messages: Optional[List[ChatMessage]] = Field(default=None, description="Chat messages if requested")


class SessionListResponse(BaseModel):
    """Response model for listing sessions."""
    model_config = ConfigDict(extra="forbid")
    
    sessions: List[SessionInfo] = Field(description="List of session info")
    total: int = Field(description="Total number of sessions")
    limit: int = Field(description="Limit parameter used")
    offset: int = Field(description="Offset parameter used")


class AgentListResponse(BaseModel):
    """Response model for listing available agents."""
    model_config = ConfigDict(extra="forbid")
    
    agents: List[str] = Field(description="List of available agent types")
