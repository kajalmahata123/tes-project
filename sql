# app/api/routes/api_keys.py

from fastapi import APIRouter, Depends, HTTPException, Body, Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import datetime
from app.dependencies import get_db_manager, verify_api_key_and_app_id
from app.db.manager import DatabaseManager

router = APIRouter()

# API key request/response models
class ApiKeyCreate(BaseModel):
    """API key creation request model."""
    model_config = ConfigDict(extra="forbid")
    
    app_name: str = Field(description="Human-readable application name")
    description: Optional[str] = Field(default=None, description="Optional description")
    expires_in_days: Optional[int] = Field(default=None, description="Optional expiration period in days")
    rate_limit: Optional[int] = Field(default=100, description="Requests per minute allowed")

class ApiKeyResponse(BaseModel):
    """API key response model."""
    model_config = ConfigDict(extra="forbid")
    
    id: str = Field(description="API key ID")
    app_id: str = Field(description="Application ID")
    api_key: Optional[str] = Field(default=None, description="Clear-text API key (only included when created)")
    app_name: str = Field(description="Application name")
    description: Optional[str] = Field(default=None, description="Description")
    is_active: bool = Field(description="Whether the key is active")
    created_at: str = Field(description="Creation timestamp")
    last_used_at: Optional[str] = Field(default=None, description="Last usage timestamp")
    expires_at: Optional[str] = Field(default=None, description="Expiration timestamp")
    rate_limit: int = Field(description="Rate limit (requests per minute)")

class ApiKeyListResponse(BaseModel):
    """Response model for listing API keys."""
    model_config = ConfigDict(extra="forbid")
    
    keys: List[ApiKeyResponse] = Field(description="List of API keys")

# Routes for API key management
@router.post("/keys", response_model=ApiKeyResponse)
async def create_api_key(
    request: ApiKeyCreate,
    auth: dict = Depends(verify_api_key_and_app_id),
    db_manager: DatabaseManager = Depends(get_db_manager)
):
    """
    Create a new API key for the application.
    
    Only authenticated administrators can create API keys.
    The API key is returned only once in the response.
    """
    app_id = auth["app_id"]
    
    try:
        key_data = await db_manager.create_api_key(
            app_id=app_id,
            app_name=request.app_name,
            description=request.description,
            expires_in_days=request.expires_in_days,
            rate_limit=request.rate_limit or 100
        )
        return key_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create API key: {str(e)}")

@router.get("/keys", response_model=ApiKeyListResponse)
async def list_api_keys(
    auth: dict = Depends(verify_api_key_and_app_id),
    db_manager: DatabaseManager = Depends(get_db_manager)
):
    """
    List all API keys for the application.
    
    The actual API keys are not included in the response.
    """
    app_id = auth["app_id"]
    
    try:
        keys = await db_manager.get_app_api_keys(app_id)
        # Remove the API key from the response
        for key in keys:
            key.pop("api_key", None)
        return {"keys": keys}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list API keys: {str(e)}")

@router.delete("/keys/{key_id}")
async def deactivate_api_key(
    key_id: str = Path(..., description="API key ID to deactivate"),
    auth: dict = Depends(verify_api_key_and_app_id),
    db_manager: DatabaseManager = Depends(get_db_manager)
):
    """
    Deactivate an API key.
    
    Once deactivated, the key can no longer be used for authentication.
    """
    app_id = auth["app_id"]
    
    # Verify the key belongs to this app
    keys = await db_manager.get_app_api_keys(app_id)
    key_ids = [key["id"] for key in keys]
    
    if key_id not in key_ids:
        raise HTTPException(status_code=404, detail="API key not found")
    
    success = await db_manager.deactivate_api_key(key_id)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to deactivate API key")
    
    return {"status": "success", "message": "API key deactivated"}
