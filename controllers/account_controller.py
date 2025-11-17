import random
from datetime import datetime, timedelta
from models.db import supabase

otp_cache = {}

def send_otp_controller(name, email, password):
    # Generate OTP
    otp = str(random.randint(100000, 999999))
    otp_cache[email] = {
        "otp": otp,
        "expiry": datetime.utcnow() + timedelta(minutes=5),
        "name": name,
        "password": password
    }

   
    return {
        "success": True,
        "message": "OTP generated successfully.",
        "otp": otp   # Flutter will use this to send Gmail
    }

def verify_otp_controller(email, otp):
    record = otp_cache.get(email)
    if not record:
        return {"success": False, "message": "No OTP found. Please request a new one."}

    if datetime.utcnow() > record["expiry"]:
        otp_cache.pop(email, None)
        return {"success": False, "message": "OTP expired. Please request a new one."}

    if record["otp"] != otp:
        return {"success": False, "message": "Invalid OTP."}

    # OTP verified — insert user into Supabase
    try:
        response = supabase.table("User").select("user_id").order("user_id", desc=True).limit(1).execute()
        last_id = response.data[0]["user_id"] if response.data else "UU000"
        new_id_num = int(last_id[2:]) + 1
        new_user_id = f"UU{new_id_num:03d}"

        supabase.table("User").insert({
            "user_id": new_user_id,
            "created_at": datetime.utcnow().isoformat(),
            "role": "tourist",
            "email": email,
            "name": record["name"],
            "password": record["password"],
            "status": "active"
        }).execute()

        response2 = supabase.table("Tourists").select("tourist_id").order("tourist_id", desc=True).limit(1).execute()
        last_id = response2.data[0]["tourist_id"] if response2.data else "TRS25001"
        new_id_num = int(last_id[3:]) + 1  # skip the "TRS" prefix
        new_tourist_id = f"TRS{new_id_num:05d}"

    
        
        supabase.table("Tourists").insert({
            "tourist_id": new_tourist_id,
            "name": record["name"],
            "user_id":new_user_id,
        }).execute()

        otp_cache.pop(email, None)
        return {"success": True, "message": "Registration successful!"}

    except Exception as e:
        return {"success": False, "message": f"Database error: {e}"}
