from flask import Blueprint, request, jsonify
from controllers.user_controller import login_user
from controllers.account_controller import send_otp_controller, verify_otp_controller
from flask_cors import cross_origin

user_routes = Blueprint("user_routes", __name__)

# Existing login
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


# ===== New Route: Send OTP =====
@user_routes.route("/send_otp", methods=["POST"])
@cross_origin()
def send_otp():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not all([name, email, password]):
        return jsonify({"success": False, "message": "Missing required fields"}), 400

    result = send_otp_controller(name, email, password)
    return jsonify(result), 200 if result["success"] else 400


# ===== New Route: Verify OTP =====
@user_routes.route("/verify_otp", methods=["POST"])
@cross_origin()
def verify_otp():
    data = request.get_json()
    email = data.get("email")
    otp = data.get("otp")

    if not all([email, otp]):
        return jsonify({"success": False, "message": "Missing fields"}), 400

    result = verify_otp_controller(email, otp)
    return jsonify(result), 200 if result["success"] else 400
