# models/user_model.py
from models.db import supabase
from werkzeug.security import check_password_hash
from datetime import datetime

def verify_user(email, password):
    try:
        response = supabase.table("User").select("*").eq("email", email).execute()

        if not response.data or len(response.data) == 0:
            return {"success": False, "message": "User not found"}

        user = response.data[0]

        # Password check
        # if not check_password_hash(user["password"], password):
        if user["password"] != password:
            return {"success": False, "message": "Invalid password"}

        # Update last login
        supabase.table("User").update({"last_login": datetime.utcnow()}).eq("user_id", user["user_id"]).execute()

        # Convert datetime fields to string safely
        if "created_at" in user and isinstance(user["created_at"], datetime):
            user["created_at"] = user["created_at"].isoformat()
        if "last_login" in user and isinstance(user["last_login"], datetime):
            user["last_login"] = user["last_login"].isoformat()

        return {
            "success": True,
            "user_id": user["user_id"],
            "email": user["email"],
            "name": user["name"],
            "role": user["role"]
        }

    except Exception as e:
        return {"success": False, "message": str(e)}


