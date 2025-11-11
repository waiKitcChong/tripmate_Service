# views/payment_routes.py
from flask import Blueprint
from controllers.otp_controller import create_payment_intent, generate_receipt

payment_routes = Blueprint("payment_routes", __name__)

@payment_routes.route("/create-intent", methods=["POST"])
def create_intent_route():
    return create_payment_intent()

@payment_routes.route("/generate-receipt", methods=["POST"])
def generate_receipt_route():
    return generate_receipt()
