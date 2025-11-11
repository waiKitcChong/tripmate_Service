import random
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from datetime import datetime, timedelta
from models.db import supabase
from dotenv import load_dotenv

load_dotenv()  # loads .env locally

otp_cache = {}

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
SENDER_EMAIL = "codeqiangod@gmail.com"

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

    sg = SendGridAPIClient(SENDGRID_API_KEY)
    sg.send(message)
    return {"success": True, "message": "OTP sent successfully."}

def verify_otp_controller(email, otp):
    # your OTP verification + insert user logic
    ...
