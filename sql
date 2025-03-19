from pydantic import BaseModel, Field, ConfigDict
import hashlib

logger = logging.getLogger(__name__)


class ReActState(BaseModel):
    """State for the ReAct agent graph."""
    model_config = ConfigDict(extra="forbid")
    
    input: str = Field(description="The original user input")
    chat_history: List[BaseMessage] = Field(default_factory=list, description="Chat history")
    thought: str = Field(default="", description="Agent's current thought")
    action_name: Optional[str] = Field(default=None, description="Tool to use")
    action_input: Optional[Dict[str, Any]] = Field(default=None, description="Input for the tool")
    observation: Optional[str] = Field(default=None, description="Result from the tool")
    output: Optional[str] = Field(default=None, description="Final response to the user")
    iterations: int = Field(default=0, description="Number of ReAct cycles")
    # Add accumulated knowledge tracking
    accumulated_knowledge: Dict[str, str] = Field(default_factory=dict, description="Knowledge gathered from tools")
    previous_queries: List[str] = Field(default_factory=list, description="Previous search queries")
    new_request: bool = Field(default=True, description="Flag indicating if this is a new request")
    # Session-level caches
    tool_cache: Dict[str, str] = Field(default_factory=dict, description="Cache for tool results")
    llm_cache: Dict[str, str] = Field(default_factory=dict, description="Cache for LLM responses")
