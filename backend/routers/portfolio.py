from __future__ import annotations

from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..services.portfolio_data import PortfolioDataService

router = APIRouter(tags=["Portfolio"])


class PortfolioStatSchema(BaseModel):
    id: int
    metric_name: str
    metric_value: str


class PortfolioSummarySchema(BaseModel):
    full_name: str
    title: str
    bio_description: str
    availability_status: Optional[str] = None
    email: Optional[str] = None
    location: Optional[str] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    website_url: Optional[str] = None
    resume_url: Optional[str] = None
    years_experience: Optional[int] = None


class SkillSchema(BaseModel):
    id: int
    title: str
    description: str
    category: Optional[str] = None
    icon_name: Optional[str] = None
    color_gradient: Optional[str] = None
    projects_count: Optional[str] = None
    impact_metric: Optional[str] = None
    featured: bool = False


class ProjectSchema(BaseModel):
    id: int
    title: str
    short_description: str
    full_description: Optional[str] = None
    description: Optional[str] = None
    business_problem: Optional[str] = None
    solution_approach: Optional[str] = None
    results_achieved: Optional[str] = None
    impact_metric: Optional[str] = None
    technologies: List[str] = []
    category: Optional[str] = None
    github_url: Optional[str] = None
    demo_url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    image_url: Optional[str] = None
    link: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    featured: bool = False


class ExperienceSchema(BaseModel):
    id: int
    company: str
    position: str
    description: str
    start_date: date
    end_date: Optional[date] = None
    location: Optional[str] = None
    is_current: bool = False
    achievements: Optional[List[str]] = None


class TestimonialSchema(BaseModel):
    id: int
    name: str
    role: Optional[str] = None
    company: Optional[str] = None
    quote: str
    featured: bool = False


class ProjectCategorySchema(BaseModel):
    slug: str
    name: str
    project_count: int


class HomepageDataSchema(BaseModel):
    profile: PortfolioSummarySchema
    stats: List[PortfolioStatSchema]
    featured_skills: List[SkillSchema]
    featured_projects: List[ProjectSchema]


class PortfolioOverviewSchema(BaseModel):
    profile: PortfolioSummarySchema
    stats: List[PortfolioStatSchema]
    skills: List[SkillSchema]
    projects: List[ProjectSchema]
    experience: List[ExperienceSchema]
    testimonials: List[TestimonialSchema]


@router.get("/api/v1/portfolio/summary", response_model=PortfolioSummarySchema)
@router.get("/api/public/profile", response_model=PortfolioSummarySchema)
async def get_portfolio_summary(session: AsyncSession = Depends(get_db)) -> PortfolioSummarySchema:
    summary = await PortfolioDataService.get_summary(session)
    return PortfolioSummarySchema(**summary)


@router.get("/api/v1/portfolio/stats", response_model=List[PortfolioStatSchema])
@router.get("/api/public/stats", response_model=List[PortfolioStatSchema])
async def get_portfolio_stats(session: AsyncSession = Depends(get_db)) -> List[PortfolioStatSchema]:
    stats = await PortfolioDataService.get_stats(session)
    return [PortfolioStatSchema(**item) for item in stats]


@router.get("/api/v1/portfolio/skills", response_model=List[SkillSchema])
@router.get("/api/public/skills", response_model=List[SkillSchema])
async def get_skills(
    featured_only: bool = False,
    category: Optional[str] = None,
    session: AsyncSession = Depends(get_db),
) -> List[SkillSchema]:
    skills = await PortfolioDataService.get_skills(session)
    filtered = []
    for skill in skills:
        if featured_only and not skill.get("featured"):
            continue
        if category and skill.get("category", "").lower() != category.lower():
            continue
        filtered.append(SkillSchema(**skill))
    return filtered


@router.get("/api/v1/portfolio/projects", response_model=List[ProjectSchema])
@router.get("/api/public/projects", response_model=List[ProjectSchema])
async def get_projects(
    featured_only: bool = False,
    category: Optional[str] = None,
    limit: Optional[int] = None,
    session: AsyncSession = Depends(get_db),
) -> List[ProjectSchema]:
    projects = await PortfolioDataService.get_projects(session)
    filtered = []
    for project in projects:
        if featured_only and not project.get("featured"):
            continue
        if category and project.get("category", "").lower() != category.lower():
            continue
        filtered.append(ProjectSchema(**project))

    if limit is not None:
        return filtered[: max(limit, 0)]
    return filtered


@router.get("/api/v1/portfolio/projects/{project_id}", response_model=ProjectSchema)
@router.get("/api/public/projects/{project_id}", response_model=ProjectSchema)
async def get_project_detail(
    project_id: int,
    session: AsyncSession = Depends(get_db),
) -> ProjectSchema:
    projects = await PortfolioDataService.get_projects(session)
    project = next((item for item in projects if item.get("id") == project_id), None)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return ProjectSchema(**project)


@router.get("/api/v1/portfolio/project-categories", response_model=List[ProjectCategorySchema])
@router.get("/api/public/project-categories", response_model=List[ProjectCategorySchema])
async def get_project_categories(session: AsyncSession = Depends(get_db)) -> List[ProjectCategorySchema]:
    categories = await PortfolioDataService.get_project_categories(session)
    return [ProjectCategorySchema(**item) for item in categories]


@router.get("/api/v1/portfolio/experience", response_model=List[ExperienceSchema])
@router.get("/api/public/experience", response_model=List[ExperienceSchema])
async def get_experience(
    featured_only: bool = False,
    session: AsyncSession = Depends(get_db),
) -> List[ExperienceSchema]:
    experience = await PortfolioDataService.get_experience(session)
    filtered = []
    for item in experience:
        if featured_only and not item.get("is_current"):
            continue
        filtered.append(ExperienceSchema(**item))
    return filtered


@router.get("/api/v1/portfolio/testimonials", response_model=List[TestimonialSchema])
@router.get("/api/public/testimonials", response_model=List[TestimonialSchema])
async def get_testimonials(
    featured_only: bool = False,
    limit: Optional[int] = None,
    session: AsyncSession = Depends(get_db),
) -> List[TestimonialSchema]:
    testimonials = await PortfolioDataService.get_testimonials(session)
    filtered = []
    for testimonial in testimonials:
        if featured_only and not testimonial.get("featured"):
            continue
        filtered.append(TestimonialSchema(**testimonial))
    if limit is not None:
        return filtered[: max(limit, 0)]
    return filtered


@router.get("/api/v1/portfolio/homepage-data", response_model=HomepageDataSchema)
@router.get("/api/public/homepage-data", response_model=HomepageDataSchema)
async def get_homepage_data(session: AsyncSession = Depends(get_db)) -> HomepageDataSchema:
    homepage = await PortfolioDataService.get_homepage_data(session)
    return HomepageDataSchema(
        profile=PortfolioSummarySchema(**homepage["profile"]),
        stats=[PortfolioStatSchema(**item) for item in homepage["stats"]],
        featured_skills=[SkillSchema(**item) for item in homepage["featured_skills"]],
        featured_projects=[ProjectSchema(**item) for item in homepage["featured_projects"]],
    )


@router.get("/api/v1/portfolio/overview", response_model=PortfolioOverviewSchema)
@router.get("/api/public/portfolio-overview", response_model=PortfolioOverviewSchema)
async def get_portfolio_overview(session: AsyncSession = Depends(get_db)) -> PortfolioOverviewSchema:
    overview = await PortfolioDataService.get_portfolio_overview(session)
    return PortfolioOverviewSchema(
        profile=PortfolioSummarySchema(**overview["profile"]),
        stats=[PortfolioStatSchema(**item) for item in overview["stats"]],
        skills=[SkillSchema(**item) for item in overview["skills"]],
        projects=[ProjectSchema(**item) for item in overview["projects"]],
        experience=[ExperienceSchema(**item) for item in overview["experience"]],
        testimonials=[TestimonialSchema(**item) for item in overview["testimonials"]],
    )
