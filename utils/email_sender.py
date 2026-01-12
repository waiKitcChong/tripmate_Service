import smtplib
from email.mime.text import MIMEText

def send_otp_email(receiver_email, otp_code):
    sender = ""
    password = ""  

    msg = MIMEText(f"Your TripMate OTP Code is: {otp_code}\n\nThis code will expire in 5 minutes.")
    msg["Subject"] = "TripMate Email Verification"
    msg["From"] = sender
    msg["To"] = receiver_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
