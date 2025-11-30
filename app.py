from flask import Flask, jsonify, request
from flask_cors import CORS
from views.user_routes import user_routes
import firebase_admin
from firebase_admin import credentials, messaging
import os
import traceback

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# ====== BLUEPRINT ======
app.register_blueprint(user_routes, url_prefix="/api/user")

# ====== FIREBASE ADMIN SETUP ======
cred = credentials.Certificate("serviceAccount.json")
firebase_admin.initialize_app(cred)

# ====== NOTIFICATION ROUTE ======
@app.route("/send-notification", methods=["POST"])
def send_notification():
    try:
        data = request.get_json()
        receiver_id = data.get("receiverId")
        sender_id = data.get("senderId")
        sender_name = data.get("senderName")
        message = data.get("message")
        chat_type = data.get("chatType")
        chat_id = data.get("chatId")

        topic = f"user_{receiver_id}" if receiver_id else f"group_{chat_id}"

        notification = messaging.Message(
            notification=messaging.Notification(
                title=sender_name,
                body=(message[:50] + "...") if len(message) > 50 else message
            ),
            data={
                "senderId": sender_id,
                "senderName": sender_name,
                "chatType": chat_type,
                "chatId": chat_id,
                "click_action": "FLUTTER_NOTIFICATION_CLICK"
            },
            topic=topic
        )

        response = messaging.send(notification)
        return jsonify({"success": True, "response": response})

    except Exception as e:
        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)}), 500

# ====== RUN APP ======
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
