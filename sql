from pydantic import BaseModel, Field, ConfigDict
from typing import Dict, List, Any, Optional


class AgentConfig(BaseModel):
    """Configuration parameters for agent instantiation."""
    model_config = ConfigDict(extra="forbid")
    
    name: str = Field(description="Agent name")
    api_keys: Dict[str, str] = Field(default_factory=dict, description="API keys for services")
    knowledge_base: Any = Field(default=None, description="Knowledge base instance")
    tools: List[Any] = Field(default_factory=list, description="Tools available to the agent")
    max_iterations: int = Field(default=3, description="Maximum reasoning iterations")
    temperature: float = Field(default=0.2, description="LLM temperature")
    system_prompt: Optional[str] = Field(default=None, description="Custom system prompt")


class AgentCapabilities(BaseModel):
    """Agent capabilities for user interface."""
    model_config = ConfigDict(extra="forbid")
    
    name: str = Field(description="Agent name")
    type: str = Field(description="Agent type")
    description: str = Field(description="Agent description")
    capabilities: List[str] = Field(description="List of agent capabilities")
    tools: List[str] = Field(default_factory=list, description="Tools used by the agent")
