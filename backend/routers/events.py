from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime, timedelta

from ..database import get_db, Event, RSVP, Communication, User
from ..auth import get_current_user

router = APIRouter()

class EventCreate(BaseModel):
    title: str
    description: Optional[str] = None
    event_type: str = "meeting"
    start_date: datetime
    end_date: Optional[datetime] = None
    location: Optional[str] = None
    max_attendees: Optional[int] = None
    rsvp_deadline: Optional[datetime] = None
    require_approval: bool = False
    allow_guests: bool = False
    send_reminders: bool = True
    reminder_days_before: List[int] = [7, 1]

class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    event_type: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    location: Optional[str] = None
    max_attendees: Optional[int] = None
    rsvp_deadline: Optional[datetime] = None
    require_approval: Optional[bool] = None
    allow_guests: Optional[bool] = None
    send_reminders: Optional[bool] = None
    reminder_days_before: Optional[List[int]] = None
    status: Optional[str] = None

class RSVPCreate(BaseModel):
    event_id: int
    email: EmailStr
    name: str
    phone: Optional[str] = None
    company: Optional[str] = None
    guest_count: int = 1
    dietary_restrictions: Optional[str] = None
    special_requests: Optional[str] = None

class RSVPUpdate(BaseModel):
    status: str  # accepted, declined, maybe
    guest_count: Optional[int] = None
    dietary_restrictions: Optional[str] = None
    special_requests: Optional[str] = None

class EventResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    event_type: str
    start_date: datetime
    end_date: Optional[datetime]
    location: Optional[str]
    max_attendees: Optional[int]
    rsvp_deadline: Optional[datetime]
    status: str
    total_rsvps: int
    accepted_rsvps: int
    declined_rsvps: int
    pending_rsvps: int
    created_at: datetime

@router.get("/", response_model=List[EventResponse])
async def list_events(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    status: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all events with RSVP statistics"""
    
    query = select(Event)
    if status:
        query = query.where(Event.status == status)
    
    query = query.offset(skip).limit(limit).order_by(Event.start_date.desc())
    result = await db.execute(query)
    events = result.scalars().all()
    
    # Get RSVP statistics for each event
    event_responses = []
    for event in events:
        rsvp_stats = await db.execute(
            select(
                func.count(RSVP.id).label("total"),
                func.sum(func.case((RSVP.status == "accepted", 1), else_=0)).label("accepted"),
                func.sum(func.case((RSVP.status == "declined", 1), else_=0)).label("declined"),
                func.sum(func.case((RSVP.status == "pending", 1), else_=0)).label("pending")
            ).where(RSVP.event_id == event.id)
        )
        stats = rsvp_stats.first()
        
        event_responses.append(EventResponse(
            id=event.id,
            title=event.title,
            description=event.description,
            event_type=event.event_type,
            start_date=event.start_date,
            end_date=event.end_date,
            location=event.location,
            max_attendees=event.max_attendees,
            rsvp_deadline=event.rsvp_deadline,
            status=event.status,
            total_rsvps=stats.total or 0,
            accepted_rsvps=stats.accepted or 0,
            declined_rsvps=stats.declined or 0,
            pending_rsvps=stats.pending or 0,
            created_at=event.created_at
        ))
    
    return event_responses

@router.post("/", response_model=dict)
async def create_event(
    event: EventCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new event"""
    
    db_event = Event(
        title=event.title,
        description=event.description,
        event_type=event.event_type,
        start_date=event.start_date,
        end_date=event.end_date,
        location=event.location,
        max_attendees=event.max_attendees,
        rsvp_deadline=event.rsvp_deadline,
        require_approval=event.require_approval,
        allow_guests=event.allow_guests,
        send_reminders=event.send_reminders,
        reminder_days_before=event.reminder_days_before,
        created_by=current_user.id
    )
    
    db.add(db_event)
    await db.commit()
    await db.refresh(db_event)
    
    return {"message": "Event created successfully", "event_id": db_event.id}

@router.get("/{event_id}")
async def get_event(
    event_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get event details with RSVP list"""
    
    result = await db.execute(select(Event).where(Event.id == event_id))
    event = result.scalar_one_or_none()
    
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Get RSVPs for this event
    rsvp_result = await db.execute(
        select(RSVP).where(RSVP.event_id == event_id).order_by(RSVP.created_at.desc())
    )
    rsvps = rsvp_result.scalars().all()
    
    return {
        "event": event,
        "rsvps": rsvps
    }

@router.put("/{event_id}")
async def update_event(
    event_id: int,
    event_update: EventUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update an event"""
    
    result = await db.execute(select(Event).where(Event.id == event_id))
    event = result.scalar_one_or_none()
    
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Update fields
    for field, value in event_update.dict(exclude_unset=True).items():
        setattr(event, field, value)
    
    await db.commit()
    await db.refresh(event)
    
    return {"message": "Event updated successfully"}

@router.post("/{event_id}/rsvps")
async def create_rsvp(
    event_id: int,
    rsvp: RSVPCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create an RSVP for an event (public endpoint)"""
    
    # Verify event exists
    result = await db.execute(select(Event).where(Event.id == event_id))
    event = result.scalar_one_or_none()
    
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Check if RSVP already exists for this email
    existing_rsvp = await db.execute(
        select(RSVP).where(and_(RSVP.event_id == event_id, RSVP.email == rsvp.email))
    )
    if existing_rsvp.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="RSVP already exists for this email")
    
    db_rsvp = RSVP(
        event_id=event_id,
        email=rsvp.email,
        name=rsvp.name,
        phone=rsvp.phone,
        company=rsvp.company,
        guest_count=rsvp.guest_count,
        dietary_restrictions=rsvp.dietary_restrictions,
        special_requests=rsvp.special_requests,
        status="pending"
    )
    
    db.add(db_rsvp)
    await db.commit()
    await db.refresh(db_rsvp)
    
    return {"message": "RSVP created successfully", "rsvp_id": db_rsvp.id}

@router.put("/rsvps/{rsvp_id}")
async def update_rsvp(
    rsvp_id: int,
    rsvp_update: RSVPUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update an RSVP response (public endpoint)"""
    
    result = await db.execute(select(RSVP).where(RSVP.id == rsvp_id))
    rsvp = result.scalar_one_or_none()
    
    if not rsvp:
        raise HTTPException(status_code=404, detail="RSVP not found")
    
    # Update RSVP
    rsvp.status = rsvp_update.status
    if rsvp_update.guest_count is not None:
        rsvp.guest_count = rsvp_update.guest_count
    if rsvp_update.dietary_restrictions is not None:
        rsvp.dietary_restrictions = rsvp_update.dietary_restrictions
    if rsvp_update.special_requests is not None:
        rsvp.special_requests = rsvp_update.special_requests
    
    rsvp.responded_at = datetime.utcnow()
    
    await db.commit()
    await db.refresh(rsvp)
    
    return {"message": "RSVP updated successfully"}

@router.post("/{event_id}/send-invitations")
async def send_invitations(
    event_id: int,
    recipient_emails: List[str],
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Send invitations to a list of email addresses"""
    
    # Verify event exists
    result = await db.execute(select(Event).where(Event.id == event_id))
    event = result.scalar_one_or_none()
    
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    sent_count = 0
    for email in recipient_emails:
        # Create RSVP record if it doesn't exist
        existing_rsvp = await db.execute(
            select(RSVP).where(and_(RSVP.event_id == event_id, RSVP.email == email))
        )
        
        if not existing_rsvp.scalar_one_or_none():
            db_rsvp = RSVP(
                event_id=event_id,
                email=email,
                name="",  # Will be filled when they respond
                status="pending",
                invitation_sent_at=datetime.utcnow()
            )
            db.add(db_rsvp)
            sent_count += 1
    
    await db.commit()
    
    return {"message": f"Invitations sent to {sent_count} recipients"}

@router.get("/{event_id}/analytics")
async def get_event_analytics(
    event_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get detailed analytics for an event"""
    
    # Get RSVP statistics
    rsvp_stats = await db.execute(
        select(
            func.count(RSVP.id).label("total_invites"),
            func.sum(func.case((RSVP.status == "accepted", 1), else_=0)).label("accepted"),
            func.sum(func.case((RSVP.status == "declined", 1), else_=0)).label("declined"),
            func.sum(func.case((RSVP.status == "maybe", 1), else_=0)).label("maybe"),
            func.sum(func.case((RSVP.status == "pending", 1), else_=0)).label("pending"),
            func.sum(RSVP.guest_count).label("total_guests")
        ).where(RSVP.event_id == event_id)
    )
    stats = rsvp_stats.first()
    
    # Get response timeline
    response_timeline = await db.execute(
        select(
            func.date(RSVP.responded_at).label("date"),
            func.count(RSVP.id).label("responses")
        ).where(
            and_(RSVP.event_id == event_id, RSVP.responded_at.isnot(None))
        ).group_by(func.date(RSVP.responded_at)).order_by(func.date(RSVP.responded_at))
    )
    timeline = response_timeline.all()
    
    return {
        "summary": {
            "total_invites": stats.total_invites or 0,
            "accepted": stats.accepted or 0,
            "declined": stats.declined or 0,
            "maybe": stats.maybe or 0,
            "pending": stats.pending or 0,
            "total_guests": stats.total_guests or 0,
            "response_rate": round((stats.accepted or 0) / max(stats.total_invites or 1, 1) * 100, 1)
        },
        "response_timeline": [
            {"date": str(row.date), "responses": row.responses}
            for row in timeline
        ]
    }
