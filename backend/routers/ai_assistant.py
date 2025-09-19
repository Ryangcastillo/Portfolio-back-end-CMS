from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from typing import Optional, Dict, Any
import httpx
import json

from ..database import get_db, AIProvider
from ..auth import get_current_user
from ..security import requires_roles, mask_secrets
from ..models.ai_models import AIRequest, AIResponse, AIProviderConfig
from ..security import encrypt_value, decrypt_value

router = APIRouter()

class AIProviderManager:
    """Manages different AI providers with flexible API key configuration"""
    
    def __init__(self):
        self.providers = {
            "openrouter": {
                "base_url": "https://openrouter.ai/api/v1",
                "headers_template": {
                    "Authorization": "Bearer {api_key}",
                    "HTTP-Referer": "https://your-cms-domain.com",
                    "X-Title": "Stitch CMS"
                }
            },
            "openai": {
                "base_url": "https://api.openai.com/v1",
                "headers_template": {
                    "Authorization": "Bearer {api_key}",
                    "Content-Type": "application/json"
                }
            },
            "anthropic": {
                "base_url": "https://api.anthropic.com/v1",
                "headers_template": {
                    "x-api-key": "{api_key}",
                    "Content-Type": "application/json",
                    "anthropic-version": "2023-06-01"
                }
            }
        }
    
    async def get_active_provider(self, db: AsyncSession) -> Optional[AIProvider]:
        """Get the currently active AI provider"""
        result = await db.execute(
            select(AIProvider).where(AIProvider.is_active == True)
        )
        return result.scalar_one_or_none()
    
    async def make_ai_request(self, provider: AIProvider, prompt: str, model: Optional[str] = None) -> Dict[Any, Any]:
        """Make a request to the AI provider"""
        if provider.name not in self.providers:
            raise HTTPException(status_code=400, detail=f"Unsupported AI provider: {provider.name}")
        
        provider_config = self.providers[provider.name]
        headers = {}
        
        # Build headers from template
        # Decrypt stored API key before injecting into headers
        raw_key = None
        if provider.api_key:
            try:
                raw_key = decrypt_value(provider.api_key)
            except Exception:
                raise HTTPException(status_code=400, detail="Stored API key could not be decrypted")
        for key, value in provider_config["headers_template"].items():
            headers[key] = value.format(api_key=raw_key or "")

        # Prepare request based on provider
        payload: Dict[str, Any] = {}
        endpoint: str = ""
        if provider.name == "openrouter":
            payload = {
                "model": model or "meta-llama/llama-3.1-8b-instruct:free",
                "messages": [{"role": "user", "content": prompt}]
            }
            endpoint = f"{provider.base_url}/chat/completions"
        elif provider.name == "openai":
            payload = {
                "model": model or "gpt-3.5-turbo",
                "messages": [{"role": "user", "content": prompt}]
            }
            endpoint = f"{provider.base_url}/chat/completions"
        elif provider.name == "anthropic":
            payload = {
                "model": model or "claude-3-haiku-20240307",
                "max_tokens": 1000,
                "messages": [{"role": "user", "content": prompt}]
            }
            endpoint = f"{provider.base_url}/messages"

        if not endpoint:
            raise HTTPException(status_code=500, detail="Failed to determine provider endpoint")

        async with httpx.AsyncClient() as client:
            response = await client.post(endpoint, headers=headers, json=payload)
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"AI provider error: {response.text}"
                )
            return response.json()

ai_manager = AIProviderManager()

@router.post("/generate-content")
async def generate_content(
    request: AIRequest,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Generate content using AI"""
    provider = await ai_manager.get_active_provider(db)
    if not provider:
        raise HTTPException(status_code=400, detail="No active AI provider configured")
    
    try:
        response = await ai_manager.make_ai_request(
            provider, 
            request.prompt, 
            request.model or ""
        )
        
        return AIResponse(
            content=response.get("choices", [{}])[0].get("message", {}).get("content", ""),
            provider=provider.name,
            model=request.model,
            usage=response.get("usage", {})
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI generation failed: {str(e)}")

@router.get("/providers")
async def list_providers(
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """List all configured AI providers"""
    result = await db.execute(select(AIProvider))
    providers = result.scalars().all()
    
    return [
        {
            "id": p.id,
            "name": p.name,
            "display_name": p.display_name,
            "is_active": p.is_active,
            "is_default": p.is_default,
            "has_api_key": bool(p.api_key),
        }
        for p in providers
    ]

@router.post("/providers", dependencies=[Depends(requires_roles("admin"))])
async def create_provider(
    config: AIProviderConfig,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Create or update an AI provider configuration"""
    # Check if provider already exists
    result = await db.execute(
        select(AIProvider).where(AIProvider.name == config.name)
    )
    existing = result.scalar_one_or_none()
    
    if existing:
        # Update existing provider
        if config.api_key:
            existing.api_key = encrypt_value(config.api_key)
        existing.base_url = config.base_url
        existing.is_active = config.is_active
        existing.configuration = config.configuration
        provider = existing
    else:
        # Create new provider
        provider = AIProvider(
            name=config.name,
            display_name=config.display_name,
            api_key=encrypt_value(config.api_key) if config.api_key else None,
            base_url=config.base_url,
            is_active=config.is_active,
            configuration=config.configuration
        )
        db.add(provider)
    
    # If this provider is set as default, deactivate others
    if config.is_active:
        await db.execute(
            select(AIProvider).where(AIProvider.id != provider.id)
        )
        for p in (await db.execute(select(AIProvider))).scalars().all():
            if p.id != provider.id:
                p.is_active = False
    
    await db.commit()
    await db.refresh(provider)
    
    return {"message": "AI provider configured successfully", "provider_id": provider.id}
