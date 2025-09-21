from sqlalchemy import Column, Integer, String, Text, Boolean, Date, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import date, datetime
from typing import Optional, List

Base = declarative_base()

class PortfolioSummary(Base):
    __tablename__ = "portfolio_summary"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    title = Column(String(200), nullable=False)
    bio = Column(Text, nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(50), nullable=True)
    location = Column(String(255), nullable=True)
    linkedin_url = Column(String(500), nullable=True)
    github_url = Column(String(500), nullable=True)
    website_url = Column(String(500), nullable=True)
    resume_url = Column(String(500), nullable=True)
    profile_image_url = Column(String(500), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

class Project(Base):
    __tablename__ = "portfolio_projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    short_description = Column(String(500), nullable=True)  # For cards/previews
    technologies = Column(JSON, nullable=False)  # Array of technology strings
    github_url = Column(String(500), nullable=True)
    demo_url = Column(String(500), nullable=True)
    image_url = Column(String(500), nullable=True)
    images = Column(JSON, nullable=True)  # Array of image URLs for gallery
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    is_featured = Column(Boolean, default=False, nullable=False)
    is_published = Column(Boolean, default=True, nullable=False)
    sort_order = Column(Integer, default=0, nullable=False)  # For custom ordering
    category = Column(String(100), nullable=True)  # e.g., "Web Development", "Mobile App"
    client = Column(String(200), nullable=True)  # If it's client work
    team_size = Column(Integer, nullable=True)
    my_role = Column(String(200), nullable=True)  # Your specific role in the project
    challenges = Column(Text, nullable=True)  # Technical challenges faced
    solutions = Column(Text, nullable=True)  # How you solved them
    results = Column(Text, nullable=True)  # Project outcomes/metrics
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

class Skill(Base):
    __tablename__ = "portfolio_skills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    category = Column(String(100), nullable=False)  # Frontend, Backend, Database, DevOps, Design, etc.
    subcategory = Column(String(100), nullable=True)  # More specific grouping
    level = Column(Integer, nullable=False)  # 1-5 proficiency level
    years_of_experience = Column(Integer, nullable=True)
    is_primary = Column(Boolean, default=False, nullable=False)  # Primary/core skills
    icon_name = Column(String(100), nullable=True)  # For displaying icons
    color = Column(String(7), nullable=True)  # Hex color for theming
    sort_order = Column(Integer, default=0, nullable=False)
    description = Column(Text, nullable=True)  # Additional details about expertise
    certifications = Column(JSON, nullable=True)  # Array of related certifications
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

class Experience(Base):
    __tablename__ = "portfolio_experience"

    id = Column(Integer, primary_key=True, index=True)
    company = Column(String(200), nullable=False)
    position = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    short_description = Column(String(500), nullable=True)  # For timeline view
    responsibilities = Column(JSON, nullable=True)  # Array of key responsibilities
    achievements = Column(JSON, nullable=True)  # Array of achievements
    technologies = Column(JSON, nullable=True)  # Technologies used in this role
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    is_current = Column(Boolean, default=False, nullable=False)
    location = Column(String(255), nullable=True)
    company_url = Column(String(500), nullable=True)
    company_logo_url = Column(String(500), nullable=True)
    employment_type = Column(String(50), nullable=True)  # Full-time, Part-time, Contract, etc.
    is_remote = Column(Boolean, default=False, nullable=False)
    sort_order = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

class Education(Base):
    __tablename__ = "portfolio_education"

    id = Column(Integer, primary_key=True, index=True)
    institution = Column(String(200), nullable=False)
    degree = Column(String(200), nullable=False)
    field_of_study = Column(String(200), nullable=True)
    description = Column(Text, nullable=True)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    is_completed = Column(Boolean, default=True, nullable=False)
    gpa = Column(String(10), nullable=True)
    location = Column(String(255), nullable=True)
    institution_url = Column(String(500), nullable=True)
    sort_order = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

class Certification(Base):
    __tablename__ = "portfolio_certifications"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    issuer = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    issue_date = Column(Date, nullable=True)
    expiry_date = Column(Date, nullable=True)
    credential_id = Column(String(200), nullable=True)
    credential_url = Column(String(500), nullable=True)
    badge_image_url = Column(String(500), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    sort_order = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

class Testimonial(Base):
    __tablename__ = "portfolio_testimonials"

    id = Column(Integer, primary_key=True, index=True)
    client_name = Column(String(200), nullable=False)
    client_position = Column(String(200), nullable=True)
    client_company = Column(String(200), nullable=True)
    testimonial_text = Column(Text, nullable=False)
    client_image_url = Column(String(500), nullable=True)
    rating = Column(Integer, nullable=True)  # 1-5 star rating
    project_id = Column(Integer, nullable=True)  # Link to specific project if applicable
    is_featured = Column(Boolean, default=False, nullable=False)
    is_published = Column(Boolean, default=True, nullable=False)
    date_given = Column(Date, nullable=True)
    sort_order = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)