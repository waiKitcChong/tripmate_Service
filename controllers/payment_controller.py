import os
from dotenv import load_dotenv
import stripe

load_dotenv()

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

def create_payment_intent(amount):
    payment_intent = stripe.PaymentIntent.create(
        amount=int(amount * 100), 
        currency="myr",
        payment_method_types=["card"],
    )
    return payment_intent.client_secret
