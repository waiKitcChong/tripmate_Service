# controllers/user_controller.py
from models.user_model import verify_user

import random
import smtplib
from email.message import EmailMessage
from db import supabase

def login_user(email, password):
    result = verify_user(email, password)
    return result



# 临时 OTP 存储
otp_store = {}  # {email: {"otp": "123456", "name": ..., "password": ...}}

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_email(name, email, otp):
    sender = "chongsq-wm22@student.tarc.edu.my"
    password = "cyzt djru zque exwh"  # Gmail App Password
    msg = EmailMessage()
    msg["Subject"] = "Your OTP Code"
    msg["From"] = sender
    msg["To"] = email
    msg.set_content(f"Hello {name}, your OTP is: {otp}")
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.send_message(msg)

def create_otp_record(name, email, password):

    existing = supabase.table("User").select("email").eq("email", email).execute()
    if existing.data:
        return {"success": False, "message": "Email already registered"}

    otp = generate_otp()
    otp_store[email] = {"otp": otp, "name": name, "password": password}
    send_otp_email(name, email, otp)
    return {"success": True, "message": "OTP sent successfully"}

def verify_otp_record(email, otp):
    if email not in otp_store:
        return {"success": False, "message": "No OTP requested"}
    if otp_store[email]["otp"] != otp:
        return {"success": False, "message": "Invalid OTP"}
    
    record = otp_store.pop(email)

    # 插入 Supabase User 表
    from datetime import datetime
    import uuid

    user_id = str(uuid.uuid4())
    created_at = datetime.utcnow().isoformat()
    user_data = {
        "user_id": user_id,
        "created_at": created_at,
        "role": "user",
        "email": email,
        "name": record["name"],
        "password": record["password"],
        "status": "active"
    }

    res = supabase.table("User").insert(user_data).execute()
    if res.error:
        return {"success": False, "message": res.error.message}
    return {"success": True, "message": "User registered successfully"}
