# models/register_model.py
from datetime import datetime, timezone, timedelta
from werkzeug.security import generate_password_hash
import random

# Import the pre-initialized Supabase client
from models.db import supabase 

# --- Helper Functions ---

def _generate_unique_user_id():
    """Generates an incremented user ID (e.g., UU001, UU002)."""
    # Assuming supabase client is successfully initialized in models/db.py
    if not supabase: 
        print("WARNING: Supabase client is not available in register_model.")
        # Fallback ID for testing when not connected
        return f"UU{int(random.random() * 1000):03d}"

    try:
        # Get the highest current user_id
        # Note: 'User' is case-sensitive if you enclosed it in quotes in PostgreSQL
        response = supabase.table('User').select('user_id').order('user_id', desc=True).limit(1).execute()
        
        latest_id = response.data[0]['user_id'] if response.data else None

        if latest_id:
            # Assumes format is UUXXX where XXX is a number
            number = int(latest_id[2:])
            new_number = number + 1
            new_id = f"UU{new_number:03d}"
        else:
            new_id = "UU001"
        
        return new_id
    except Exception as e:
        print(f"Error generating User ID: {e}")
        return f"UU{int(random.random() * 10000):05d}" # Fallback to a larger random number


def _generate_otp():
    """Generates a 6-digit numeric OTP."""
    return str(random.randint(100000, 999999))

# --- Core Functions ---

def check_email_exists(email):
    """Checks if a user with the given email already exists."""
    if not supabase: return False

    try:
        response = supabase.table('User').select('user_id').eq('email', email).execute()
        # Checks if any record exists, regardless of status (Active/Pending)
        return len(response.data) > 0
    except Exception as e:
        print(f"Error checking email: {e}")
        return False


def register_pending_user(name, email, raw_password):
    """Creates a temporary pending user record with an OTP."""
    if not supabase: 
        return {"success": False, "message": "Database client not available."}

    user_id = _generate_unique_user_id()
    otp = _generate_otp()
    otp_expiry = datetime.now(timezone.utc) + timedelta(minutes=10) # OTP valid for 10 minutes

    try:
        data = {
            'user_id': user_id,
            'created_at': datetime.now(timezone.utc).isoformat(),
            'role': 'User', # Default role
            'email': email,
            'name': name,
            'password': raw_password, # Temporarily store raw password
            'status': 'Pending',
            'login_attempts': 0,
            'reset_token': otp,        # Use reset_token to store OTP
            'token_expiry': otp_expiry.isoformat(),
        }

        # Check for existing pending user and update instead of inserting
        response = supabase.table('User').select('user_id, password').eq('email', email).eq('status', 'Pending').execute()
        
        if response.data:
            # Update existing pending user (for resend/retry)
            update_data = {
                'reset_token': otp, 
                'token_expiry': otp_expiry.isoformat(),
                'password': raw_password, # Update password/name in case user changed inputs on register page
                'name': name
            }
            update_response = supabase.table('User').update(update_data).eq('email', email).execute()
            if update_response.data:
                return {"success": True, "message": "Pending user updated.", "otp": otp, "user_id": response.data[0]['user_id']}
            else:
                raise Exception("Failed to update pending user.")

        else:
            # Insert new user
            insert_response = supabase.table('User').insert(data).execute()
            if insert_response.data:
                return {"success": True, "message": "New pending user created.", "otp": otp, "user_id": user_id}
            else:
                raise Exception("Failed to insert new user.")

    except Exception as e:
        print(f"Error in register_pending_user: {e}")
        return {"success": False, "message": f"Database error: {e}"}


def verify_and_activate_user(email, otp):
    """Verifies the OTP and activates the user account by hashing the password."""
    if not supabase: 
        return {"success": False, "message": "Database client not available."}

    try:
        # 1. Fetch the pending user record
        response = supabase.table('User').select('*').eq('email', email).eq('status', 'Pending').execute()
        
        if not response.data:
            return {"success": False, "message": "Account not found or already verified."}

        user_data = response.data[0]
        
        stored_otp = user_data.get('reset_token')
        expiry_str = user_data.get('token_expiry')
        raw_password = user_data.get('password') # Retrieve temporarily stored raw password

        if stored_otp is None or expiry_str is None:
            return {"success": False, "message": "Verification token missing."}

        # 2. Check expiry
        expiry_time = datetime.fromisoformat(expiry_str.replace('Z', '+00:00'))
        if datetime.now(timezone.utc) > expiry_time:
            return {"success": False, "message": "OTP expired. Please request a new one."}

        # 3. Check OTP match
        if otp != stored_otp:
            return {"success": False, "message": "Invalid OTP provided."}

        # 4. Activate account: Hash password and update status
        hashed_password = generate_password_hash(raw_password)
        
        update_data = {
            'password': hashed_password,
            'status': 'Active',
            'reset_token': None, # Clear OTP
            'token_expiry': None, # Clear expiry
            'last_login': datetime.now(timezone.utc).isoformat(),
        }

        update_response = supabase.table('User').update(update_data).eq('user_id', user_data['user_id']).execute()

        if update_response.data:
            return {"success": True, "message": "Account successfully verified and activated."}
        else:
            return {"success": False, "message": "Failed to activate account."}

    except Exception as e:
        print(f"Error in verify_and_activate_user: {e}")
        return {"success": False, "message": f"Database error: {e}"}