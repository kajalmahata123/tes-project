from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict, Any
from datetime import datetime


class ChatMessage(BaseModel):
    """Chat message schema."""
    model_config = ConfigDict(extra="forbid")
    
    role: str = Field(description="Message role (user or assistant)")
    content: str = Field(description="Message content")
    timestamp: str = Field(description="ISO format timestamp")

    @classmethod
    def user_message(cls, content: str) -> "ChatMessage":
        """Create a new user message."""
        return cls(
            role="user",
            content=content,
            timestamp=datetime.now().isoformat()
        )

    @classmethod
    def assistant_message(cls, content: str) -> "ChatMessage":
        """Create a new assistant message."""
        return cls(
            role="assistant",
            content=content,
            timestamp=datetime.now().isoformat()
        )


class ChatSession(BaseModel):
    """Chat session schema."""
    model_config = ConfigDict(extra="forbid")
    
    session_id: str = Field(description="Session identifier")
    user_id: Optional[str] = Field(default=None, description="User identifier")
    agent_type: str = Field(description="Agent type")
    created_at: str = Field(description="ISO format creation timestamp")
    last_activity: str = Field(description="ISO format last activity timestamp")
    messages: List[ChatMessage] = Field(default_factory=list, description="Chat messages")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Session metadata")
