# controllers/user_controller.py
from models.user_model import verify_user, find_user_by_email, insert_new_user, update_user_otp, verify_user_otp
from Services.email_service import send_otp_email
from werkzeug.security import generate_password_hash
import random
from datetime import datetime, timezone, timedelta

def generate_otp():
    """Generates a 6-digit numeric OTP."""
    return str(random.randint(100000, 999999))

def register_user(name, email, password):
    """
    Handles user registration: checks email, creates record, and sends OTP.
    """
    if find_user_by_email(email):
        return {"success": False, "message": "Email already registered."}

    # 1. Generate password hash
    hashed_password = generate_password_hash(password)
    
    # 2. Generate OTP and expiry (15 minutes from now, UTC)
    otp_code = generate_otp()
    expiry_time = datetime.now(timezone.utc) + timedelta(minutes=15) 

    try:
        # 3. Insert new user with status 'unverified'
        user_id = insert_new_user(name, email, hashed_password)

        if not user_id:
             return {"success": False, "message": "Database insertion failed."}
        
        # 4. Store the OTP and expiry in the database
        update_user_otp(email, otp_code, expiry_time)

        # 5. Send OTP via email
        email_sent = send_otp_email(email, otp_code)
        
        if not email_sent:
            return {"success": False, "message": "Registration successful, but failed to send verification email. Please try resending."}

        return {"success": True, "message": "Registration successful. OTP sent to your email for verification."}
    
    except Exception as e:
        print(f"Error during registration: {e}")
        return {"success": False, "message": f"An unexpected error occurred during registration: {e}"}

def verify_otp_and_activate(email, otp):
    """
    Verifies the submitted OTP and activates the user account.
    """
    try:
        is_verified = verify_user_otp(email, otp) 

        if is_verified:
            return {"success": True, "message": "Account successfully verified."}
        else:
            return {"success": False, "message": "Invalid or expired verification code."}
            
    except Exception as e:
        print(f"Error during OTP verification: {e}")
        return {"success": False, "message": f"An unexpected error occurred: {e}"}

def login_user(email, password):
    # Existing login function
    result = verify_user(email, password)
    return result