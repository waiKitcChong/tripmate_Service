from flask import Blueprint
from controllers.payment_controller import create_payment_intent

payment_routes = Blueprint("payment_routes", __name__)

@payment_routes.route("/create-payment-intent", methods=["POST"])
def handle_create_payment_intent():
    return create_payment_intent()
