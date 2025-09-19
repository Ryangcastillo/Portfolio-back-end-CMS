from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from typing import Dict, Any, Optional, List

from ..database import get_db, SiteSettings, User
from ..auth import get_current_user
from ..security import requires_roles, mask_secrets

router = APIRouter()

class SettingCreate(BaseModel):
    key: str
    value: Any
    description: Optional[str] = None

class SettingUpdate(BaseModel):
    value: Any
    description: Optional[str] = None

class SettingResponse(BaseModel):
    id: int
    key: str
    value: Any
    description: Optional[str] = None
    updated_at: Optional[str] = None

class SiteConfig(BaseModel):
    site_title: str = "My CMS Site"
    site_description: str = "A powerful CMS built with Stitch"
    site_logo: Optional[str] = None
    site_favicon: Optional[str] = None
    footer_text: str = "© 2024 My CMS Site. All rights reserved."
    contact_email: str = "admin@example.com"
    social_links: Dict[str, str] = {}
    theme_settings: Dict[str, Any] = {
        "primary_color": "#3b82f6",
        "secondary_color": "#64748b",
        "font_family": "Inter",
        "dark_mode_enabled": True
    }

@router.get("/", response_model=List[SettingResponse])
async def list_settings(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all site settings"""
    
    result = await db.execute(select(SiteSettings))
    settings = result.scalars().all()
    
    return [
        SettingResponse(
            id=setting.id,
            key=setting.key,
            value=mask_secrets(setting.value, setting.key),
            description=setting.description,
            updated_at=setting.updated_at.isoformat() if setting.updated_at else None,
        )
        for setting in settings
    ]

@router.get("/{setting_key}")
async def get_setting(
    setting_key: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific setting by key"""
    
    result = await db.execute(select(SiteSettings).where(SiteSettings.key == setting_key))
    setting = result.scalar_one_or_none()
    
    if not setting:
        raise HTTPException(status_code=404, detail="Setting not found")
    
    return SettingResponse(
        id=setting.id,
        key=setting.key,
        value=mask_secrets(setting.value, setting.key),
        description=setting.description,
        updated_at=setting.updated_at.isoformat() if setting.updated_at else None,
    )

@router.post("/", response_model=SettingResponse, dependencies=[Depends(requires_roles("admin"))])
async def create_setting(
    setting: SettingCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new setting"""
    
    # Check if setting already exists
    result = await db.execute(select(SiteSettings).where(SiteSettings.key == setting.key))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Setting already exists")
    
    db_setting = SiteSettings(
        key=setting.key,
        value=setting.value,
        description=setting.description
    )
    
    db.add(db_setting)
    await db.commit()
    await db.refresh(db_setting)
    
    return SettingResponse(
        id=db_setting.id,
        key=db_setting.key,
        value=mask_secrets(db_setting.value, db_setting.key),
        description=db_setting.description,
        updated_at=db_setting.updated_at.isoformat() if db_setting.updated_at else None,
    )

@router.put("/{setting_key}", dependencies=[Depends(requires_roles("admin"))])
async def update_setting(
    setting_key: str,
    setting_update: SettingUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update an existing setting"""
    
    result = await db.execute(select(SiteSettings).where(SiteSettings.key == setting_key))
    setting = result.scalar_one_or_none()
    
    if not setting:
        raise HTTPException(status_code=404, detail="Setting not found")
    
    setting.value = setting_update.value
    if setting_update.description is not None:
        setting.description = setting_update.description
    
    await db.commit()
    await db.refresh(setting)
    
    return SettingResponse(
        id=setting.id,
        key=setting.key,
        value=mask_secrets(setting.value, setting.key),
        description=setting.description,
        updated_at=setting.updated_at.isoformat() if setting.updated_at else None,
    )

@router.delete("/{setting_key}", dependencies=[Depends(requires_roles("admin"))])
async def delete_setting(
    setting_key: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a setting"""
    
    result = await db.execute(select(SiteSettings).where(SiteSettings.key == setting_key))
    setting = result.scalar_one_or_none()
    
    if not setting:
        raise HTTPException(status_code=404, detail="Setting not found")
    
    await db.delete(setting)
    await db.commit()
    
    return {"message": "Setting deleted successfully"}

@router.get("/config/site", response_model=SiteConfig)
async def get_site_config(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get complete site configuration"""
    
    result = await db.execute(select(SiteSettings))
    settings = result.scalars().all()
    
    # Convert settings to config object
    config_dict = {setting.key: setting.value for setting in settings}
    
    # Merge with defaults
    default_config = SiteConfig()
    for key, value in config_dict.items():
        if hasattr(default_config, key):
            setattr(default_config, key, value)
    
    return default_config

@router.post("/config/site", dependencies=[Depends(requires_roles("admin"))])
async def update_site_config(
    config: SiteConfig,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update complete site configuration"""
    
    config_dict = config.dict()
    
    for key, value in config_dict.items():
        # Check if setting exists
        result = await db.execute(select(SiteSettings).where(SiteSettings.key == key))
        setting = result.scalar_one_or_none()
        
        if setting:
            setting.value = value
        else:
            # Create new setting
            new_setting = SiteSettings(
                key=key,
                value=value,
                description=f"Site configuration: {key}"
            )
            db.add(new_setting)
    
    await db.commit()
    
    return {"message": "Site configuration updated successfully"}

@router.post("/initialize-defaults", dependencies=[Depends(requires_roles("admin"))])
async def initialize_default_settings(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Initialize default site settings"""
    
    default_config = SiteConfig()
    config_dict = default_config.dict()
    
    for key, value in config_dict.items():
        # Check if setting already exists
        result = await db.execute(select(SiteSettings).where(SiteSettings.key == key))
        if not result.scalar_one_or_none():
            new_setting = SiteSettings(
                key=key,
                value=value,
                description=f"Default site configuration: {key}"
            )
            db.add(new_setting)
    
    await db.commit()
    
    return {"message": "Default settings initialized successfully"}
