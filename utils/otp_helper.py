import random, time

# In-memory storage for OTPs (you can later move to Redis)
otp_store = {}

def generate_otp(email):
    otp = str(random.randint(100000, 999999))
    expiry = time.time() + 300  # 5 minutes
    otp_store[email] = {"otp": otp, "expiry": expiry}
    return otp

def verify_otp(email, otp_input):
    data = otp_store.get(email)
    if not data:
        return False
    if time.time() > data["expiry"]:
        otp_store.pop(email, None)
        return False
    if data["otp"] == otp_input:
        otp_store.pop(email, None)
        return True
    return False
