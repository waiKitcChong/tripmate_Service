# controllers/payment_controller.py
import os
import stripe
from flask import jsonify, request

stripe.api_key = os.getenv("STRIPE_SECRET_KEY") 

def create_payment_intent():
    try:
        data = request.get_json()
        amount = data.get("amount", 1000)
        currency = data.get("currency", "myr")

        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency=currency,
            automatic_payment_methods={"enabled": True},
        )

        return jsonify({
            "client_secret": intent.client_secret,
            "amount": amount,
            "currency": currency
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400
