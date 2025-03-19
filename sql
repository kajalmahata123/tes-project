from pydantic import BaseModel, Field, ConfigDict

from app.graphs.base_graph import BaseAgentGraph

import logging

logger = logging.getLogger(__name__)


class ToolsState(BaseModel):
    """State for the tools orchestration graph."""
    model_config = ConfigDict(extra="forbid")
    
    input: str = Field(description="The original user input")
    chat_history: List[BaseMessage] = Field(default_factory=list, description="Chat history")
    selected_tools: List[str] = Field(default_factory=list, description="Tools selected for use")
    tool_results: Dict[str, Any] = Field(default_factory=dict, description="Results from tools")
    current_tool: Optional[str] = Field(default=None, description="Currently executing tool")
    errors: List[str] = Field(default_factory=list, description="Errors encountered")
    output: Optional[str] = Field(default=None, description="Final response to user")
    completed: bool = Field(default=False, description="Whether processing is complete")
