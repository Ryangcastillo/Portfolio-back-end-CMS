"""
Admin Portfolio Management API

These endpoints require authentication and are used by the CMS admin interface
to manage portfolio content (CRUD operations).
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from auth import get_current_user  # Your existing auth function
from models.portfolio_models import (
    ProfileInfo, ProfileStats, Skill, Project, ProjectCategory, 
    Experience, Testimonial
)
from pydantic import BaseModel
from datetime import datetime


# Pydantic models for request/response
class ProfileInfoCreate(BaseModel):
    full_name: str
    title: str
    subtitle: Optional[str] = None
    bio_description: str
    years_experience: int
    availability_status: str = "Available for New Opportunities"
    resume_url: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    portfolio_url: Optional[str] = None


class ProfileStatsCreate(BaseModel):
    metric_name: str
    metric_value: str
    metric_description: Optional[str] = None
    display_order: int = 0


class SkillCreate(BaseModel):
    title: str
    description: str
    icon_name: Optional[str] = None
    color_gradient: Optional[str] = None
    projects_count: Optional[str] = None
    impact_metric: Optional[str] = None
    category: Optional[str] = None
    skill_level: Optional[str] = None
    display_order: int = 0
    is_featured: bool = False


class ProjectCategoryCreate(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None
    icon_name: Optional[str] = None
    color_theme: Optional[str] = None
    display_order: int = 0


class ProjectCreate(BaseModel):
    title: str
    short_description: str
    full_description: Optional[str] = None
    impact_metric: Optional[str] = None
    business_problem: Optional[str] = None
    solution_approach: Optional[str] = None
    results_achieved: Optional[str] = None
    technologies: Optional[List[str]] = None
    methodology: Optional[str] = None
    challenges_overcome: Optional[str] = None
    thumbnail_url: Optional[str] = None
    image_gallery: Optional[List[str]] = None
    demo_url: Optional[str] = None
    github_url: Optional[str] = None
    case_study_url: Optional[str] = None
    category_id: Optional[int] = None
    is_featured: bool = False
    display_order: int = 0
    is_published: bool = True
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    project_duration: Optional[str] = None


class ExperienceCreate(BaseModel):
    company_name: str
    position_title: str
    company_description: Optional[str] = None
    start_date: datetime
    end_date: Optional[datetime] = None
    is_current: bool = False
    location: Optional[str] = None
    work_type: Optional[str] = None
    key_responsibilities: Optional[List[str]] = None
    key_achievements: Optional[List[str]] = None
    technologies_used: Optional[List[str]] = None
    display_order: int = 0
    is_featured: bool = True


class TestimonialCreate(BaseModel):
    author_name: str
    author_title: Optional[str] = None
    author_company: Optional[str] = None
    author_avatar_url: Optional[str] = None
    testimonial_text: str
    rating: Optional[int] = None
    project_context: Optional[str] = None
    collaboration_type: Optional[str] = None
    is_featured: bool = False
    display_order: int = 0
    is_approved: bool = True


# Initialize router with auth required
router = APIRouter(prefix="/api/admin/portfolio", tags=["admin-portfolio"])


# Profile Info Management
@router.post("/profile")
async def create_or_update_profile(
    profile_data: ProfileInfoCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Create or update profile information (only one profile should exist)"""
    
    # Check if profile already exists
    existing_profile = db.query(ProfileInfo).filter(ProfileInfo.is_active == True).first()
    
    if existing_profile:
        # Update existing
        for field, value in profile_data.dict().items():
            setattr(existing_profile, field, value)
        existing_profile.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(existing_profile)
        return existing_profile
    else:
        # Create new
        new_profile = ProfileInfo(**profile_data.dict())
        db.add(new_profile)
        db.commit()
        db.refresh(new_profile)
        return new_profile


@router.get("/profile")
async def get_admin_profile(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get profile for admin editing"""
    profile = db.query(ProfileInfo).filter(ProfileInfo.is_active == True).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile


# Profile Stats Management
@router.post("/stats")
async def create_profile_stat(
    stat_data: ProfileStatsCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Create new profile statistic"""
    new_stat = ProfileStats(**stat_data.dict())
    db.add(new_stat)
    db.commit()
    db.refresh(new_stat)
    return new_stat


@router.get("/stats")
async def get_admin_stats(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get all stats for admin management"""
    return db.query(ProfileStats).order_by(ProfileStats.display_order).all()


@router.put("/stats/{stat_id}")
async def update_profile_stat(
    stat_id: int,
    stat_data: ProfileStatsCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Update profile statistic"""
    stat = db.query(ProfileStats).filter(ProfileStats.id == stat_id).first()
    if not stat:
        raise HTTPException(status_code=404, detail="Statistic not found")
    
    for field, value in stat_data.dict().items():
        setattr(stat, field, value)
    stat.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(stat)
    return stat


@router.delete("/stats/{stat_id}")
async def delete_profile_stat(
    stat_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Delete profile statistic"""
    stat = db.query(ProfileStats).filter(ProfileStats.id == stat_id).first()
    if not stat:
        raise HTTPException(status_code=404, detail="Statistic not found")
    
    db.delete(stat)
    db.commit()
    return {"message": "Statistic deleted successfully"}


# Skills Management
@router.post("/skills")
async def create_skill(
    skill_data: SkillCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Create new skill"""
    new_skill = Skill(**skill_data.dict())
    db.add(new_skill)
    db.commit()
    db.refresh(new_skill)
    return new_skill


@router.get("/skills")
async def get_admin_skills(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get all skills for admin management"""
    return db.query(Skill).order_by(Skill.display_order).all()


@router.put("/skills/{skill_id}")
async def update_skill(
    skill_id: int,
    skill_data: SkillCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Update skill"""
    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    
    for field, value in skill_data.dict().items():
        setattr(skill, field, value)
    skill.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(skill)
    return skill


@router.delete("/skills/{skill_id}")
async def delete_skill(
    skill_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Delete skill"""
    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    
    db.delete(skill)
    db.commit()
    return {"message": "Skill deleted successfully"}


# Project Categories Management
@router.post("/categories")
async def create_project_category(
    category_data: ProjectCategoryCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Create new project category"""
    new_category = ProjectCategory(**category_data.dict())
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category


@router.get("/categories")
async def get_admin_categories(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get all categories for admin management"""
    return db.query(ProjectCategory).order_by(ProjectCategory.display_order).all()


# Projects Management
@router.post("/projects")
async def create_project(
    project_data: ProjectCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Create new project"""
    new_project = Project(**project_data.dict())
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project


@router.get("/projects")
async def get_admin_projects(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get all projects for admin management"""
    return db.query(Project).order_by(Project.display_order).all()


@router.put("/projects/{project_id}")
async def update_project(
    project_id: int,
    project_data: ProjectCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Update project"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    for field, value in project_data.dict().items():
        setattr(project, field, value)
    project.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(project)
    return project


@router.delete("/projects/{project_id}")
async def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Delete project"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    db.delete(project)
    db.commit()
    return {"message": "Project deleted successfully"}


# Experience Management  
@router.post("/experience")
async def create_experience(
    experience_data: ExperienceCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Create new work experience"""
    new_experience = Experience(**experience_data.dict())
    db.add(new_experience)
    db.commit()
    db.refresh(new_experience)
    return new_experience


@router.get("/experience")
async def get_admin_experience(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get all experience for admin management"""
    return db.query(Experience).order_by(Experience.start_date.desc()).all()


# Testimonials Management
@router.post("/testimonials")
async def create_testimonial(
    testimonial_data: TestimonialCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Create new testimonial"""
    new_testimonial = Testimonial(**testimonial_data.dict())
    db.add(new_testimonial)
    db.commit()
    db.refresh(new_testimonial)
    return new_testimonial


@router.get("/testimonials")
async def get_admin_testimonials(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get all testimonials for admin management"""
    return db.query(Testimonial).order_by(Testimonial.display_order).all()