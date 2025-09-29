from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, JSON, ForeignKey
from sqlalchemy.sql import func
from datetime import datetime
from typing import AsyncGenerator

from .config import get_settings

settings = get_settings()

# Convert PostgreSQL URL to async, or use SQLite for development
if "sqlite" in settings.database_url:
    database_url = settings.database_url
else:
    database_url = settings.database_url.replace("postgresql://", "postgresql+asyncpg://")

engine = create_async_engine(database_url, echo=True)
AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

# Database Models
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    role = Column(String, default="editor")  # admin, editor, viewer
    is_active = Column(Boolean, default=True)
    preferences = Column(JSON, default={})
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Content(Base):
    __tablename__ = "content"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    slug = Column(String, unique=True, index=True)
    content_type = Column(String, nullable=False)  # article, page, blog_post
    body = Column(Text)
    excerpt = Column(Text)
    status = Column(String, default="draft")  # draft, published, archived
    author_id = Column(Integer, ForeignKey("users.id"))
    
    # SEO Fields
    meta_title = Column(String)
    meta_description = Column(Text)
    meta_keywords = Column(String)
    
    # AI Generated Content
    ai_generated = Column(Boolean, default=False)
    ai_suggestions = Column(JSON, default={})
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    published_at = Column(DateTime(timezone=True))

class Module(Base):
    __tablename__ = "modules"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    version = Column(String)
    is_active = Column(Boolean, default=False)
    configuration = Column(JSON, default={})
    api_keys = Column(JSON, default={})  # Encrypted storage for API keys
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class AIProvider(Base):
    __tablename__ = "ai_providers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)  # openrouter, openai, anthropic
    display_name = Column(String, nullable=False)
    api_key = Column(String)  # Encrypted
    base_url = Column(String)
    is_active = Column(Boolean, default=False)
    is_default = Column(Boolean, default=False)
    configuration = Column(JSON, default={})
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class SiteSettings(Base):
    __tablename__ = "site_settings"
    
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, nullable=False)
    value = Column(JSON)
    description = Column(Text)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Event(Base):
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    event_type = Column(String, default="meeting")  # meeting, webinar, conference, etc.
    start_date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True))
    location = Column(String)  # Physical or virtual location
    max_attendees = Column(Integer)
    
    # RSVP Settings
    rsvp_deadline = Column(DateTime(timezone=True))
    require_approval = Column(Boolean, default=False)
    allow_guests = Column(Boolean, default=False)
    
    # Communication Settings
    send_reminders = Column(Boolean, default=True)
    reminder_days_before = Column(JSON, default=[7, 1])  # Days before event to send reminders
    
    # Event Status
    status = Column(String, default="draft")  # draft, published, cancelled
    created_by = Column(Integer, ForeignKey("users.id"))
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class RSVP(Base):
    __tablename__ = "rsvps"
    
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    
    # Guest Information
    email = Column(String, nullable=False)
    name = Column(String, nullable=False)
    phone = Column(String)
    company = Column(String)
    
    # RSVP Response
    status = Column(String, default="pending")  # pending, accepted, declined, maybe
    guest_count = Column(Integer, default=1)
    dietary_restrictions = Column(Text)
    special_requests = Column(Text)
    
    # Tracking
    invitation_sent_at = Column(DateTime(timezone=True))
    responded_at = Column(DateTime(timezone=True))
    reminder_count = Column(Integer, default=0)
    last_reminder_sent = Column(DateTime(timezone=True))
    
    # Metadata
    source = Column(String, default="manual")  # manual, import, api
    notes = Column(Text)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Communication(Base):
    __tablename__ = "communications"
    
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"))
    rsvp_id = Column(Integer, ForeignKey("rsvps.id"))
    
    # Communication Details
    type = Column(String, nullable=False)  # invitation, reminder, confirmation, followup
    subject = Column(String)
    message = Column(Text)
    
    # Delivery Information
    recipient_email = Column(String, nullable=False)
    recipient_name = Column(String)
    sent_at = Column(DateTime(timezone=True))
    delivery_status = Column(String, default="pending")  # pending, sent, delivered, failed, bounced
    
    # Tracking
    opened_at = Column(DateTime(timezone=True))
    clicked_at = Column(DateTime(timezone=True))
    
    # Template and Personalization
    template_id = Column(String)
    personalization_data = Column(JSON, default={})
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    token_hash = Column(String, unique=True, index=True, nullable=False)  # sha256 of token
    family_id = Column(String, index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=False)
    revoked_at = Column(DateTime(timezone=True))

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
