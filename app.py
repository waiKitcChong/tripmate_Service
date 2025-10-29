# app.py
from flask import Flask,jsonify
from flask_cors import CORS
from views.user_routes import user_routes
from controllers.data_controller import fetch_all_data


app = Flask(__name__)
CORS(app)

@app.route("/get_all_data", methods=["GET"])
def get_all_data():
    """
    API endpoint to fetch all Supabase tables.
    """
    data = fetch_all_data()
    return jsonify(data)

app.register_blueprint(user_routes, url_prefix="/api/user")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
