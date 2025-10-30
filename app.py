from flask import Flask, jsonify
from flask_cors import CORS
from views.user_routes import user_routes
from controllers.data_controller import (
    fetch_all_data,
    insert_record,
    update_record,
    delete_record
)

app = Flask(__name__)
# ✅ This enables CORS correctly in Flask
CORS(app, resources={r"/*": {"origins": "*"}})

# ====== ROUTES ======
@app.route("/get_all_data", methods=["GET"])
def get_all_data():
    data = fetch_all_data()
    return jsonify(data)

@app.route("/insert/<table>", methods=["POST"])
def insert_table(table):
    return insert_record(table)

@app.route("/update/<table>/<record_id>", methods=["PUT"])
def update_table(table, record_id):
    return update_record(table, record_id)

@app.route("/delete/<table>/<record_id>", methods=["DELETE"])
def delete_table(table, record_id):
    return delete_record(table, record_id)

# ====== BLUEPRINT ======
app.register_blueprint(user_routes, url_prefix="/api/user")

# ====== RUN APP ======
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
