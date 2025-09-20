"""
Portfolio Content Models for Headless CMS

These models store content that will be managed through the admin interface
and served to the public-facing website via API endpoints.
"""

from datetime import datetime
from typing import Optional, List
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from database import Base


class ProfileInfo(Base):
    """Main profile/bio information"""
    __tablename__ = "profile_info"
    
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255), nullable=False)
    title = Column(String(255), nullable=False)
    subtitle = Column(Text, nullable=True)
    bio_description = Column(Text, nullable=False)
    years_experience = Column(Integer, nullable=False)
    availability_status = Column(String(100), nullable=False, default="Available for New Opportunities")
    resume_url = Column(String(500), nullable=True)
    
    # Contact information
    email = Column(String(255), nullable=True)
    phone = Column(String(50), nullable=True)
    location = Column(String(255), nullable=True)
    
    # Social links
    linkedin_url = Column(String(500), nullable=True)
    github_url = Column(String(500), nullable=True)
    portfolio_url = Column(String(500), nullable=True)
    
    # Meta
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ProfileStats(Base):
    """Key statistics displayed on homepage"""
    __tablename__ = "profile_stats"
    
    id = Column(Integer, primary_key=True, index=True)
    metric_name = Column(String(255), nullable=False)  # e.g., "Years Experience", "Cost Savings"
    metric_value = Column(String(100), nullable=False)  # e.g., "8+", "$500K+"
    metric_description = Column(String(255), nullable=True)
    display_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Skill(Base):
    """Skills and expertise areas"""
    __tablename__ = "skills"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    
    # Visual elements
    icon_name = Column(String(100), nullable=True)  # Lucide icon name
    color_gradient = Column(String(255), nullable=True)  # CSS gradient classes
    
    # Metrics
    projects_count = Column(String(100), nullable=True)  # e.g., "15+ projects"
    impact_metric = Column(String(255), nullable=True)  # e.g., "$500K+ savings"
    
    # Categories
    category = Column(String(100), nullable=True)  # Data Analysis, AI, etc.
    skill_level = Column(String(50), nullable=True)  # Beginner, Intermediate, Expert
    
    # Display
    display_order = Column(Integer, default=0)
    is_featured = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ProjectCategory(Base):
    """Categories for organizing projects"""
    __tablename__ = "project_categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    slug = Column(String(255), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    icon_name = Column(String(100), nullable=True)
    color_theme = Column(String(100), nullable=True)
    
    display_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    projects = relationship("Project", back_populates="category")
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Project(Base):
    """Individual projects and case studies"""
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    short_description = Column(Text, nullable=False)
    full_description = Column(Text, nullable=True)
    
    # Business impact
    impact_metric = Column(String(255), nullable=True)  # e.g., "$200K annual savings"
    business_problem = Column(Text, nullable=True)
    solution_approach = Column(Text, nullable=True)
    results_achieved = Column(Text, nullable=True)
    
    # Technical details
    technologies = Column(JSON, nullable=True)  # Array of tech stack items
    methodology = Column(Text, nullable=True)
    challenges_overcome = Column(Text, nullable=True)
    
    # Media and links
    thumbnail_url = Column(String(500), nullable=True)
    image_gallery = Column(JSON, nullable=True)  # Array of image URLs
    demo_url = Column(String(500), nullable=True)
    github_url = Column(String(500), nullable=True)
    case_study_url = Column(String(500), nullable=True)
    
    # Organization
    category_id = Column(Integer, ForeignKey("project_categories.id"), nullable=True)
    category = relationship("ProjectCategory", back_populates="projects")
    
    # Display settings
    is_featured = Column(Boolean, default=False)
    display_order = Column(Integer, default=0)
    is_published = Column(Boolean, default=True)
    
    # Timeline
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    project_duration = Column(String(100), nullable=True)  # e.g., "3 months"
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Experience(Base):
    """Work experience and employment history"""
    __tablename__ = "experience"
    
    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String(255), nullable=False)
    position_title = Column(String(255), nullable=False)
    company_description = Column(Text, nullable=True)
    
    # Timeline
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=True)  # NULL for current position
    is_current = Column(Boolean, default=False)
    
    # Location
    location = Column(String(255), nullable=True)
    work_type = Column(String(100), nullable=True)  # Remote, Hybrid, On-site
    
    # Content
    key_responsibilities = Column(JSON, nullable=True)  # Array of responsibility strings
    key_achievements = Column(JSON, nullable=True)  # Array of achievement strings
    technologies_used = Column(JSON, nullable=True)  # Array of tech stack
    
    # Display
    display_order = Column(Integer, default=0)
    is_featured = Column(Boolean, default=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Testimonial(Base):
    """Client and colleague testimonials"""
    __tablename__ = "testimonials"
    
    id = Column(Integer, primary_key=True, index=True)
    author_name = Column(String(255), nullable=False)
    author_title = Column(String(255), nullable=True)
    author_company = Column(String(255), nullable=True)
    author_avatar_url = Column(String(500), nullable=True)
    
    # Content
    testimonial_text = Column(Text, nullable=False)
    rating = Column(Integer, nullable=True)  # 1-5 stars
    
    # Project context
    project_context = Column(String(255), nullable=True)
    collaboration_type = Column(String(100), nullable=True)  # Client, Colleague, Manager
    
    # Display
    is_featured = Column(Boolean, default=False)
    display_order = Column(Integer, default=0)
    is_approved = Column(Boolean, default=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class BlogPost(Base):
    """Blog posts and articles (optional for future expansion)"""
    __tablename__ = "blog_posts"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    slug = Column(String(255), nullable=False, unique=True)
    excerpt = Column(Text, nullable=True)
    content = Column(Text, nullable=False)
    
    # SEO
    meta_title = Column(String(255), nullable=True)
    meta_description = Column(Text, nullable=True)
    
    # Media
    featured_image_url = Column(String(500), nullable=True)
    
    # Organization
    tags = Column(JSON, nullable=True)  # Array of tag strings
    category = Column(String(100), nullable=True)
    
    # Publishing
    is_published = Column(Boolean, default=False)
    published_at = Column(DateTime, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)