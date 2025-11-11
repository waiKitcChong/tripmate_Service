from flask import Flask, jsonify,request
from flask_cors import CORS
from views.user_routes import user_routes

import traceback


app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})

# ====== BLUEPRINT ======
app.register_blueprint(user_routes, url_prefix="/api/user")
# ====== RUN APP ======
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
