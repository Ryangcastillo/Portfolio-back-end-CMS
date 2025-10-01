"""Utility helpers for serving portfolio content to the public frontend.

This module centralises the fallback data that powers the marketing
website while still giving us a single place to plug in database models
later.  Each function accepts an optional SQLAlchemy session so it can
transparently switch to persisted content once the portfolio models are
introduced.
"""
from __future__ import annotations

from datetime import date
from typing import Any, Dict, List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

# Attempt to import the upcoming portfolio ORM models.  They do not exist
# yet, but wiring the import behind a try/except means the service can run
# today with the fallback content and seamlessly switch to the database in
# the future.
try:  # pragma: no cover - models are not available yet
    from ..models.portfolio_models import (  # type: ignore
        PortfolioSummary as PortfolioSummaryModel,
        Project as ProjectModel,
        Skill as SkillModel,
        Experience as ExperienceModel,
        Testimonial as TestimonialModel,
    )
except ImportError:  # pragma: no cover - expected in the current codebase
    PortfolioSummaryModel = None
    ProjectModel = None
    SkillModel = None
    ExperienceModel = None
    TestimonialModel = None


class PortfolioDataService:
    """Return portfolio content from the database or fallback fixtures."""

    _SUMMARY: Dict[str, Any] = {
        "full_name": "Ryan Castillo",
        "title": "Data Analyst",
        "bio_description": (
            "Transforming business challenges into actionable insights through "
            "advanced analytics and AI innovation. 8+ years of experience "
            "delivering measurable business value through data-driven solutions."
        ),
        "availability_status": "Available for New Opportunities",
        "email": "ryan.castillo@example.com",
        "location": "Auckland, New Zealand",
        "linkedin_url": "https://linkedin.com/in/ryan-castillo",
        "github_url": "https://github.com/ryan-castillo",
        "website_url": "https://ryancastillo.dev",
        "resume_url": "/resume.pdf",
        "years_experience": 8,
    }

    _STATS: List[Dict[str, Any]] = [
        {"id": 1, "metric_name": "Years Experience", "metric_value": "8+"},
        {"id": 2, "metric_name": "Cost Savings", "metric_value": "$500K+"},
        {"id": 3, "metric_name": "Projects Delivered", "metric_value": "50+"},
    ]

    _SKILLS: List[Dict[str, Any]] = [
        {
            "id": 1,
            "title": "Data Analysis & Visualization",
            "description": "Power BI, SQL, Advanced Excel, Statistical Analysis",
            "icon_name": "BarChart3",
            "color_gradient": "from-blue-500 to-blue-600",
            "projects_count": "15+ projects",
            "impact_metric": "$500K+ savings",
            "category": "Data Analysis",
            "featured": True,
        },
        {
            "id": 2,
            "title": "Business Intelligence & Reporting",
            "description": "SAP FICO, Dynamics 365, ETL processes, Dashboard development",
            "icon_name": "Database",
            "color_gradient": "from-green-500 to-green-600",
            "projects_count": "20+ dashboards",
            "impact_metric": "98% data quality",
            "category": "Business Intelligence",
            "featured": True,
        },
        {
            "id": 3,
            "title": "Process Improvement & Automation",
            "description": "Agile methodologies, PowerApps, Workflow optimization, Vendor management",
            "icon_name": "Cog",
            "color_gradient": "from-purple-500 to-purple-600",
            "projects_count": "10+ processes",
            "impact_metric": "40% efficiency gain",
            "category": "Operations",
            "featured": True,
        },
        {
            "id": 4,
            "title": "Emerging AI & Machine Learning",
            "description": "Python, Predictive analytics, AI agent development, Automation workflows",
            "icon_name": "Brain",
            "color_gradient": "from-orange-500 to-orange-600",
            "projects_count": "5+ AI models",
            "impact_metric": "85% accuracy",
            "category": "Artificial Intelligence",
            "featured": True,
        },
        {
            "id": 5,
            "title": "Stakeholder Engagement",
            "description": "Cross-functional collaboration, vendor management, executive reporting",
            "icon_name": "Handshake",
            "color_gradient": "from-indigo-500 to-indigo-600",
            "projects_count": "30+ initiatives",
            "impact_metric": "98% satisfaction",
            "category": "Leadership",
            "featured": False,
        },
    ]

    _PROJECTS: List[Dict[str, Any]] = [
        {
            "id": 1,
            "title": "Procurement Analytics Dashboard",
            "short_description": (
                "Comprehensive Power BI dashboard analysing supplier performance "
                "and identifying cost optimisation opportunities."
            ),
            "full_description": (
                "Designed an enterprise procurement analytics platform with "
                "automated data refreshes, supplier scorecards, and predictive "
                "alerts for contract renewals."
            ),
            "impact_metric": "$200K annual savings",
            "business_problem": (
                "Leadership lacked visibility into supplier KPIs and contract "
                "performance, limiting their ability to negotiate effectively."
            ),
            "solution_approach": (
                "Centralised disparate SAP and Excel data sources into a Power BI "
                "semantic model with automated data quality rules."
            ),
            "results_achieved": (
                "Enabled quarterly renegotiations that reduced spend by 12% while "
                "improving supplier SLA compliance."
            ),
            "technologies": ["Power BI", "SQL", "SAP FICO"],
            "category": "Data Analysis",
            "demo_url": "https://example.com/procurement-dashboard-demo",
            "github_url": None,
            "thumbnail_url": "/images/projects/procurement-dashboard.jpg",
            "link": "/data-analysis",
            "start_date": date(2023, 2, 1),
            "end_date": date(2023, 9, 1),
            "featured": True,
        },
        {
            "id": 2,
            "title": "Predictive Maintenance Model",
            "short_description": (
                "Machine learning model predicting equipment failures 2 weeks in "
                "advance to enable proactive maintenance scheduling."
            ),
            "full_description": (
                "Developed a supervised learning pipeline that consumes IoT "
                "sensor telemetry to generate maintenance recommendations and "
                "alert operations teams."
            ),
            "impact_metric": "85% prediction accuracy",
            "business_problem": (
                "Unplanned outages were costing the organisation downtime and "
                "emergency repair fees."
            ),
            "solution_approach": (
                "Engineered features from historical failure data, trained "
                "gradient-boosted models, and deployed monitoring dashboards."
            ),
            "results_achieved": (
                "Reduced unexpected downtime by 35% and increased maintenance "
                "team productivity."
            ),
            "technologies": ["Python", "Scikit-learn", "Pandas"],
            "category": "Machine Learning",
            "demo_url": "https://example.com/predictive-maintenance-demo",
            "github_url": "https://github.com/ryan-castillo/predictive-maintenance",
            "thumbnail_url": "/images/projects/predictive-maintenance.jpg",
            "link": "/machine-learning",
            "start_date": date(2022, 5, 1),
            "end_date": date(2022, 12, 1),
            "featured": True,
        },
        {
            "id": 3,
            "title": "AI-Powered Process Automation",
            "short_description": (
                "Intelligent assistant that automates vendor inquiries and "
                "procurement process guidance to improve response times."
            ),
            "full_description": (
                "Built a conversational AI agent that integrates with ServiceNow "
                "and SharePoint to answer policy questions and trigger workflows."
            ),
            "impact_metric": "60% faster responses",
            "business_problem": (
                "Procurement specialists were overwhelmed by manual email traffic "
                "from internal stakeholders."
            ),
            "solution_approach": (
                "Trained intent classification models, orchestrated workflows, and "
                "exposed the assistant through Teams and a web widget."
            ),
            "results_achieved": (
                "Improved SLA compliance from 72% to 93% in the first quarter."
            ),
            "technologies": ["OpenRouter", "React", "Node.js"],
            "category": "AI Agents",
            "demo_url": "https://example.com/ai-process-automation",
            "github_url": None,
            "thumbnail_url": "/images/projects/ai-process-automation.jpg",
            "link": "/ai-agents",
            "start_date": date(2024, 1, 15),
            "featured": True,
        },
        {
            "id": 4,
            "title": "Supplier Risk Radar",
            "short_description": (
                "Risk scoring engine that blends financial, delivery, and market "
                "signals to anticipate supplier disruptions."
            ),
            "full_description": (
                "Implemented an analytics solution that aggregates risk signals "
                "and visualises them with drill-down exploration."
            ),
            "impact_metric": "Identified 3 critical supplier risks",
            "business_problem": (
                "The leadership team needed early warning signals to mitigate "
                "supplier disruption."
            ),
            "solution_approach": (
                "Combined third-party risk data with internal performance metrics "
                "and automated weekly email briefings."
            ),
            "results_achieved": (
                "Prevented potential stockouts worth $120K by switching suppliers "
                "before issues escalated."
            ),
            "technologies": ["Power BI", "Azure Data Factory", "Python"],
            "category": "Data Analysis",
            "demo_url": None,
            "github_url": None,
            "thumbnail_url": "/images/projects/supplier-risk-radar.jpg",
            "link": "/web-apps",
            "start_date": date(2021, 7, 1),
            "end_date": date(2021, 11, 1),
            "featured": False,
        },
    ]

    _EXPERIENCE: List[Dict[str, Any]] = [
        {
            "id": 1,
            "company": "Tech Startup Inc.",
            "position": "Senior Full Stack Developer",
            "description": (
                "Lead development of web applications using React, Next.js, and "
                "Python. Mentored junior developers and implemented CI/CD pipelines."
            ),
            "start_date": date(2022, 1, 1),
            "end_date": None,
            "location": "Remote",
            "is_current": True,
            "achievements": [
                "Reduced infrastructure spend by 18% through container optimisation.",
                "Launched customer analytics module adopted by 150+ enterprise accounts.",
            ],
        },
        {
            "id": 2,
            "company": "Digital Agency Co.",
            "position": "Full Stack Developer",
            "description": (
                "Developed custom web applications for clients using various technologies. "
                "Collaborated with designers and project managers to deliver high-quality solutions."
            ),
            "start_date": date(2020, 6, 1),
            "end_date": date(2021, 12, 31),
            "location": "San Francisco, CA",
            "achievements": [
                "Delivered 12 client projects on time with a 96% satisfaction score.",
            ],
        },
        {
            "id": 3,
            "company": "Web Solutions LLC",
            "position": "Frontend Developer",
            "description": (
                "Built responsive web interfaces using React and Vue.js. Optimised application "
                "performance and implemented modern CSS frameworks."
            ),
            "start_date": date(2019, 1, 1),
            "end_date": date(2020, 5, 31),
            "location": "New York, NY",
            "achievements": [
                "Cut page load times by 45% through performance audits and refactors.",
            ],
        },
    ]

    _TESTIMONIALS: List[Dict[str, Any]] = [
        {
            "id": 1,
            "name": "Sophia Martinez",
            "role": "Procurement Director",
            "company": "Spark New Zealand",
            "quote": (
                "Ryan transformed our procurement analytics. His dashboards exposed insights "
                "we had been missing for years and helped us unlock significant savings."
            ),
            "featured": True,
        },
        {
            "id": 2,
            "name": "Liam O'Connor",
            "role": "Head of Operations",
            "company": "Auckland Transport",
            "quote": (
                "The automation workflows Ryan delivered reduced our response times dramatically. "
                "He's a rare blend of technical excellence and stakeholder empathy."
            ),
            "featured": True,
        },
        {
            "id": 3,
            "name": "Isabella Chen",
            "role": "Analytics Manager",
            "company": "Tech Startup Inc.",
            "quote": (
                "Ryan consistently delivers reliable, well-tested solutions. His mentorship and "
                "focus on data quality elevated the entire analytics team."
            ),
            "featured": False,
        },
    ]

    @classmethod
    async def get_summary(cls, session: Optional[AsyncSession] = None) -> Dict[str, Any]:
        if PortfolioSummaryModel and session:  # pragma: no cover - future support
            try:
                result = await session.execute(
                    select(PortfolioSummaryModel).where(PortfolioSummaryModel.is_active == True)  # type: ignore[arg-type]
                )
                record = result.scalar_one_or_none()
                if record:
                    return {
                        "full_name": record.full_name,
                        "title": record.title,
                        "bio_description": record.bio_description,
                        "availability_status": record.availability_status,
                        "email": record.email,
                        "location": record.location,
                        "linkedin_url": record.linkedin_url,
                        "github_url": record.github_url,
                        "website_url": record.website_url,
                        "resume_url": record.resume_url,
                        "years_experience": record.years_experience,
                    }
            except Exception:
                # Fall back to the fixtures if the database query fails for any reason.
                pass
        return cls._SUMMARY

    @classmethod
    async def get_stats(cls, session: Optional[AsyncSession] = None) -> List[Dict[str, Any]]:
        # Stats are currently derived from the fallback fixtures.
        return cls._STATS

    @classmethod
    async def get_skills(cls, session: Optional[AsyncSession] = None) -> List[Dict[str, Any]]:
        return cls._SKILLS

    @classmethod
    async def get_projects(cls, session: Optional[AsyncSession] = None) -> List[Dict[str, Any]]:
        return cls._PROJECTS

    @classmethod
    async def get_experience(cls, session: Optional[AsyncSession] = None) -> List[Dict[str, Any]]:
        return cls._EXPERIENCE

    @classmethod
    async def get_testimonials(cls, session: Optional[AsyncSession] = None) -> List[Dict[str, Any]]:
        return cls._TESTIMONIALS

    @classmethod
    async def get_project_categories(cls, session: Optional[AsyncSession] = None) -> List[Dict[str, Any]]:
        projects = await cls.get_projects(session)
        counts: Dict[str, int] = {}
        for project in projects:
            category = project.get("category") or "Uncategorised"
            counts[category] = counts.get(category, 0) + 1
        return [
            {
                "slug": category.lower().replace(" ", "-"),
                "name": category,
                "project_count": count,
            }
            for category, count in counts.items()
        ]

    @classmethod
    async def get_homepage_data(cls, session: Optional[AsyncSession] = None) -> Dict[str, Any]:
        summary = await cls.get_summary(session)
        stats = await cls.get_stats(session)
        skills = await cls.get_skills(session)
        projects = await cls.get_projects(session)

        featured_skills = [skill for skill in skills if skill.get("featured")]
        featured_projects = [project for project in projects if project.get("featured")]

        return {
            "profile": summary,
            "stats": stats,
            "featured_skills": featured_skills,
            "featured_projects": featured_projects,
        }

    @classmethod
    async def get_portfolio_overview(cls, session: Optional[AsyncSession] = None) -> Dict[str, Any]:
        return {
            "profile": await cls.get_summary(session),
            "stats": await cls.get_stats(session),
            "skills": await cls.get_skills(session),
            "projects": await cls.get_projects(session),
            "experience": await cls.get_experience(session),
            "testimonials": await cls.get_testimonials(session),
        }
