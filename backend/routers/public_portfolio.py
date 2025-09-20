"""
Public Portfolio API Endpoints

These endpoints serve content to the public-facing website.
No authentication required - these are public endpoints.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
from models.portfolio_models import (
    ProfileInfo, ProfileStats, Skill, Project, ProjectCategory, 
    Experience, Testimonial, BlogPost
)
from pydantic import BaseModel
from datetime import datetime


# Pydantic models for API responses
class ProfileInfoResponse(BaseModel):
    id: int
    full_name: str
    title: str
    subtitle: Optional[str]
    bio_description: str
    years_experience: int
    availability_status: str
    resume_url: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    location: Optional[str]
    linkedin_url: Optional[str]
    github_url: Optional[str]
    portfolio_url: Optional[str]
    
    class Config:
        from_attributes = True


class ProfileStatsResponse(BaseModel):
    id: int
    metric_name: str
    metric_value: str
    metric_description: Optional[str]
    display_order: int
    
    class Config:
        from_attributes = True


class SkillResponse(BaseModel):
    id: int
    title: str
    description: str
    icon_name: Optional[str]
    color_gradient: Optional[str]
    projects_count: Optional[str]
    impact_metric: Optional[str]
    category: Optional[str]
    skill_level: Optional[str]
    display_order: int
    is_featured: bool
    
    class Config:
        from_attributes = True


class ProjectCategoryResponse(BaseModel):
    id: int
    name: str
    slug: str
    description: Optional[str]
    icon_name: Optional[str]
    color_theme: Optional[str]
    display_order: int
    
    class Config:
        from_attributes = True


class ProjectResponse(BaseModel):
    id: int
    title: str
    short_description: str
    full_description: Optional[str]
    impact_metric: Optional[str]
    business_problem: Optional[str]
    solution_approach: Optional[str]
    results_achieved: Optional[str]
    technologies: Optional[List[str]]
    methodology: Optional[str]
    challenges_overcome: Optional[str]
    thumbnail_url: Optional[str]
    image_gallery: Optional[List[str]]
    demo_url: Optional[str]
    github_url: Optional[str]
    case_study_url: Optional[str]
    category: Optional[ProjectCategoryResponse]
    is_featured: bool
    display_order: int
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    project_duration: Optional[str]
    
    class Config:
        from_attributes = True


class ExperienceResponse(BaseModel):
    id: int
    company_name: str
    position_title: str
    company_description: Optional[str]
    start_date: datetime
    end_date: Optional[datetime]
    is_current: bool
    location: Optional[str]
    work_type: Optional[str]
    key_responsibilities: Optional[List[str]]
    key_achievements: Optional[List[str]]
    technologies_used: Optional[List[str]]
    display_order: int
    
    class Config:
        from_attributes = True


class TestimonialResponse(BaseModel):
    id: int
    author_name: str
    author_title: Optional[str]
    author_company: Optional[str]
    author_avatar_url: Optional[str]
    testimonial_text: str
    rating: Optional[int]
    project_context: Optional[str]
    collaboration_type: Optional[str]
    display_order: int
    
    class Config:
        from_attributes = True


# Initialize router
router = APIRouter(prefix="/api/public", tags=["public-portfolio"])


@router.get("/profile", response_model=ProfileInfoResponse)
async def get_profile_info(db: Session = Depends(get_db)):
    """Get main profile information"""
    profile = db.query(ProfileInfo).filter(ProfileInfo.is_active == True).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile


@router.get("/stats", response_model=List[ProfileStatsResponse])
async def get_profile_stats(db: Session = Depends(get_db)):
    """Get profile statistics for homepage"""
    stats = db.query(ProfileStats).filter(
        ProfileStats.is_active == True
    ).order_by(ProfileStats.display_order).all()
    return stats


@router.get("/skills", response_model=List[SkillResponse])
async def get_skills(
    featured_only: bool = Query(False, description="Get only featured skills"),
    category: Optional[str] = Query(None, description="Filter by skill category"),
    db: Session = Depends(get_db)
):
    """Get skills and expertise areas"""
    query = db.query(Skill).filter(Skill.is_active == True)
    
    if featured_only:
        query = query.filter(Skill.is_featured == True)
    
    if category:
        query = query.filter(Skill.category == category)
    
    skills = query.order_by(Skill.display_order).all()
    return skills


@router.get("/projects", response_model=List[ProjectResponse])
async def get_projects(
    featured_only: bool = Query(False, description="Get only featured projects"),
    category: Optional[str] = Query(None, description="Filter by category slug"),
    limit: Optional[int] = Query(None, description="Limit number of results"),
    db: Session = Depends(get_db)
):
    """Get projects and case studies"""
    query = db.query(Project).filter(Project.is_published == True)
    
    if featured_only:
        query = query.filter(Project.is_featured == True)
    
    if category:
        query = query.join(ProjectCategory).filter(ProjectCategory.slug == category)
    
    query = query.order_by(Project.display_order, Project.created_at.desc())
    
    if limit:
        query = query.limit(limit)
    
    projects = query.all()
    return projects


@router.get("/projects/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: int, db: Session = Depends(get_db)):
    """Get single project details"""
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.is_published == True
    ).first()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    return project


@router.get("/project-categories", response_model=List[ProjectCategoryResponse])
async def get_project_categories(db: Session = Depends(get_db)):
    """Get all project categories"""
    categories = db.query(ProjectCategory).filter(
        ProjectCategory.is_active == True
    ).order_by(ProjectCategory.display_order).all()
    return categories


@router.get("/experience", response_model=List[ExperienceResponse])
async def get_experience(
    featured_only: bool = Query(False, description="Get only featured experience"),
    db: Session = Depends(get_db)
):
    """Get work experience"""
    query = db.query(Experience)
    
    if featured_only:
        query = query.filter(Experience.is_featured == True)
    
    experience = query.order_by(Experience.start_date.desc()).all()
    return experience


@router.get("/testimonials", response_model=List[TestimonialResponse])
async def get_testimonials(
    featured_only: bool = Query(False, description="Get only featured testimonials"),
    limit: Optional[int] = Query(None, description="Limit number of results"),
    db: Session = Depends(get_db)
):
    """Get testimonials and recommendations"""
    query = db.query(Testimonial).filter(Testimonial.is_approved == True)
    
    if featured_only:
        query = query.filter(Testimonial.is_featured == True)
    
    query = query.order_by(Testimonial.display_order)
    
    if limit:
        query = query.limit(limit)
    
    testimonials = query.all()
    return testimonials


# Convenience endpoints for specific page content
@router.get("/homepage-data")
async def get_homepage_data(db: Session = Depends(get_db)):
    """Get all data needed for homepage in single request"""
    
    # Get profile info
    profile = db.query(ProfileInfo).filter(ProfileInfo.is_active == True).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    # Get stats
    stats = db.query(ProfileStats).filter(
        ProfileStats.is_active == True
    ).order_by(ProfileStats.display_order).all()
    
    # Get featured skills
    featured_skills = db.query(Skill).filter(
        Skill.is_active == True,
        Skill.is_featured == True
    ).order_by(Skill.display_order).all()
    
    # Get featured projects
    featured_projects = db.query(Project).filter(
        Project.is_published == True,
        Project.is_featured == True
    ).order_by(Project.display_order).limit(3).all()
    
    return {
        "profile": ProfileInfoResponse.from_orm(profile),
        "stats": [ProfileStatsResponse.from_orm(stat) for stat in stats],
        "featured_skills": [SkillResponse.from_orm(skill) for skill in featured_skills],
        "featured_projects": [ProjectResponse.from_orm(project) for project in featured_projects]
    }


@router.get("/portfolio-overview")
async def get_portfolio_overview(db: Session = Depends(get_db)):
    """Get overview data for portfolio pages"""
    
    # Get categories with project counts
    categories = db.query(ProjectCategory).filter(
        ProjectCategory.is_active == True
    ).order_by(ProjectCategory.display_order).all()
    
    category_data = []
    for category in categories:
        project_count = db.query(Project).filter(
            Project.category_id == category.id,
            Project.is_published == True
        ).count()
        
        category_info = ProjectCategoryResponse.from_orm(category)
        category_data.append({
            **category_info.dict(),
            "project_count": project_count
        })
    
    # Get recent projects
    recent_projects = db.query(Project).filter(
        Project.is_published == True
    ).order_by(Project.created_at.desc()).limit(6).all()
    
    return {
        "categories": category_data,
        "recent_projects": [ProjectResponse.from_orm(project) for project in recent_projects]
    }