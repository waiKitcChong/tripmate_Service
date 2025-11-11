import smtplib
from email.mime.text import MIMEText

msg = MIMEText("Test email")
msg['Subject'] = "Test"
msg['From'] = "chongsq-wm22@student.tarc.edu.my"
msg['To'] = "waikitchong06@gmail.com"

with smtplib.SMTP("smtp.gmail.com", 587) as server:
    server.starttls()
    server.login("chongsq-wm22@student.tarc.edu.my", "cyzt djru zque exwh")
    server.send_message(msg)
print("Email sent")
