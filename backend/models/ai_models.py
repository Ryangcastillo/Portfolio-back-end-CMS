from pydantic import BaseModel
from typing import Optional, Dict, Any

class AIRequest(BaseModel):
    prompt: str
    model: Optional[str] = None
    max_tokens: Optional[int] = 1000
    temperature: Optional[float] = 0.7
    context: Optional[str] = None

class AIResponse(BaseModel):
    content: str
    provider: str
    model: Optional[str] = None
    usage: Optional[Dict[str, Any]] = None

class AIProviderConfig(BaseModel):
    name: str
    display_name: str
    api_key: str
    base_url: Optional[str] = None
    is_active: bool = False
    configuration: Optional[Dict[str, Any]] = {}
