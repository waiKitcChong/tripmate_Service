# controllers/user_controller.py
from models.user_model import verify_user

def login_user(email, password):
    # Existing login function
    result = verify_user(email, password)
    return result