from pydantic import BaseModel, Field, ConfigDict
from typing import Dict, Any, List, Optional, Union


class ToolRequest(BaseModel):
    """Base schema for tool requests."""
    model_config = ConfigDict(extra="forbid")
    
    tool_name: str = Field(description="Name of the tool to use")
    input: Dict[str, Any] = Field(description="Input parameters for the tool")


class DocumentationSearchRequest(BaseModel):
    """Request schema for documentation search tool."""
    model_config = ConfigDict(extra="forbid")
    
    query: str = Field(description="Search query")
    filter_criteria: Optional[Dict[str, Any]] = Field(default=None, description="Optional filters")
    top_k: Optional[int] = Field(default=5, description="Number of results to return")


class DocumentationSearchResult(BaseModel):
    """Result schema for documentation search."""
    model_config = ConfigDict(extra="forbid")
    
    content: str = Field(description="Document content")
    source: str = Field(description="Document source")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Document metadata")
    score: Optional[float] = Field(default=None, description="Search relevance score")


class CodeGenerationRequest(BaseModel):
    """Request schema for code generation tool."""
    model_config = ConfigDict(extra="forbid")
    
    operation_id: Optional[str] = Field(default=None, description="API operation ID")
    path: Optional[str] = Field(default=None, description="API path")
    method: Optional[str] = Field(default=None, description="HTTP method")
    language: str = Field(description="Programming language")
    include_auth: bool = Field(default=True, description="Include authentication")
    include_error_handling: bool = Field(default=True, description="Include error handling")


class WorkflowGenerationRequest(BaseModel):
    """Request schema for workflow generation tool."""
    model_config = ConfigDict(extra="forbid")
    
    task: str = Field(description="Task description")
    operations: List[str] = Field(default_factory=list, description="List of operations to include")
    include_code: bool = Field(default=True, description="Include code examples")
    language: Optional[str] = Field(default=None, description="Programming language if code is included")


class ApiEndpoint(BaseModel):
    """Schema for API endpoint information."""
    model_config = ConfigDict(extra="forbid")
    
    path: str = Field(description="Endpoint path")
    method: str = Field(description="HTTP method")
    operation_id: Optional[str] = Field(default=None, description="Operation ID")
    summary: Optional[str] = Field(default=None, description="Operation summary")
    description: Optional[str] = Field(default=None, description="Operation description")
    parameters: List[Dict[str, Any]] = Field(default_factory=list, description="Operation parameters")
    request_body: Optional[Dict[str, Any]] = Field(default=None, description="Request body schema")
    responses: Dict[str, Any] = Field(default_factory=dict, description="Response schemas")
