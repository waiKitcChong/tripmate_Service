# controllers/account_controller.py
import random
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from datetime import datetime, timedelta
from models.db import supabase

otp_cache = {}

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")  # Set in Render dashboard
SENDER_EMAIL = "chongsq-wm22@student.tarc.edu.my"

def send_otp_controller(name, email, password):
    otp = str(random.randint(100000, 999999))
    otp_cache[email] = {
        "otp": otp,
        "expiry": datetime.utcnow() + timedelta(minutes=5),
        "name": name,
        "password": password
    }

    message = Mail(
        from_email=SENDER_EMAIL,
        to_emails=email,
        subject="TripMate Email Verification OTP",
        plain_text_content=f"Hello {name},\n\nYour verification code is: {otp}\nIt will expire in 5 minutes."
    )

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        sg.send(message)
        print(f"✅ OTP sent to {email}")
    except Exception as e:
        print(f"❌ SendGrid failed: {e}")

    return {"success": True, "message": "OTP sent successfully."}
