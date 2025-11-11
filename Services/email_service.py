# services/email_service.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SENDER_EMAIL = os.environ.get("SENDER_EMAIL", "chongsq-wm22@student.tarc.edu.my") 
SENDER_PASSWORD = os.environ.get("SENDER_PASSWORD", "cyzt djru zque exwh") 

def send_otp_email(recipient_email, otp_code):
    """
    Sends the OTP code to the user's email.
    Returns: True on success, False on failure.
    """
    if SENDER_EMAIL == "chongsq-wm22@student.tarc.edu.my" or SENDER_PASSWORD == "cyzt djru zque exwh":
         print("❌ EMAIL ERROR: Please configure SENDER_EMAIL and SENDER_PASSWORD in your environment variables (or hardcode for testing only).")
         return False

    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = recipient_email
        msg['Subject'] = "TripMate Account Verification Code"

        body = f"""
        Dear TripMate User,

        Thank you for registering. Your 6-digit verification code is:

        *** {otp_code} ***

        Please enter this code in the app to complete your registration.
        This code will expire shortly (15 minutes).

        If you did not request this, please ignore this email.

        Best regards,
        TripMate Team
        """
        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, recipient_email, msg.as_string())
        
        print(f"✅ OTP {otp_code} sent successfully to {recipient_email}")
        return True

    except Exception as e:
        print(f"❌ Failed to send email to {recipient_email}: {e}")
        return False