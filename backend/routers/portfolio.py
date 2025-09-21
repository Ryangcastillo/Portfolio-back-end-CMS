from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from pydantic import BaseModel
from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..database import get_session
from ..models.portfolio_models import (
    PortfolioSummary as PortfolioSummaryModel,
    Project as ProjectModel,
    Skill as SkillModel,
    Experience as ExperienceModel,
    Education as EducationModel,
    Certification as CertificationModel,
    Testimonial as TestimonialModel,
)

router = APIRouter(prefix="/api/v1/portfolio", tags=["portfolio"])

# Pydantic models for portfolio data
class ProjectSchema(BaseModel):
    id: Optional[int] = None
    title: str
    description: str
    technologies: List[str]
    github_url: Optional[str] = None
    demo_url: Optional[str] = None
    image_url: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    featured: bool = False

class SkillSchema(BaseModel):
    id: Optional[int] = None
    name: str
    category: str  # e.g., "Frontend", "Backend", "Database", "DevOps"
    level: int  # 1-5 proficiency level
    years_of_experience: Optional[int] = None

class ExperienceSchema(BaseModel):
    id: Optional[int] = None
    company: str
    position: str
    description: str
    start_date: date
    end_date: Optional[date] = None
    location: Optional[str] = None
    is_current: bool = False

class PortfolioSummarySchema(BaseModel):
    name: str
    title: str
    bio: str
    email: str
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    website_url: Optional[str] = None
    resume_url: Optional[str] = None

# Portfolio endpoints
@router.get("/summary", response_model=PortfolioSummarySchema)
async def get_portfolio_summary(session: AsyncSession = Depends(get_session)):
    """Get portfolio summary information"""
    try:
        # Try to get from database first
        result = await session.execute(select(PortfolioSummaryModel).where(PortfolioSummaryModel.is_active == True))
        summary = result.scalar_one_or_none()
        
        if summary:
            return PortfolioSummarySchema(
                name=summary.name,
                title=summary.title,
                bio=summary.bio,
                email=summary.email,
                linkedin_url=summary.linkedin_url,
                github_url=summary.github_url,
                website_url=summary.website_url,
                resume_url=summary.resume_url
            )
    except Exception as e:
        # Log the error but continue with fallback data
        print(f"Database error: {e}")
    
    # Fallback to static data if no database record or error
    return PortfolioSummarySchema(
        name="Your Name",
        title="Full Stack Developer",
        bio="Passionate developer with expertise in building modern web applications using React, Next.js, Python, and FastAPI.",
        email="your.email@example.com",
        linkedin_url="https://linkedin.com/in/yourprofile",
        github_url="https://github.com/yourusername",
        website_url="https://yourwebsite.com"
    )

@router.get("/projects", response_model=List[ProjectSchema])
async def get_projects(featured_only: bool = False, session: AsyncSession = Depends(get_session)):
    """Get all projects or only featured ones"""
    try:
        # Try to get from database first
        query = select(ProjectModel).where(ProjectModel.is_published == True)
        if featured_only:
            query = query.where(ProjectModel.is_featured == True)
        query = query.order_by(ProjectModel.sort_order.desc(), ProjectModel.created_at.desc())
        
        result = await session.execute(query)
        projects = result.scalars().all()
        
        if projects:
            return [
                ProjectSchema(
                    id=p.id,
                    title=p.title,
                    description=p.description,
                    technologies=p.technologies or [],
                    github_url=p.github_url,
                    demo_url=p.demo_url,
                    image_url=p.image_url,
                    start_date=p.start_date,
                    end_date=p.end_date,
                    featured=p.is_featured
                )
                for p in projects
            ]
    except Exception as e:
        # Log the error but continue with fallback data
        print(f"Database error: {e}")
    
    # Fallback to static data if no database records or error
    projects = [
        ProjectSchema(
            id=1,
            title="Stitch CMS",
            description="A modern, AI-powered Content Management System built with Next.js and FastAPI",
            technologies=["Next.js", "TypeScript", "FastAPI", "Python", "PostgreSQL", "Tailwind CSS"],
            github_url="https://github.com/yourusername/cms",
            demo_url="https://your-cms-demo.com",
            start_date=date(2024, 1, 1),
            featured=True
        ),
        ProjectSchema(
            id=2,
            title="E-Commerce Platform",
            description="Full-stack e-commerce solution with payment integration and admin dashboard",
            technologies=["React", "Node.js", "Express", "MongoDB", "Stripe API"],
            github_url="https://github.com/yourusername/ecommerce",
            demo_url="https://your-ecommerce-demo.com",
            start_date=date(2023, 6, 1),
            end_date=date(2023, 12, 1),
            featured=True
        ),
        ProjectSchema(
            id=3,
            title="Task Management App",
            description="Collaborative task management application with real-time updates",
            technologies=["Vue.js", "Firebase", "Vuex", "CSS3"],
            github_url="https://github.com/yourusername/task-manager",
            start_date=date(2023, 1, 1),
            end_date=date(2023, 5, 1),
            featured=False
        )
    ]
    
    if featured_only:
        return [p for p in projects if p.featured]
    return projects

@router.get("/skills", response_model=List[SkillSchema])
async def get_skills():
    """Get all skills grouped by category"""
    # Sample skills data - replace with database queries later
    skills = [
        # Frontend
        SkillSchema(id=1, name="React", category="Frontend", level=5, years_of_experience=4),
        SkillSchema(id=2, name="Next.js", category="Frontend", level=4, years_of_experience=2),
        SkillSchema(id=3, name="TypeScript", category="Frontend", level=4, years_of_experience=3),
        SkillSchema(id=4, name="Vue.js", category="Frontend", level=3, years_of_experience=2),
        SkillSchema(id=5, name="Tailwind CSS", category="Frontend", level=5, years_of_experience=3),
        
        # Backend
        SkillSchema(id=6, name="Python", category="Backend", level=5, years_of_experience=5),
        SkillSchema(id=7, name="FastAPI", category="Backend", level=4, years_of_experience=2),
        SkillSchema(id=8, name="Node.js", category="Backend", level=4, years_of_experience=3),
        SkillSchema(id=9, name="Express.js", category="Backend", level=4, years_of_experience=3),
        
        # Database
        SkillSchema(id=10, name="PostgreSQL", category="Database", level=4, years_of_experience=3),
        SkillSchema(id=11, name="MongoDB", category="Database", level=3, years_of_experience=2),
        SkillSchema(id=12, name="SQLAlchemy", category="Database", level=4, years_of_experience=2),
        
        # DevOps
        SkillSchema(id=13, name="Docker", category="DevOps", level=3, years_of_experience=2),
        SkillSchema(id=14, name="GitHub Actions", category="DevOps", level=3, years_of_experience=2),
        SkillSchema(id=15, name="Vercel", category="DevOps", level=4, years_of_experience=2),
    ]
    return skills

@router.get("/experience", response_model=List[ExperienceSchema])
async def get_experience():
    """Get work experience in chronological order"""
    # Sample experience data - replace with database queries later
    experience = [
        ExperienceSchema(
            id=1,
            company="Tech Startup Inc.",
            position="Senior Full Stack Developer",
            description="Lead development of web applications using React, Next.js, and Python. Mentored junior developers and implemented CI/CD pipelines.",
            start_date=date(2022, 1, 1),
            location="Remote",
            is_current=True
        ),
        ExperienceSchema(
            id=2,
            company="Digital Agency Co.",
            position="Full Stack Developer",
            description="Developed custom web applications for clients using various technologies. Collaborated with designers and project managers to deliver high-quality solutions.",
            start_date=date(2020, 6, 1),
            end_date=date(2021, 12, 31),
            location="San Francisco, CA"
        ),
        ExperienceSchema(
            id=3,
            company="Web Solutions LLC",
            position="Frontend Developer",
            description="Built responsive web interfaces using React and Vue.js. Optimized application performance and implemented modern CSS frameworks.",
            start_date=date(2019, 1, 1),
            end_date=date(2020, 5, 31),
            location="New York, NY"
        )
    ]
    return experience

# Future endpoints for CRUD operations (when you add database models)
# @router.post("/projects", response_model=ProjectSchema)
# async def create_project(project: ProjectSchema, session: AsyncSession = Depends(get_session)):
#     """Create a new project"""
#     pass

# @router.put("/projects/{project_id}", response_model=ProjectSchema)
# async def update_project(project_id: int, project: ProjectSchema, session: AsyncSession = Depends(get_session)):
#     """Update a project"""
#     pass

# @router.delete("/projects/{project_id}")
# async def delete_project(project_id: int, session: AsyncSession = Depends(get_session)):
#     """Delete a project"""
#     pass