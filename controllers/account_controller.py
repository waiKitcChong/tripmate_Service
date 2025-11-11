from models.account_model import check_existing_user, insert_new_user
from utils.otp_helper import generate_otp, verify_otp
from utils.email_sender import send_otp_email

pending_users = {}  # temporarily store registration info before OTP verify

def send_otp_controller(name, email, password):
    if check_existing_user(email):
        return {"success": False, "message": "Email already registered"}

    otp = generate_otp(email)
    email_sent = send_otp_email(email, otp)

    if not email_sent:
        return {"success": False, "message": "Failed to send OTP"}

    pending_users[email] = {"name": name, "email": email, "password": password}
    return {"success": True, "message": "OTP sent to email"}

def verify_otp_controller(email, otp_input):
    if not verify_otp(email, otp_input):
        return {"success": False, "message": "Invalid or expired OTP"}

    user_data = pending_users.pop(email, None)
    if not user_data:
        return {"success": False, "message": "No registration data found"}

    new_id = insert_new_user(user_data["name"], user_data["email"], user_data["password"])
    return {"success": True, "message": "Registration successful", "user_id": new_id}
