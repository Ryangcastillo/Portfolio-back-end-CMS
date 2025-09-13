import smtplib
import asyncio
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from ..database import Event, RSVP, Communication, get_db
from ..config import get_settings

settings = get_settings()

class NotificationService:
    def __init__(self):
        self.smtp_server = settings.smtp_server
        self.smtp_port = settings.smtp_port
        self.smtp_username = settings.smtp_username
        self.smtp_password = settings.smtp_password
        self.from_email = settings.from_email
        
    async def send_email(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        text_content: Optional[str] = None
    ) -> bool:
        """Send an email using SMTP"""
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.from_email
            msg['To'] = to_email
            
            # Add text version if provided
            if text_content:
                text_part = MIMEText(text_content, 'plain')
                msg.attach(text_part)
            
            # Add HTML version
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)
            
            return True
        except Exception as e:
            print(f"Error sending email: {e}")
            return False
    
    async def send_invitation(
        self,
        event: Event,
        rsvp: RSVP,
        db: AsyncSession
    ) -> bool:
        """Send event invitation email"""
        
        # Generate RSVP links
        accept_url = f"{settings.frontend_url}/rsvp/{rsvp.id}/accept"
        decline_url = f"{settings.frontend_url}/rsvp/{rsvp.id}/decline"
        maybe_url = f"{settings.frontend_url}/rsvp/{rsvp.id}/maybe"
        
        subject = f"You're invited: {event.title}"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Event Invitation</title>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: #f8f9fa; padding: 20px; border-radius: 8px; margin-bottom: 20px; }}
                .event-details {{ background: #fff; border: 1px solid #e9ecef; border-radius: 8px; padding: 20px; margin-bottom: 20px; }}
                .buttons {{ text-align: center; margin: 30px 0; }}
                .btn {{ display: inline-block; padding: 12px 24px; margin: 0 10px; text-decoration: none; border-radius: 6px; font-weight: bold; }}
                .btn-accept {{ background: #28a745; color: white; }}
                .btn-decline {{ background: #dc3545; color: white; }}
                .btn-maybe {{ background: #ffc107; color: #212529; }}
                .footer {{ text-align: center; color: #6c757d; font-size: 14px; margin-top: 30px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>You're Invited!</h1>
                    <p>You have been invited to attend the following event:</p>
                </div>
                
                <div class="event-details">
                    <h2>{event.title}</h2>
                    {f'<p><strong>Description:</strong> {event.description}</p>' if event.description else ''}
                    <p><strong>Date:</strong> {event.start_date.strftime('%B %d, %Y at %I:%M %p')}</p>
                    {f'<p><strong>End Date:</strong> {event.end_date.strftime('%B %d, %Y at %I:%M %p')}</p>' if event.end_date else ''}
                    {f'<p><strong>Location:</strong> {event.location}</p>' if event.location else ''}
                    <p><strong>Event Type:</strong> {event.event_type.title()}</p>
                    {f'<p><strong>RSVP Deadline:</strong> {event.rsvp_deadline.strftime('%B %d, %Y at %I:%M %p')}</p>' if event.rsvp_deadline else ''}
                </div>
                
                <div class="buttons">
                    <a href="{accept_url}" class="btn btn-accept">Accept</a>
                    <a href="{maybe_url}" class="btn btn-maybe">Maybe</a>
                    <a href="{decline_url}" class="btn btn-decline">Decline</a>
                </div>
                
                <div class="footer">
                    <p>Please respond by clicking one of the buttons above.</p>
                    <p>If you have any questions, please contact the event organizer.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Send email
        success = await self.send_email(rsvp.email, subject, html_content)
        
        # Log communication
        if success:
            communication = Communication(
                event_id=event.id,
                rsvp_id=rsvp.id,
                type="invitation",
                subject=subject,
                message=html_content,
                recipient_email=rsvp.email,
                recipient_name=rsvp.name,
                sent_at=datetime.utcnow(),
                delivery_status="sent"
            )
            db.add(communication)
            
            # Update RSVP
            rsvp.invitation_sent_at = datetime.utcnow()
            
            await db.commit()
        
        return success
    
    async def send_reminder(
        self,
        event: Event,
        rsvp: RSVP,
        db: AsyncSession,
        days_before: int
    ) -> bool:
        """Send event reminder email"""
        
        # Generate RSVP links if not responded yet
        rsvp_links = ""
        if rsvp.status == "pending":
            accept_url = f"{settings.frontend_url}/rsvp/{rsvp.id}/accept"
            decline_url = f"{settings.frontend_url}/rsvp/{rsvp.id}/decline"
            maybe_url = f"{settings.frontend_url}/rsvp/{rsvp.id}/maybe"
            
            rsvp_links = f"""
            <div class="buttons">
                <p>Haven't responded yet? Please let us know:</p>
                <a href="{accept_url}" class="btn btn-accept">Accept</a>
                <a href="{maybe_url}" class="btn btn-maybe">Maybe</a>
                <a href="{decline_url}" class="btn btn-decline">Decline</a>
            </div>
            """
        
        subject = f"Reminder: {event.title} - {days_before} day{'s' if days_before != 1 else ''} to go!"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Event Reminder</title>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: #e3f2fd; padding: 20px; border-radius: 8px; margin-bottom: 20px; }}
                .event-details {{ background: #fff; border: 1px solid #e9ecef; border-radius: 8px; padding: 20px; margin-bottom: 20px; }}
                .buttons {{ text-align: center; margin: 30px 0; }}
                .btn {{ display: inline-block; padding: 12px 24px; margin: 0 10px; text-decoration: none; border-radius: 6px; font-weight: bold; }}
                .btn-accept {{ background: #28a745; color: white; }}
                .btn-decline {{ background: #dc3545; color: white; }}
                .btn-maybe {{ background: #ffc107; color: #212529; }}
                .footer {{ text-align: center; color: #6c757d; font-size: 14px; margin-top: 30px; }}
                .status {{ padding: 10px; border-radius: 6px; margin: 20px 0; }}
                .status-accepted {{ background: #d4edda; color: #155724; }}
                .status-declined {{ background: #f8d7da; color: #721c24; }}
                .status-maybe {{ background: #fff3cd; color: #856404; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Event Reminder</h1>
                    <p>This is a friendly reminder about your upcoming event:</p>
                </div>
                
                <div class="event-details">
                    <h2>{event.title}</h2>
                    {f'<p><strong>Description:</strong> {event.description}</p>' if event.description else ''}
                    <p><strong>Date:</strong> {event.start_date.strftime('%B %d, %Y at %I:%M %p')}</p>
                    {f'<p><strong>End Date:</strong> {event.end_date.strftime('%B %d, %Y at %I:%M %p')}</p>' if event.end_date else ''}
                    {f'<p><strong>Location:</strong> {event.location}</p>' if event.location else ''}
                    <p><strong>Time until event:</strong> {days_before} day{'s' if days_before != 1 else ''}</p>
                </div>
                
                {f'<div class="status status-{rsvp.status}"><strong>Your RSVP Status:</strong> {rsvp.status.title()}</div>' if rsvp.status != "pending" else ''}
                
                {rsvp_links}
                
                <div class="footer">
                    <p>We look forward to seeing you at the event!</p>
                    <p>If you have any questions, please contact the event organizer.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Send email
        success = await self.send_email(rsvp.email, subject, html_content)
        
        # Log communication
        if success:
            communication = Communication(
                event_id=event.id,
                rsvp_id=rsvp.id,
                type="reminder",
                subject=subject,
                message=html_content,
                recipient_email=rsvp.email,
                recipient_name=rsvp.name,
                sent_at=datetime.utcnow(),
                delivery_status="sent"
            )
            db.add(communication)
            
            # Update reminder tracking
            rsvp.reminder_count += 1
            rsvp.last_reminder_sent = datetime.utcnow()
            
            await db.commit()
        
        return success
    
    async def send_confirmation(
        self,
        event: Event,
        rsvp: RSVP,
        db: AsyncSession
    ) -> bool:
        """Send RSVP confirmation email"""
        
        status_messages = {
            "accepted": "Thank you for accepting our invitation!",
            "declined": "Thank you for letting us know you can't make it.",
            "maybe": "Thank you for your response. We hope you can join us!"
        }
        
        subject = f"RSVP Confirmation: {event.title}"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>RSVP Confirmation</title>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: #d4edda; padding: 20px; border-radius: 8px; margin-bottom: 20px; }}
                .event-details {{ background: #fff; border: 1px solid #e9ecef; border-radius: 8px; padding: 20px; margin-bottom: 20px; }}
                .footer {{ text-align: center; color: #6c757d; font-size: 14px; margin-top: 30px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>RSVP Confirmed</h1>
                    <p>{status_messages.get(rsvp.status, 'Thank you for your response.')}</p>
                </div>
                
                <div class="event-details">
                    <h2>{event.title}</h2>
                    <p><strong>Your Response:</strong> {rsvp.status.title()}</p>
                    {f'<p><strong>Guest Count:</strong> {rsvp.guest_count}</p>' if rsvp.guest_count > 1 else ''}
                    {f'<p><strong>Dietary Restrictions:</strong> {rsvp.dietary_restrictions}</p>' if rsvp.dietary_restrictions else ''}
                    {f'<p><strong>Special Requests:</strong> {rsvp.special_requests}</p>' if rsvp.special_requests else ''}
                    
                    <hr style="margin: 20px 0;">
                    
                    <h3>Event Details</h3>
                    <p><strong>Date:</strong> {event.start_date.strftime('%B %d, %Y at %I:%M %p')}</p>
                    {f'<p><strong>End Date:</strong> {event.end_date.strftime('%B %d, %Y at %I:%M %p')}</p>' if event.end_date else ''}
                    {f'<p><strong>Location:</strong> {event.location}</p>' if event.location else ''}
                </div>
                
                <div class="footer">
                    <p>If you need to change your response, please contact the event organizer.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Send email
        success = await self.send_email(rsvp.email, subject, html_content)
        
        # Log communication
        if success:
            communication = Communication(
                event_id=event.id,
                rsvp_id=rsvp.id,
                type="confirmation",
                subject=subject,
                message=html_content,
                recipient_email=rsvp.email,
                recipient_name=rsvp.name,
                sent_at=datetime.utcnow(),
                delivery_status="sent"
            )
            db.add(communication)
            await db.commit()
        
        return success

# Background task for sending reminders
async def send_event_reminders():
    """Background task to send event reminders"""
    async for db in get_db():
        try:
            notification_service = NotificationService()
            
            # Get events that need reminders
            now = datetime.utcnow()
            
            # Find events with reminders enabled
            events_query = select(Event).where(
                and_(
                    Event.send_reminders == True,
                    Event.status == "published",
                    Event.start_date > now
                )
            )
            
            result = await db.execute(events_query)
            events = result.scalars().all()
            
            for event in events:
                if not event.reminder_days_before:
                    continue
                
                for days_before in event.reminder_days_before:
                    reminder_date = event.start_date - timedelta(days=days_before)
                    
                    # Check if we should send reminder today
                    if (now.date() == reminder_date.date() and 
                        now.hour >= 9):  # Send reminders at 9 AM
                        
                        # Get RSVPs that haven't received this reminder yet
                        rsvps_query = select(RSVP).where(
                            and_(
                                RSVP.event_id == event.id,
                                RSVP.last_reminder_sent < reminder_date
                            )
                        )
                        
                        rsvp_result = await db.execute(rsvps_query)
                        rsvps = rsvp_result.scalars().all()
                        
                        for rsvp in rsvps:
                            await notification_service.send_reminder(
                                event, rsvp, db, days_before
                            )
                            
                            # Small delay to avoid overwhelming email server
                            await asyncio.sleep(1)
            
        except Exception as e:
            print(f"Error in reminder task: {e}")
        finally:
            await db.close()

# Initialize notification service
notification_service = NotificationService()
