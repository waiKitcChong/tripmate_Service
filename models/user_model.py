# models/user_model.py
from models.db import supabase
from werkzeug.security import check_password_hash
from datetime import datetime

def verify_user(email, password):
    try:
        # 1️⃣ Query user by email
        response = supabase.table("User").select("*").eq("email", email).execute()

        if not response.data or len(response.data) == 0:
            return {"success": False, "message": "User not found"}

        user = response.data[0]

        # 2️⃣ Verify password (if hashed in DB)
        # If you store plaintext passwords (not recommended), compare directly:
        # if user["password"] != password:
        #     return {"success": False, "message": "Invalid password"}

        if not check_password_hash(user["password"], password):
            return {"success": False, "message": "Invalid password"}

        # 3️⃣ Update last login time
        supabase.table("User").update({"last_login": datetime.utcnow()}).eq("user_id", user["user_id"]).execute()

        # 4️⃣ Return role and identity
        return {
            "success": True,
            "user_id": user["user_id"],
            "email": user["email"],
            "name": user["name"],
            "role": user["role"]
        }

    except Exception as e:
        return {"success": False, "message": str(e)}

