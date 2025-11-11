import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

SENDER_EMAIL = "chongsq-wm22@student.tarc.edu.my"
SMTP_PASSWORD = "cyzt djru zque exwh"

def send_otp_email(receiver_email, otp_code, name):
    """Sends a 6-digit OTP code to the user's email."""
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = receiver_email
        msg['Subject'] = "TripMate Account Verification OTP"

        # Email body
        body = f"""
        Dear {name},

        Thank you for registering with TripMate!

        Your 6-digit One-Time Password (OTP) for account verification is:

        {otp_code}

        Please enter this code in the app to complete your registration. This code is valid for 10 minutes.

        If you did not attempt to register, please ignore this email.

        Best regards,
        The TripMate Team
        """
        msg.attach(MIMEText(body, 'plain'))

        # Connect to Gmail's SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        
        # Log in with your App Password
        server.login(SENDER_EMAIL, SMTP_PASSWORD)
        
        # Send the email
        text = msg.as_string()
        server.sendmail(SENDER_EMAIL, receiver_email, text)
        server.quit()

        print(f"✅ OTP email sent successfully to {receiver_email}")
        return {"success": True, "message": "OTP email sent successfully"}

    except Exception as e:
        print(f"❌ Failed to send email to {receiver_email}: {e}")
        return {"success": False, "message": f"Failed to send verification email. Error: {e}"}