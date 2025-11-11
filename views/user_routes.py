# views/user_routes.py
from flask import Blueprint, request, jsonify
from controllers.user_controller import login_user
from controllers.register_controller import register_user, resend_otp, verify_user_otp # NEW
from flask_cors import cross_origin

user_routes = Blueprint("user_routes", __name__)

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

    # Return user role to PHP frontend
    return jsonify({
        "success": True,
        "role": result["role"],
        "user_id": result["user_id"],
        "name": result["name"]
    }), 200


# NEW: Registration Route
@user_routes.route("/register", methods=["POST"])
@cross_origin()
def register():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return jsonify({"success": False, "message": "Missing required fields"}), 400
        
    result, status_code = register_user(name, email, password)
    return jsonify(result), status_code


# NEW: Send OTP Route (Used for Resend)
@user_routes.route("/send_otp", methods=["POST"])
@cross_origin()
def send_otp():
    data = request.get_json()
    email = data.get("email")
    
    if not email:
        return jsonify({"success": False, "message": "Missing email field"}), 400
        
    result, status_code = resend_otp(email)
    return jsonify(result), status_code


# NEW: Verify OTP Route
@user_routes.route("/verify_otp", methods=["POST"])
@cross_origin()
def verify_otp():
    data = request.get_json()
    email = data.get("email")
    otp = data.get("otp")
    
    if not email or not otp:
        return jsonify({"success": False, "message": "Missing email or OTP field"}), 400
        
    result, status_code = verify_user_otp(email, otp)
    return jsonify(result), status_code