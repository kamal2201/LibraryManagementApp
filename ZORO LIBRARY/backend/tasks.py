from celery import Celery
from workers import celery
from models import *
from mailer import send_email
from celery.schedules import crontab
from datetime import datetime, timedelta
    
@celery.task
def send_approved_email(email):
    body = "Your book request has been approved successfully."
    subject = "Request Approved"
    try:
        send_email(email, subject, body)
        return f"Successfully sent email to {email}"
    except Exception as e:
        return f"Failed to send email to {email}. Error: {str(e)}"

@celery.task
def send_rejected_email(email):
    body = "Your book request has been rejected."
    subject = "Request Rejected"
    try:
        send_email(email, subject, body)
        return f"Successfully sent email to {email}"
    except Exception as e:
        return f"Failed to send email to {email}. Error: {str(e)}"

@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(hour=0, minute=0), check_user_logins.s(), name="Daily Reminder")

@celery.task
def send_daily_reminder(email):
    send_email(
        to=email,
        subject="Daily Reminder",
        body="It looks like you haven't logged in for a while. Please check your account!"
    )

@celery.task
def check_user_logins():
    one_day_ago = datetime.now() - timedelta(days=1)
    users = User.query.filter(User.last_loggedin < one_day_ago).all()

    for user in users:
        send_daily_reminder.delay(user.email)
