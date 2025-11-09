import os
from flask import Blueprint, request, jsonify
import stripe
from dotenv import load_dotenv

load_dotenv()  

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

payment_routes = Blueprint('payment_routes', __name__)

@payment_routes.route("/create-payment-intent", methods=["POST"])
def create_payment_intent():
    try:
        data = request.get_json()
        amount = data.get("amount")
        currency = data.get("currency", "myr").lower()

        if not amount or amount <= 0:
            return jsonify({"error": "Invalid amount"}), 400


        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency=currency,
            automatic_payment_methods={"enabled": True},
        )

        return jsonify({"client_secret": intent.client_secret})
    except Exception as e:
        print("⚠️ PaymentIntent error:", e)
        return jsonify({"error": str(e)}), 400
