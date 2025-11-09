# controllers/payment_controller.py
from flask import jsonify, request
import stripe
import os
from dotenv import load_dotenv

load_dotenv()  # Load STRIPE keys from .env file

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")


def create_payment_intent():
    """Create Stripe payment intent and return client secret"""
    try:
        data = request.get_json()
        amount = int(data.get("amount", 0))  # amount in cents
        currency = data.get("currency", "usd")

        if amount <= 0:
            return jsonify({"error": "Invalid payment amount"}), 400

        # Create payment intent
        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency=currency,
            payment_method_types=["card"],
        )

        return jsonify({
            "clientSecret": intent.client_secret,
            "amount": amount,
            "currency": currency
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def generate_receipt():
    """Generate simple payment receipt (for demo)"""
    try:
        data = request.get_json()
        user = data.get("user", "Unknown User")
        amount = data.get("amount")
        currency = data.get("currency", "usd")
        status = data.get("status", "succeeded")

        receipt = {
            "receipt_id": f"RCPT_{os.urandom(4).hex().upper()}",
            "user": user,
            "amount": amount,
            "currency": currency,
            "status": status,
            "message": "Payment successful! Thank you for your purchase."
        }
        return jsonify(receipt), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
