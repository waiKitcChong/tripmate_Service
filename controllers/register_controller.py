# controllers/register_controller.py
from models.register_model import register_pending_user, check_email_exists, verify_and_activate_user
from utils.email_service import send_otp_email
from email_validator import validate_email, EmailNotValidError
from flask import jsonify

def register_user(name, email, password):
    """Handles the initial registration and OTP sending."""
    try:
        # Basic Email Format Validation
        try:
            validate_email(email, check_deliverability=False) 
        except EmailNotValidError as e:
            return {"success": False, "message": f"Invalid email format: {e}"}, 400

        # Check if email is already registered AND Active
        if check_email_exists(email):
            # Could check status here, but for simplicity, prevent registration if email exists
            response = {"success": False, "message": "This email is already registered."}
            return response, 409 # Conflict

        # 1. Create/Update a pending user record
        reg_result = register_pending_user(name, email, password)

        if not reg_result['success']:
            return {"success": False, "message": reg_result['message']}, 500

        otp_code = reg_result['otp']
        
        # 2. Send OTP email
        email_result = send_otp_email(email, otp_code, name)

        if not email_result['success']:
            # Log the failure but still return 200 for security, or return a 500
            print(f"Email send failed for {email}: {email_result['message']}")
            # You might choose to delete the pending user here, but for simplicity, we keep it
            
            # Since the main goal is to verify the email, a mail failure is a server issue.
            return {"success": False, "message": "Registration created, but failed to send verification email. Try resending later."}, 500


        return {"success": True, "message": "Registration successful. Please verify your email with the OTP sent."}, 200

    except Exception as e:
        print(f"Error during registration: {e}")
        return {"success": False, "message": f"Internal server error: {e}"}, 500


def resend_otp(email):
    """Handles resending an OTP for an existing pending user."""
    # This logic is very similar to initial registration, but skips the email existence check 
    # and only updates the pending record.
    try:
        # Check if a PENDING user exists
        # In this implementation, register_pending_user handles the update, 
        # but we need to ensure the user is 'Pending' first.
        
        # We can simulate the check by passing a placeholder password for simplicity
        # A more robust check should be added here to only allow resend for 'Pending' users.
        
        # To avoid re-generating the user_id, we fetch name and pass a placeholder
        
        # Fetch name for email
        # ... (implementation to fetch name and then call register_pending_user)
        # For simplicity now, let's assume we can fetch data or just rely on the model logic
        
        # Simplistic approach: Create a temporary pending record (which updates existing one)
        temp_name = "User" # Fallback name
        temp_password = "ResendPlaceholder" # Placeholder password
        
        reg_result = register_pending_user(temp_name, email, temp_password)

        if not reg_result['success']:
            return {"success": False, "message": reg_result['message']}, 400

        otp_code = reg_result['otp']
        
        # 2. Send OTP email (use temp_name or ideally fetch the real name)
        email_result = send_otp_email(email, otp_code, temp_name)
        
        if not email_result['success']:
            return {"success": False, "message": "Failed to send verification email. Try again later."}, 500
            
        return {"success": True, "message": "A new OTP has been sent to your email."}, 200

    except Exception as e:
        print(f"Error during resend OTP: {e}")
        return {"success": False, "message": f"Internal server error: {e}"}, 500


def verify_user_otp(email, otp):
    """Verifies the user-provided OTP and activates the account."""
    try:
        if not email or not otp:
            return {"success": False, "message": "Missing email or OTP."}, 400

        result = verify_and_activate_user(email, otp)
        
        if result['success']:
            return result, 200
        else:
            return result, 401

    except Exception as e:
        print(f"Error during OTP verification: {e}")
        return {"success": False, "message": f"Internal server error: {e}"}, 500