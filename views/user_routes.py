# views/user_routes.py
from flask import Blueprint, request, jsonify
from controllers.user_controller import login_user
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

