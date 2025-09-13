from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from pydantic import BaseModel
from typing import List, Dict, Any
from datetime import datetime, timedelta

from ..database import get_db, Content, User, Module
from ..auth import get_current_user

router = APIRouter()

class DashboardStats(BaseModel):
    total_content: int
    published_content: int
    draft_content: int
    total_users: int
    active_modules: int
    recent_activity: List[Dict[str, Any]]

class QuickAction(BaseModel):
    id: str
    title: str
    description: str
    icon: str
    url: str

@router.get("/stats", response_model=DashboardStats)
async def get_dashboard_stats(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get dashboard statistics and metrics"""
    
    # Content statistics
    total_content_result = await db.execute(select(func.count(Content.id)))
    total_content = total_content_result.scalar()
    
    published_content_result = await db.execute(
        select(func.count(Content.id)).where(Content.status == "published")
    )
    published_content = published_content_result.scalar()
    
    draft_content_result = await db.execute(
        select(func.count(Content.id)).where(Content.status == "draft")
    )
    draft_content = draft_content_result.scalar()
    
    # User statistics
    total_users_result = await db.execute(select(func.count(User.id)))
    total_users = total_users_result.scalar()
    
    # Module statistics
    active_modules_result = await db.execute(
        select(func.count(Module.id)).where(Module.is_active == True)
    )
    active_modules = active_modules_result.scalar()
    
    # Recent activity (last 10 content items)
    recent_content_result = await db.execute(
        select(Content).order_by(desc(Content.updated_at)).limit(10)
    )
    recent_content = recent_content_result.scalars().all()
    
    recent_activity = [
        {
            "id": content.id,
            "title": content.title,
            "type": "content",
            "action": "updated" if content.updated_at > content.created_at else "created",
            "timestamp": content.updated_at or content.created_at,
            "status": content.status
        }
        for content in recent_content
    ]
    
    return DashboardStats(
        total_content=total_content,
        published_content=published_content,
        draft_content=draft_content,
        total_users=total_users,
        active_modules=active_modules,
        recent_activity=recent_activity
    )

@router.get("/quick-actions")
async def get_quick_actions(
    current_user: User = Depends(get_current_user)
) -> List[QuickAction]:
    """Get available quick actions for the dashboard"""
    
    actions = [
        QuickAction(
            id="create_article",
            title="Create Article",
            description="Write a new article with AI assistance",
            icon="article",
            url="/content/create?type=article"
        ),
        QuickAction(
            id="create_page",
            title="Create Page",
            description="Build a new page for your site",
            icon="page",
            url="/content/create?type=page"
        ),
        QuickAction(
            id="manage_modules",
            title="Manage Modules",
            description="Install or configure modules",
            icon="modules",
            url="/modules"
        ),
        QuickAction(
            id="seo_analysis",
            title="SEO Analysis",
            description="Analyze and improve your site's SEO",
            icon="seo",
            url="/seo/analyze"
        )
    ]
    
    return actions

@router.get("/analytics")
async def get_analytics_overview(
    days: int = 30,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get analytics overview for the specified period"""
    
    # Calculate date range
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    # Content creation over time
    content_by_day = await db.execute(
        select(
            func.date(Content.created_at).label('date'),
            func.count(Content.id).label('count')
        )
        .where(Content.created_at >= start_date)
        .group_by(func.date(Content.created_at))
        .order_by(func.date(Content.created_at))
    )
    
    content_timeline = [
        {"date": str(row.date), "count": row.count}
        for row in content_by_day
    ]
    
    # Content by type
    content_by_type = await db.execute(
        select(
            Content.content_type,
            func.count(Content.id).label('count')
        )
        .group_by(Content.content_type)
    )
    
    content_types = [
        {"type": row.content_type, "count": row.count}
        for row in content_by_type
    ]
    
    return {
        "period_days": days,
        "content_timeline": content_timeline,
        "content_by_type": content_types,
        "summary": {
            "total_content_created": sum(item["count"] for item in content_timeline),
            "most_popular_type": max(content_types, key=lambda x: x["count"])["type"] if content_types else None
        }
    }
