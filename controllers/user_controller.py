# controllers/user_controller.py
from models.user_model import verify_user

def login_user(email, password):
    result = verify_user(email, password)
    return result

