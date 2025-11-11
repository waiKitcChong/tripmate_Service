# models/user_model.py
from models.db import supabase
from datetime import datetime, timezone, timedelta
from werkzeug.security import check_password_hash
import re

# =========================================================================
# ID Generation Logic
# =========================================================================

def get_next_user_id():
    """
    Fetches the highest current user_id (e.g., 'UU999') and calculates the next one.
    Returns: The next user ID string (e.g., 'UU1000').
    """
    try:
        # Fetch the latest user_id that starts with 'UU'
        # We order by user_id string descending and limit to 1.
        response = supabase.table('User').select('user_id').like('user_id', 'UU%').order('user_id', desc=True).limit(1).execute()
        
        data = response.data
        latest_id = data[0]['user_id'] if data else None

        if latest_id and latest_id.startswith('UU'):
            # Use regex to safely extract the numeric part
            match = re.match(r'^UU(\d+)$', latest_id)
            if match:
                num_part = match.group(1)
                current_number = int(num_part)
                next_number = current_number + 1
                
                # Maintain the padding length, or expand if necessary
                padding_length = len(num_part)
                new_padding = max(len(str(next_number)), padding_length)
                
                next_id_num_str = str(next_number).zfill(new_padding)
                return f"UU{next_id_num_str}"
        
        # Fallback if no valid UU ID is found or if the table is empty
        return "UU0001" 

    except Exception as e:
        print(f"Error generating next user ID: {e}")
        return "UU0001" 

# =========================================================================
# CRUD Operations
# =========================================================================

def find_user_by_email(email):
    """
    Finds a user by email.
    Returns: A dictionary of user data or None.
    """
    try:
        # Supabase uses 'eq' for WHERE column = value
        response = supabase.table('User').select('*').eq('email', email).limit(1).execute()
        user_data = response.data
        return user_data[0] if user_data else None
    except Exception as e:
        print(f"Error finding user by email: {e}")
        return None

def insert_new_user(name, email, password_hash):
    """
    Inserts a new user record with unverified status using the custom incremented ID.
    Returns: The inserted user_id or None on failure.
    """
    user_id = get_next_user_id()

    if not user_id or not user_id.startswith('UU'):
         return None # ID generation failed
         
    # Use timezone-aware datetime for Postgres timestamp with time zone
    now = datetime.now(timezone.utc).isoformat()
    
    new_user_data = {
        "user_id": user_id,
        "created_at": now,
        "role": 'user',
        "email": email,
        "name": name,
        "password": password_hash,
        "status": 'unverified',
        "login_attempts": 0
    }
    
    try:
        response = supabase.table('User').insert(new_user_data).execute()
        
        if response.data:
            return user_id
        else:
            print("Supabase insert returned no data.")
            return None
            
    except Exception as e:
        print(f"Supabase Insert failed: {e}")
        return None

def update_user_otp(email, otp, expiry_time):
    """
    Stores the new OTP (in 'reset_token') and its expiry time for the user.
    """
    try:
        response = supabase.table('User').update({
            'reset_token': otp,
            'token_expiry': expiry_time.isoformat()
        }).eq('email', email).execute()
        
        return response.data
        
    except Exception as e:
        print(f"Error updating OTP: {e}")
        return None

def verify_user_otp(email, otp):
    """
    Checks if the given OTP matches the one stored for the email and verifies the user.
    Returns: True if verified and updated, False otherwise.
    """
    user = find_user_by_email(email)
    if not user:
        return False

    # Check OTP and expiry
    is_otp_match = (user.get('reset_token') == otp)
    
    token_expiry_str = user.get('token_expiry')
    if not token_expiry_str:
        return False
        
    try:
        # Convert stored ISO string back to datetime object (must be timezone-aware)
        # Using a simplified conversion here, assuming ISO format from DB matches Python's output
        token_expiry = datetime.fromisoformat(token_expiry_str.replace('Z', '+00:00')) if 'Z' in token_expiry_str else datetime.fromisoformat(token_expiry_str)
        
        # Ensure comparison is with timezone-aware current time
        is_not_expired = (datetime.now(timezone.utc) < token_expiry)
    except ValueError:
        print("Error parsing token_expiry time.")
        is_not_expired = False


    if is_otp_match and is_not_expired:
        try:
            # Update status to 'verified' and clear OTP/expiry fields
            supabase.table('User').update({
                'status': 'verified',
                'reset_token': None,
                'token_expiry': None,
            }).eq('email', email).execute()
            return True
        except Exception as e:
            print(f"Error activating user: {e}")
            return False

    return False

def verify_user(email, password):
    """
    Verifies user login credentials.
    """
    user = find_user_by_email(email)
    if user and check_password_hash(user['password'], password):
        if user['status'] != 'verified':
             return {"success": False, "message": "Account not verified. Please check your email for the verification code."}
        
        # Update last_login time
        try:
             supabase.table('User').update({'last_login': datetime.now(timezone.utc).isoformat()}).eq('user_id', user['user_id']).execute()
        except Exception as e:
             print(f"Failed to update last login: {e}")

        return {
            "success": True, 
            "role": user['role'], 
            "user_id": user['user_id'], 
            "name": user['name']
        }
    return {"success": False, "message": "Invalid email or password"}