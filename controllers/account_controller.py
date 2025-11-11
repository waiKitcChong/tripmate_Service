# controllers/account_controller.py
import smtplib
import random
import threading
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from models.db import supabase
from datetime import datetime, timedelta

# Store OTP temporarily in memory (you can move to Supabase if needed)
otp_cache = {}

SENDER_EMAIL = "chongsq-wm22@student.tarc.edu.my"
SENDER_PASSWORD = "cyzt djru zque exwh"  # Gmail App Password

def send_email_async(recipient, subject, body):
    """Send email in background thread to prevent timeout"""
    def send():
        try:
            msg = MIMEMultipart()
            msg["From"] = SENDER_EMAIL
            msg["To"] = recipient
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "plain"))

            with smtplib.SMTP("smtp.gmail.com", 587, timeout=10) as server:
                server.starttls()
                server.login(SENDER_EMAIL, SENDER_PASSWORD)
                server.send_message(msg)
            print(f"✅ OTP email sent to {recipient}")
        except Exception as e:
            print(f"❌ Email send failed: {e}")
    threading.Thread(target=send).start()


def send_otp_controller(name, email, password):
    # Generate a random 6-digit OTP
    otp = str(random.randint(100000, 999999))

    # Cache OTP temporarily (5 minutes)
    otp_cache[email] = {
        "otp": otp,
        "expiry": datetime.utcnow() + timedelta(minutes=5),
        "name": name,
        "password": password
    }

    # Send email (non-blocking)
    subject = "TripMate Email Verification OTP"
    body = f"Hello {name},\n\nYour TripMate verification code is: {otp}\nThis code will expire in 5 minutes.\n\nThank you!"
    send_email_async(email, subject, body)

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

    # ✅ OTP verified — Insert user into Supabase
    try:
        # Find latest user_id (e.g., UU001, UU002...)
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
