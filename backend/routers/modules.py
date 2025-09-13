from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import json

from ..database import get_db, Module, User
from ..auth import get_current_user

router = APIRouter()

class ModuleCreate(BaseModel):
    name: str
    description: str
    version: str = "1.0.0"
    configuration: Dict[str, Any] = {}
    api_keys: Dict[str, str] = {}

class ModuleUpdate(BaseModel):
    description: Optional[str] = None
    is_active: Optional[bool] = None
    configuration: Optional[Dict[str, Any]] = None
    api_keys: Optional[Dict[str, str]] = None

class ModuleResponse(BaseModel):
    id: int
    name: str
    description: str
    version: str
    is_active: bool
    configuration: Dict[str, Any]
    has_api_keys: bool
    created_at: str
    updated_at: Optional[str] = None

class AvailableModule(BaseModel):
    name: str
    display_name: str
    description: str
    version: str
    category: str
    features: List[str]
    required_config: List[str]
    api_requirements: List[str]

# Available modules catalog
AVAILABLE_MODULES = [
    AvailableModule(
        name="google_analytics",
        display_name="Google Analytics",
        description="Track website traffic and user behavior",
        version="1.0.0",
        category="Analytics",
        features=["Traffic tracking", "User behavior analysis", "Conversion tracking"],
        required_config=["tracking_id"],
        api_requirements=["google_analytics_key"]
    ),
    AvailableModule(
        name="seo_optimizer",
        display_name="SEO Optimizer",
        description="AI-powered SEO analysis and optimization",
        version="1.0.0",
        category="SEO",
        features=["Keyword analysis", "Meta tag optimization", "Content scoring"],
        required_config=["target_keywords"],
        api_requirements=["seo_api_key"]
    ),
    AvailableModule(
        name="social_media",
        display_name="Social Media Integration",
        description="Auto-post content to social media platforms",
        version="1.0.0",
        category="Marketing",
        features=["Auto-posting", "Social analytics", "Content scheduling"],
        required_config=["platforms"],
        api_requirements=["twitter_api_key", "facebook_api_key"]
    ),
    AvailableModule(
        name="email_marketing",
        display_name="Email Marketing",
        description="Newsletter and email campaign management",
        version="1.0.0",
        category="Marketing",
        features=["Newsletter creation", "Subscriber management", "Campaign analytics"],
        required_config=["sender_email"],
        api_requirements=["mailchimp_api_key"]
    ),
    AvailableModule(
        name="backup_manager",
        display_name="Backup Manager",
        description="Automated content and database backups",
        version="1.0.0",
        category="Utilities",
        features=["Scheduled backups", "Cloud storage", "Restore functionality"],
        required_config=["backup_frequency"],
        api_requirements=["cloud_storage_key"]
    )
]

@router.get("/available", response_model=List[AvailableModule])
async def list_available_modules(
    category: Optional[str] = None,
    current_user: User = Depends(get_current_user)
):
    """List all available modules for installation"""
    
    modules = AVAILABLE_MODULES
    
    if category:
        modules = [m for m in modules if m.category.lower() == category.lower()]
    
    return modules

@router.get("/installed", response_model=List[ModuleResponse])
async def list_installed_modules(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all installed modules"""
    
    result = await db.execute(select(Module))
    modules = result.scalars().all()
    
    return [
        ModuleResponse(
            id=module.id,
            name=module.name,
            description=module.description,
            version=module.version,
            is_active=module.is_active,
            configuration=module.configuration,
            has_api_keys=bool(module.api_keys),
            created_at=module.created_at.isoformat(),
            updated_at=module.updated_at.isoformat() if module.updated_at else None
        )
        for module in modules
    ]

@router.post("/install/{module_name}")
async def install_module(
    module_name: str,
    module_data: ModuleCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Install a new module"""
    
    # Check if module is available
    available_module = next((m for m in AVAILABLE_MODULES if m.name == module_name), None)
    if not available_module:
        raise HTTPException(status_code=404, detail="Module not available")
    
    # Check if already installed
    result = await db.execute(select(Module).where(Module.name == module_name))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Module already installed")
    
    # Create module
    db_module = Module(
        name=module_name,
        description=module_data.description or available_module.description,
        version=module_data.version,
        configuration=module_data.configuration,
        api_keys=module_data.api_keys,
        is_active=False  # Start inactive until configured
    )
    
    db.add(db_module)
    await db.commit()
    await db.refresh(db_module)
    
    return {"message": f"Module {module_name} installed successfully", "module_id": db_module.id}

@router.put("/{module_id}")
async def update_module(
    module_id: int,
    module_update: ModuleUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update module configuration"""
    
    result = await db.execute(select(Module).where(Module.id == module_id))
    module = result.scalar_one_or_none()
    
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    
    # Update fields
    update_data = module_update.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(module, field, value)
    
    await db.commit()
    await db.refresh(module)
    
    return {"message": "Module updated successfully"}

@router.post("/{module_id}/activate")
async def activate_module(
    module_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Activate a module"""
    
    result = await db.execute(select(Module).where(Module.id == module_id))
    module = result.scalar_one_or_none()
    
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    
    module.is_active = True
    await db.commit()
    
    return {"message": f"Module {module.name} activated successfully"}

@router.post("/{module_id}/deactivate")
async def deactivate_module(
    module_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Deactivate a module"""
    
    result = await db.execute(select(Module).where(Module.id == module_id))
    module = result.scalar_one_or_none()
    
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    
    module.is_active = False
    await db.commit()
    
    return {"message": f"Module {module.name} deactivated successfully"}

@router.delete("/{module_id}")
async def uninstall_module(
    module_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Uninstall a module"""
    
    result = await db.execute(select(Module).where(Module.id == module_id))
    module = result.scalar_one_or_none()
    
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    
    await db.delete(module)
    await db.commit()
    
    return {"message": f"Module {module.name} uninstalled successfully"}
