from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, desc
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import re

from ..database import get_db, Content, User
from ..auth import get_current_user

router = APIRouter()

class ContentCreate(BaseModel):
    title: str
    content_type: str
    body: Optional[str] = None
    excerpt: Optional[str] = None
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None
    meta_keywords: Optional[str] = None
    status: str = "draft"

class ContentUpdate(BaseModel):
    title: Optional[str] = None
    body: Optional[str] = None
    excerpt: Optional[str] = None
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None
    meta_keywords: Optional[str] = None
    status: Optional[str] = None

class ContentResponse(BaseModel):
    id: int
    title: str
    slug: str
    content_type: str
    body: Optional[str] = None
    excerpt: Optional[str] = None
    status: str
    author_id: int
    meta_title: Optional[str] = None
    meta_description: Optional[str] = None
    meta_keywords: Optional[str] = None
    ai_generated: bool
    ai_suggestions: dict
    created_at: datetime
    updated_at: Optional[datetime] = None
    published_at: Optional[datetime] = None

def generate_slug(title: str) -> str:
    """Generate URL-friendly slug from title"""
    slug = re.sub(r'[^\w\s-]', '', title.lower())
    slug = re.sub(r'[-\s]+', '-', slug)
    return slug.strip('-')

@router.post("/", response_model=ContentResponse)
async def create_content(
    content: ContentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create new content"""
    
    # Generate slug
    base_slug = generate_slug(content.title)
    slug = base_slug
    counter = 1
    
    # Ensure unique slug
    while True:
        existing = await db.execute(select(Content).where(Content.slug == slug))
        if not existing.scalar_one_or_none():
            break
        slug = f"{base_slug}-{counter}"
        counter += 1
    
    # Create content
    db_content = Content(
        title=content.title,
        slug=slug,
        content_type=content.content_type,
        body=content.body,
        excerpt=content.excerpt,
        status=content.status,
        author_id=current_user.id,
        meta_title=content.meta_title,
        meta_description=content.meta_description,
        meta_keywords=content.meta_keywords
    )
    
    # Set published_at if status is published
    if content.status == "published":
        db_content.published_at = datetime.utcnow()
    
    db.add(db_content)
    await db.commit()
    await db.refresh(db_content)
    
    return db_content

@router.get("/", response_model=List[ContentResponse])
async def list_content(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    content_type: Optional[str] = None,
    status: Optional[str] = None,
    search: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List content with filtering and pagination"""
    
    query = select(Content)
    
    # Apply filters
    if content_type:
        query = query.where(Content.content_type == content_type)
    
    if status:
        query = query.where(Content.status == status)
    
    if search:
        search_term = f"%{search}%"
        query = query.where(
            or_(
                Content.title.ilike(search_term),
                Content.body.ilike(search_term),
                Content.excerpt.ilike(search_term)
            )
        )
    
    # Order by updated_at descending
    query = query.order_by(desc(Content.updated_at)).offset(skip).limit(limit)
    
    result = await db.execute(query)
    content_list = result.scalars().all()
    
    return content_list

@router.get("/{content_id}", response_model=ContentResponse)
async def get_content(
    content_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get specific content by ID"""
    
    result = await db.execute(select(Content).where(Content.id == content_id))
    content = result.scalar_one_or_none()
    
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    
    return content

@router.put("/{content_id}", response_model=ContentResponse)
async def update_content(
    content_id: int,
    content_update: ContentUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update existing content"""
    
    result = await db.execute(select(Content).where(Content.id == content_id))
    content = result.scalar_one_or_none()
    
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    
    # Update fields
    update_data = content_update.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(content, field, value)
    
    # Update slug if title changed
    if content_update.title:
        new_slug = generate_slug(content_update.title)
        if new_slug != content.slug:
            # Ensure unique slug
            base_slug = new_slug
            counter = 1
            while True:
                existing = await db.execute(
                    select(Content).where(
                        Content.slug == new_slug,
                        Content.id != content_id
                    )
                )
                if not existing.scalar_one_or_none():
                    break
                new_slug = f"{base_slug}-{counter}"
                counter += 1
            content.slug = new_slug
    
    # Set published_at if status changed to published
    if content_update.status == "published" and content.status != "published":
        content.published_at = datetime.utcnow()
    
    content.updated_at = datetime.utcnow()
    
    await db.commit()
    await db.refresh(content)
    
    return content

@router.delete("/{content_id}")
async def delete_content(
    content_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete content"""
    
    result = await db.execute(select(Content).where(Content.id == content_id))
    content = result.scalar_one_or_none()
    
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    
    await db.delete(content)
    await db.commit()
    
    return {"message": "Content deleted successfully"}

@router.post("/{content_id}/ai-suggestions")
async def generate_ai_suggestions(
    content_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Generate AI suggestions for content improvement"""
    
    result = await db.execute(select(Content).where(Content.id == content_id))
    content = result.scalar_one_or_none()
    
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    
    # This would integrate with the AI service
    # For now, return mock suggestions
    suggestions = {
        "seo": {
            "title_suggestions": [
                f"Optimized: {content.title}",
                f"SEO-Friendly: {content.title}"
            ],
            "meta_description": f"Auto-generated meta description for {content.title}",
            "keywords": ["keyword1", "keyword2", "keyword3"]
        },
        "content": {
            "improvements": [
                "Consider adding more subheadings for better readability",
                "Include relevant images to break up text",
                "Add internal links to related content"
            ]
        }
    }
    
    # Save suggestions to content
    content.ai_suggestions = suggestions
    await db.commit()
    
    return suggestions
