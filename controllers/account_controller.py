# controllers/account_controller.py
import random
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from datetime import datetime, timedelta
from models.db import supabase

# Temporary in-memory OTP cache
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


def verify_otp_controller(email, otp):
    record = otp_cache.get(email)

    if not record:
        return {"success": False, "message": "No OTP found. Please request a new one."}

    if datetime.utcnow() > record["expiry"]:
        otp_cache.pop(email, None)
        return {"success": False, "message": "OTP expired. Please request a new one."}

    if record["otp"] != otp:
        return {"success": False, "message": "Invalid OTP."}

    # OTP verified — insert user into Supabase
    try:
        # Get latest user_id (e.g., UU001, UU002)
        response = supabase.table("User").select("user_id").order("user_id", desc=True).limit(1).execute()
        last_id = response.data[0]["user_id"] if response.data else "UU000"
        new_id_num = int(last_id[2:]) + 1
        new_user_id = f"UU{new_id_num:03d}"

        supabase.table("User").insert({
            "user_id": new_user_id,
            "created_at": datetime.utcnow().isoformat(),
            "role": "user",
            "email": email,
            "name": record["name"],
            "password": record["password"],
            "status": "active"
        }).execute()

        otp_cache.pop(email, None)
        return {"success": True, "message": "Registration successful!"}

    except Exception as e:
        return {"success": False, "message": f"Database error: {e}"}
