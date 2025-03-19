# app/api/routes/bootstrap.py

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
import uuid
from app.dependencies import get_db_manager
from app.config import get_settings
from app.db.manager import DatabaseManager
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


class BootstrapRequest(BaseModel):
    """Bootstrap request model for initial API key creation."""
    model_config = ConfigDict(extra="forbid")
    
    admin_secret: str = Field(description="Admin secret for bootstrapping")
    app_id: str = Field(description="Application identifier")
    app_name: str = Field(description="Human-readable application name")
    description: Optional[str] = Field(default="Initial admin API key", description="Description")


class ApiKeyResponse(BaseModel):
    """API key response model."""
    model_config = ConfigDict(extra="forbid")
    
    id: str = Field(description="API key ID")
    app_id: str = Field(description="Application ID")
    api_key: str = Field(description="Clear-text API key (only included when created)")
    app_name: str = Field(description="Application name")
    description: Optional[str] = Field(default=None, description="Description")
    is_active: bool = Field(description="Whether the key is active")
    created_at: str = Field(description="Creation timestamp")
    expires_at: Optional[str] = Field(default=None, description="Expiration timestamp")
    rate_limit: int = Field(description="Rate limit (requests per minute)")


@router.post("/bootstrap", response_model=ApiKeyResponse)
async def bootstrap_admin_key(
        request: BootstrapRequest,
        db_manager: DatabaseManager = Depends(get_db_manager)
):
    """
    Bootstrap the first admin API key. This endpoint should be disabled in production
    after initial setup or secured with a strong admin secret.

    This endpoint requires only the admin secret defined in the application settings.
    It does NOT require the X-API-Key or X-APP-ID headers.
    """
    # Verify admin secret
    admin_secret = get_settings().ADMIN_BOOTSTRAP_SECRET
    if not admin_secret or admin_secret == "change-this-in-production" or request.admin_secret != admin_secret:
        raise HTTPException(
            status_code=401,
            detail="Invalid admin secret"
        )

    # Check if app_id already has API keys
    existing_keys = await db_manager.get_app_api_keys(request.app_id)
    if existing_keys:
        raise HTTPException(
            status_code=400,
            detail=f"Application {request.app_id} already has {len(existing_keys)} API keys"
        )

    try:
        # Create admin API key with higher rate limit
        key_data = await db_manager.create_api_key(
            app_id=request.app_id,
            app_name=request.app_name,
            description=request.description,
            expires_in_days=None,  # Admin key doesn't expire
            rate_limit=500  # Higher rate limit for admin
        )

        logger.warning(f"Created bootstrap admin API key for app {request.app_id}")
        return key_data
    except Exception as e:
        logger.error(f"Failed to create bootstrap API key: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Failed to create bootstrap API key"
        )
