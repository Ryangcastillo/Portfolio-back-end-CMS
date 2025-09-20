#!/usr/bin/env python3
"""
Simplified CMS Backend Server

A minimal FastAPI server that demonstrates the core CMS functionality
without complex database migrations. This provides the basic API endpoints
that the frontend expects.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, List, Any, Optional
from datetime import datetime
import json
import os

# Simple in-memory data store for demo purposes
class DataStore:
    def __init__(self):
        self.users = [
            {
                "id": 1,
                "name": "Admin User",
                "email": "admin@example.com",
                "role": "admin",
                "status": "active",
                "lastLogin": "2024-01-15T10:30:00Z",
                "createdAt": "2024-01-01T00:00:00Z",
            }
        ]
        
        self.content = [
            {
                "id": 1,
                "title": "Welcome to Stitch CMS",
                "slug": "welcome-to-stitch-cms",
                "content": "This is your first piece of content in Stitch CMS.",
                "status": "published",
                "createdAt": "2024-01-01T00:00:00Z",
                "updatedAt": "2024-01-01T00:00:00Z",
            }
        ]
        
        self.events = [
            {
                "id": 1,
                "title": "Launch Event",
                "description": "Official launch of our new CMS platform",
                "startTime": "2024-02-01T18:00:00Z",
                "endTime": "2024-02-01T20:00:00Z",
                "location": "Virtual",
                "maxAttendees": 100,
                "rsvpCount": 25,
                "createdAt": "2024-01-15T00:00:00Z",
            }
        ]
        
        self.rsvps = [
            {
                "id": 1,
                "eventId": 1,
                "email": "attendee@example.com",
                "name": "John Attendee",
                "status": "confirmed",
                "respondedAt": "2024-01-16T09:00:00Z",
            }
        ]
        
        self.settings = {
            "site_name": "Stitch CMS Demo",
            "site_description": "A powerful, modular content management system",
            "default_language": "en",
            "timezone": "UTC",
        }

# Initialize data store
data_store = DataStore()

# Create FastAPI app
app = FastAPI(
    title="Stitch CMS API",
    description="A simplified CMS API for demonstration",
    version="1.0.0-demo"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://your-domain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Stitch CMS API is running",
        "version": "1.0.0-demo",
        "status": "healthy"
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy", 
        "version": "1.0.0-demo",
        "timestamp": datetime.utcnow().isoformat(),
        "database": "in-memory",
    }

# Users endpoints
@app.get("/api/users")
async def get_users():
    return {"users": data_store.users, "total": len(data_store.users)}

@app.get("/api/users/{user_id}")
async def get_user(user_id: int):
    user = next((u for u in data_store.users if u["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Content endpoints
@app.get("/api/content")
async def get_content():
    return {"content": data_store.content, "total": len(data_store.content)}

@app.get("/api/content/{content_id}")
async def get_content_item(content_id: int):
    content = next((c for c in data_store.content if c["id"] == content_id), None)
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    return content

@app.post("/api/content")
async def create_content(content_data: Dict[str, Any]):
    new_id = max([c["id"] for c in data_store.content], default=0) + 1
    new_content = {
        "id": new_id,
        "createdAt": datetime.utcnow().isoformat(),
        "updatedAt": datetime.utcnow().isoformat(),
        **content_data
    }
    data_store.content.append(new_content)
    return new_content

# Events endpoints
@app.get("/api/events")
async def get_events():
    return {"events": data_store.events, "total": len(data_store.events)}

@app.get("/api/events/{event_id}")
async def get_event(event_id: int):
    event = next((e for e in data_store.events if e["id"] == event_id), None)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@app.get("/api/events/all-rsvps")
async def get_all_rsvps():
    return {"rsvps": data_store.rsvps, "total": len(data_store.rsvps)}

@app.get("/api/events/{event_id}/rsvps")
async def get_event_rsvps(event_id: int):
    event_rsvps = [r for r in data_store.rsvps if r["eventId"] == event_id]
    return {"rsvps": event_rsvps, "total": len(event_rsvps)}

# Settings endpoints
@app.get("/api/settings")
async def get_settings():
    return data_store.settings

@app.put("/api/settings")
async def update_settings(settings_data: Dict[str, Any]):
    data_store.settings.update(settings_data)
    return data_store.settings

# Analytics endpoints (mock data)
@app.get("/api/analytics/overview")
async def get_analytics_overview():
    return {
        "totalViews": 12543,
        "totalUsers": len(data_store.users),
        "totalContent": len(data_store.content),
        "totalEvents": len(data_store.events),
        "activeUsers": len([u for u in data_store.users if u["status"] == "active"]),
        "publishedContent": len([c for c in data_store.content if c["status"] == "published"]),
        "upcomingEvents": len([e for e in data_store.events if e["startTime"] > datetime.utcnow().isoformat()]),
    }

# AI Assistant endpoint (mock)
@app.post("/api/ai/generate")
async def generate_content(request_data: Dict[str, Any]):
    return {
        "generated_content": f"This is AI-generated content based on: {request_data.get('prompt', 'No prompt provided')}",
        "provider": "demo",
        "model": "demo-model-v1",
        "timestamp": datetime.utcnow().isoformat(),
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "simple_backend:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )