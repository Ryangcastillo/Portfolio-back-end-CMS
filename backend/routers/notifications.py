from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

from ..database import get_db, Event, RSVP, Communication, User
from ..auth import get_current_user
from ..security import requires_roles
from ..services.notification_service import notification_service

router = APIRouter()

class SendInvitationsRequest(BaseModel):
    recipient_emails: List[EmailStr]

class NotificationStats(BaseModel):
    total_sent: int
    total_delivered: int
    total_opened: int
    total_clicked: int
    bounce_rate: float
    open_rate: float
    click_rate: float

@router.post("/{event_id}/send-invitations", dependencies=[Depends(requires_roles("admin"))])
async def send_event_invitations(
    event_id: int,
    request: SendInvitationsRequest,
    background_tasks: BackgroundTasks,
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
    created_rsvps = []
    
    for email in request.recipient_emails:
        # Check if RSVP already exists
        existing_rsvp = await db.execute(
            select(RSVP).where(and_(RSVP.event_id == event_id, RSVP.email == email))
        )
        
        if not existing_rsvp.scalar_one_or_none():
            # Create new RSVP
            db_rsvp = RSVP(
                event_id=event_id,
                email=email,
                name="",  # Will be filled when they respond
                status="pending"
            )
            db.add(db_rsvp)
            created_rsvps.append(db_rsvp)
            sent_count += 1
    
    await db.commit()
    
    # Send invitations in background
    for rsvp in created_rsvps:
        await db.refresh(rsvp)
        background_tasks.add_task(
            notification_service.send_invitation,
            event, rsvp, db
        )
    
    return {"message": f"Invitations queued for {sent_count} recipients"}

@router.post("/{event_id}/send-reminders", dependencies=[Depends(requires_roles("admin"))])
async def send_event_reminders(
    event_id: int,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Manually send reminders for an event"""
    
    # Verify event exists
    result = await db.execute(select(Event).where(Event.id == event_id))
    event = result.scalar_one_or_none()
    
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Get all RSVPs for this event
    rsvps_result = await db.execute(
        select(RSVP).where(RSVP.event_id == event_id)
    )
    rsvps = rsvps_result.scalars().all()
    
    # Calculate days until event
    days_until = (event.start_date - datetime.utcnow()).days
    
    # Send reminders in background
    for rsvp in rsvps:
        background_tasks.add_task(
            notification_service.send_reminder,
            event, rsvp, db, days_until
        )
    
    return {"message": f"Reminders queued for {len(rsvps)} recipients"}

@router.get("/{event_id}/communications")
async def get_event_communications(
    event_id: int,
    skip: int = 0,
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get communication history for an event"""
    
    result = await db.execute(
        select(Communication)
        .where(Communication.event_id == event_id)
        .offset(skip)
        .limit(limit)
        .order_by(Communication.sent_at.desc())
    )
    
    communications = result.scalars().all()
    
    return communications

@router.get("/{event_id}/notification-stats")
async def get_notification_stats(
    event_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> NotificationStats:
    """Get notification statistics for an event"""
    
    # Get communication stats
    stats_result = await db.execute(
        select(
            func.count(Communication.id).label("total_sent"),
            func.sum(func.case((Communication.delivery_status == "delivered", 1), else_=0)).label("delivered"),
            func.sum(func.case((Communication.opened_at.isnot(None), 1), else_=0)).label("opened"),
            func.sum(func.case((Communication.clicked_at.isnot(None), 1), else_=0)).label("clicked"),
            func.sum(func.case((Communication.delivery_status == "bounced", 1), else_=0)).label("bounced")
        ).where(Communication.event_id == event_id)
    )
    
    stats = stats_result.first()
    
    total_sent = stats.total_sent or 0
    delivered = stats.delivered or 0
    opened = stats.opened or 0
    clicked = stats.clicked or 0
    bounced = stats.bounced or 0
    
    bounce_rate = (bounced / max(total_sent, 1)) * 100
    open_rate = (opened / max(delivered, 1)) * 100
    click_rate = (clicked / max(opened, 1)) * 100
    
    return NotificationStats(
        total_sent=total_sent,
        total_delivered=delivered,
        total_opened=opened,
        total_clicked=clicked,
        bounce_rate=round(bounce_rate, 2),
        open_rate=round(open_rate, 2),
        click_rate=round(click_rate, 2)
    )

@router.get("/templates")
async def get_notification_templates(
    current_user: User = Depends(get_current_user)
):
    """Get available notification templates"""
    
    templates = [
        {
            "id": "invitation",
            "name": "Event Invitation",
            "description": "Standard invitation email template",
            "type": "invitation"
        },
        {
            "id": "reminder",
            "name": "Event Reminder", 
            "description": "Reminder email template",
            "type": "reminder"
        },
        {
            "id": "confirmation",
            "name": "RSVP Confirmation",
            "description": "RSVP confirmation email template",
            "type": "confirmation"
        }
    ]
    
    return templates

@router.post("/test-email", dependencies=[Depends(requires_roles("admin"))])
async def send_test_email(
    recipient_email: EmailStr,
    current_user: User = Depends(get_current_user)
):
    """Send a test email to verify email configuration"""
    
    subject = "Test Email from Stitch CMS"
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Test Email</title>
    </head>
    <body>
        <h1>Test Email</h1>
        <p>This is a test email from your Stitch CMS notification system.</p>
        <p>If you received this email, your email configuration is working correctly!</p>
    </body>
    </html>
    """
    
    success = await notification_service.send_email(
        recipient_email, subject, html_content
    )
    
    if success:
        return {"message": "Test email sent successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to send test email")
