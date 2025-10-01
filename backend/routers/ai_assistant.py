from __future__ import annotations

from typing import Any, Dict, Optional

import httpx
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..auth import get_current_user
from ..database import AIProvider, get_db
from ..models.ai_models import AIProviderConfig, AIRequest, AIResponse
from ..security import decrypt_value, encrypt_value, requires_roles

router = APIRouter()


def _extract_ai_message(provider_name: str, payload: Dict[str, Any]) -> str:
    """Normalise the chat completion response into a plain string."""
    if provider_name == "anthropic":
        # Claude responses include a list of content blocks
        content = payload.get("content") or payload.get("messages")
        if isinstance(content, list) and content:
            block = content[0]
            if isinstance(block, dict):
                if "text" in block:
                    return block.get("text", "")
                inner = block.get("content")
                if isinstance(inner, list) and inner:
                    text_block = inner[0]
                    if isinstance(text_block, dict):
                        return text_block.get("text", "")
        return payload.get("output_text", "")

    choices = payload.get("choices")
    if isinstance(choices, list) and choices:
        choice = choices[0]
        if isinstance(choice, dict):
            message = choice.get("message")
            if isinstance(message, dict):
                return message.get("content", "")
            if "text" in choice:
                return choice.get("text", "")
    message = payload.get("message")
    if isinstance(message, str):
        return message
    if isinstance(message, dict):
        return message.get("content", "")
    return payload.get("content", "") if isinstance(payload.get("content"), str) else ""


class AIProviderManager:
    """Manages different AI providers with flexible API key configuration."""

    def __init__(self) -> None:
        self.providers: Dict[str, Dict[str, Any]] = {
            "openrouter": {
                "base_url": "https://openrouter.ai/api/v1",
                "default_model": "meta-llama/llama-3.1-8b-instruct:free",
                "headers_template": {
                    "Authorization": "Bearer {api_key}",
                    "HTTP-Referer": "https://your-cms-domain.com",
                    "X-Title": "Stitch CMS",
                },
            },
            "openai": {
                "base_url": "https://api.openai.com/v1",
                "default_model": "gpt-3.5-turbo",
                "headers_template": {
                    "Authorization": "Bearer {api_key}",
                    "Content-Type": "application/json",
                },
            },
            "anthropic": {
                "base_url": "https://api.anthropic.com/v1",
                "default_model": "claude-3-haiku-20240307",
                "headers_template": {
                    "x-api-key": "{api_key}",
                    "Content-Type": "application/json",
                    "anthropic-version": "2023-06-01",
                },
            },
        }

    async def get_active_provider(self, db: AsyncSession) -> Optional[AIProvider]:
        """Fetch the currently active AI provider configuration."""
        result = await db.execute(select(AIProvider).where(AIProvider.is_active == True))
        return result.scalar_one_or_none()

    async def make_ai_request(self, provider: AIProvider, request: AIRequest) -> Dict[str, Any]:
        """Invoke the configured AI provider with the supplied prompt."""
        if not request.prompt or not request.prompt.strip():
            raise HTTPException(status_code=400, detail="Prompt cannot be empty")

        provider_config = self.providers.get(provider.name)
        if not provider_config:
            raise HTTPException(status_code=400, detail=f"Unsupported AI provider: {provider.name}")

        # Decrypt the API key that is stored in the database.
        raw_key: Optional[str] = None
        if provider.api_key:
            try:
                raw_key = decrypt_value(provider.api_key)
            except Exception as exc:  # pragma: no cover - defensive branch
                raise HTTPException(status_code=400, detail="Stored API key could not be decrypted") from exc

        if not raw_key:
            raise HTTPException(status_code=400, detail="No API key configured for the active AI provider")

        headers = {
            header: template.format(api_key=raw_key)
            for header, template in provider_config["headers_template"].items()
        }

        base_url = provider.base_url or provider_config.get("base_url")
        if not base_url:
            raise HTTPException(status_code=400, detail="No base URL configured for the AI provider")

        temperature = request.temperature if request.temperature is not None else 0.7
        temperature = max(0.0, min(2.0, float(temperature)))
        max_tokens = request.max_tokens or 1000
        max_tokens = max(1, min(int(max_tokens), 4000))
        model_name = request.model or provider_config.get("default_model")

        # Build message payloads with optional system context support.
        user_messages = []
        if request.context:
            user_messages.append({"role": "system", "content": request.context})
        user_messages.append({"role": "user", "content": request.prompt})

        payload: Dict[str, Any]
        endpoint: str
        if provider.name in {"openrouter", "openai"}:
            payload = {
                "model": model_name,
                "messages": user_messages,
                "temperature": temperature,
            }
            if provider.name == "openrouter":
                # OpenRouter surfaces usage pricing based on max tokens supplied
                payload["max_tokens"] = max_tokens
            elif request.max_tokens is not None:
                payload["max_tokens"] = max_tokens
            endpoint = f"{base_url}/chat/completions"
        elif provider.name == "anthropic":
            anthropic_messages = [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": request.prompt},
                    ],
                }
            ]
            payload = {
                "model": model_name,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "messages": anthropic_messages,
            }
            if request.context:
                payload["system"] = request.context
            endpoint = f"{base_url}/messages"
        else:  # pragma: no cover - safeguarded by provider check above
            raise HTTPException(status_code=400, detail=f"Unsupported AI provider: {provider.name}")

        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(endpoint, headers=headers, json=payload)
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"AI provider error: {response.text}",
                )
            return response.json()


ai_manager = AIProviderManager()


@router.post("/generate-content", response_model=AIResponse)
async def generate_content(
    request: AIRequest,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
) -> AIResponse:
    """Generate content using the configured AI provider (authenticated)."""
    provider = await ai_manager.get_active_provider(db)
    if not provider:
        raise HTTPException(status_code=400, detail="No active AI provider configured")

    response_payload = await ai_manager.make_ai_request(provider, request)
    content = _extract_ai_message(provider.name, response_payload)
    return AIResponse(
        content=content or "",
        provider=provider.name,
        model=request.model or response_payload.get("model"),
        usage=response_payload.get("usage"),
    )


@router.post("/public/chat", response_model=AIResponse)
async def public_chat(
    request: AIRequest,
    db: AsyncSession = Depends(get_db),
) -> AIResponse:
    """Public endpoint the marketing site can use for the AI assistant widget."""
    provider = await ai_manager.get_active_provider(db)
    if not provider or not provider.is_active:
        raise HTTPException(status_code=503, detail="AI assistant is not currently available")

    try:
        response_payload = await ai_manager.make_ai_request(provider, request)
    except HTTPException:
        raise
    except Exception as exc:  # pragma: no cover - defensive safety net
        raise HTTPException(status_code=500, detail="AI generation failed") from exc

    content = _extract_ai_message(provider.name, response_payload)
    if not content:
        content = "I'm sorry, I wasn't able to generate a response just now. Please try again."

    return AIResponse(
        content=content,
        provider=provider.name,
        model=request.model or response_payload.get("model"),
        usage=response_payload.get("usage"),
    )


@router.get("/providers")
async def list_providers(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """List all configured AI providers."""
    result = await db.execute(select(AIProvider))
    providers = result.scalars().all()

    return [
        {
            "id": provider.id,
            "name": provider.name,
            "display_name": provider.display_name,
            "is_active": provider.is_active,
            "is_default": provider.is_default,
            "has_api_key": bool(provider.api_key),
        }
        for provider in providers
    ]


@router.post("/providers", dependencies=[Depends(requires_roles("admin"))])
async def create_provider(
    config: AIProviderConfig,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """Create or update an AI provider configuration."""
    result = await db.execute(select(AIProvider).where(AIProvider.name == config.name))
    existing = result.scalar_one_or_none()

    default_base_url = ai_manager.providers.get(config.name, {}).get("base_url")

    if existing:
        if config.api_key:
            existing.api_key = encrypt_value(config.api_key)
        existing.base_url = config.base_url or existing.base_url or default_base_url
        existing.is_active = config.is_active
        existing.configuration = config.configuration
        provider_record = existing
    else:
        provider_record = AIProvider(
            name=config.name,
            display_name=config.display_name,
            api_key=encrypt_value(config.api_key) if config.api_key else None,
            base_url=config.base_url or default_base_url,
            is_active=config.is_active,
            configuration=config.configuration,
        )
        db.add(provider_record)

    if config.is_active:
        # Deactivate other providers so only one is active at a time
        other_providers = (await db.execute(select(AIProvider))).scalars().all()
        for provider in other_providers:
            if provider.id != provider_record.id:
                provider.is_active = False

    await db.commit()
    await db.refresh(provider_record)

    return {"message": "AI provider configured successfully", "provider_id": provider_record.id}
