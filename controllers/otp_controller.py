import random
import time
from flask import jsonify
from utils.email_utils import send_email
from models.otp_model import save_otp, get_otp, delete_otp
from controllers.user_controller import create_user_if_not_exists

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_email(email):
    otp = generate_otp()
    save_otp(email, otp)
    send_email(email, "TripMate Email Verification", f"Your OTP code is: {otp}")
    return {"success": True, "message": "OTP sent to your email."}

def verify_otp_code(email, otp, name, password):
    stored_otp = get_otp(email)

    if not stored_otp:
        return {"success": False, "message": "No OTP found for this email."}

    if stored_otp != otp:
        return {"success": False, "message": "Invalid OTP."}

    delete_otp(email)
    result = create_user_if_not_exists(name, email, password)
    return result
