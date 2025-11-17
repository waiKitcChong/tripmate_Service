from models.db import supabase
from datetime import datetime

def get_latest_user_id():
    result = supabase.table("User").select("user_id").order("user_id", desc=True).limit(1).execute()
    if not result.data:
        return "UU000"
    latest_id = result.data[0]["user_id"]
    num = int(latest_id[2:]) + 1
    return f"UU{num:03d}"

def check_existing_user(email):
    result = supabase.table("User").select("*").eq("email", email).execute()
    return len(result.data) > 0

def insert_new_user(name, email, password):
    new_id = get_latest_user_id()
    
    response2 = supabase.table("Tourists").select("tourist_id").order("tourist_id", desc=True).limit(1).execute()
    last_id = response2.data[0]["tourist_id"] if response2.data else "TRS25001"
    new_id_num = int(last_id[3:]) + 1  # skip the "TRS" prefix
    new_tourist_id = f"TRS{new_id_num:05d}"

    
        
    supabase.table("Tourists").insert({
        "tourist_id": new_tourist_id,
         "name": name,
    }).execute()

    supabase.table("User").insert({
        "user_id": new_id,
        "created_at": datetime.utcnow().isoformat(),
        "role": "tourist",
        "email": email,
        "name": name,
        "password": password,
        "status": "active"
    }).execute()
    return new_id
