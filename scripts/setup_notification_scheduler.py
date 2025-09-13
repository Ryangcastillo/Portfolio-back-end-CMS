import asyncio
import schedule
import time
from datetime import datetime
import sys
import os

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from backend.services.notification_service import send_event_reminders

def run_reminder_task():
    """Run the reminder task"""
    print(f"[{datetime.now()}] Running event reminder task...")
    try:
        asyncio.run(send_event_reminders())
        print(f"[{datetime.now()}] Event reminder task completed successfully")
    except Exception as e:
        print(f"[{datetime.now()}] Error in reminder task: {e}")

def main():
    """Main scheduler function"""
    print("Starting notification scheduler...")
    
    # Schedule reminder checks every hour
    schedule.every().hour.do(run_reminder_task)
    
    # Also run at specific times for better coverage
    schedule.every().day.at("09:00").do(run_reminder_task)  # 9 AM
    schedule.every().day.at("15:00").do(run_reminder_task)  # 3 PM
    
    print("Scheduler started. Checking for reminders every hour and at 9 AM, 3 PM daily.")
    print("Press Ctrl+C to stop the scheduler.")
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    except KeyboardInterrupt:
        print("\nScheduler stopped.")

if __name__ == "__main__":
    main()
