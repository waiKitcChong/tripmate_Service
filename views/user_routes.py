# views/user_routes.py
from flask import Blueprint, request, jsonify
from controllers.user_controller import login_user, register_user, verify_otp_and_activate
from flask_cors import cross_origin
import re

user_routes = Blueprint("user_routes", __name__)

# Basic Email Validation Helper
def is_valid_email(email):
    # Simple regex for email format
    return re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email)

@user_routes.route("/login", methods=["POST"])
@cross_origin()
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"success": False, "message": "Missing fields"}), 400

    result = login_user(email, password)

    if not result["success"]:
        return jsonify(result), 401

    return jsonify({
        "success": True,
        "role": result["role"],
        "user_id": result["user_id"],
        "name": result["name"]
    }), 200

# ====== New Register Route ======
@user_routes.route("/register", methods=["POST"])
@cross_origin()
def register():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return jsonify({"success": False, "message": "Missing required fields."}), 400

    if not is_valid_email(email):
        return jsonify({"success": False, "message": "Invalid email format."}), 400

    # Minimal password length check
    if len(password) < 6:
        return jsonify({"success": False, "message": "Password must be at least 6 characters long."}), 400

    # Call controller for registration and OTP sending
    result = register_user(name, email, password)

    if result["success"]:
        # HTTP 202 Accepted - Registration initiated, verification required
        return jsonify(result), 202 
    else:
        # Check for specific error message for HTTP status code handling
        status_code = 409 if "already registered" in result.get("message", "").lower() else 500
        return jsonify(result), status_code

# ====== New OTP Verification Route ======
@user_routes.route("/verify_otp", methods=["POST"])
@cross_origin()
def verify_otp():
    data = request.get_json()
    email = data.get("email")
    otp = data.get("otp")

    if not email or not otp:
        return jsonify({"success": False, "message": "Missing email or OTP."}), 400

    if len(otp) != 6 or not otp.isdigit():
        return jsonify({"success": False, "message": "Invalid OTP format. Must be 6 digits."}), 400

    result = verify_otp_and_activate(email, otp)

    if result["success"]:
        return jsonify(result), 200
    else:
        return jsonify(result), 401