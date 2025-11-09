from flask import Flask, jsonify,request
from flask_cors import CORS
from views.user_routes import user_routes
from views.payment_routes import payment_routes  
from dotenv import load_dotenv
from controllers.data_controller import (
    fetch_all_data,
    insert_record,
    update_record,
    delete_record
)
import traceback

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})

load_dotenv()  # 讀取 .env 內容
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
    try:
        print("=== Incoming PUT request ===")
        print("Table:", table)
        print("Record ID:", record_id)
        print("Request JSON:", request.get_json())

        #  Don't jsonify again — just return directly
        return update_record(table, record_id)

    except Exception as e:
        print("❌ ERROR in /update route:", str(e))
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

    
@app.route("/delete/<table>/<record_id>", methods=["DELETE"])
def delete_table(table, record_id):
    return delete_record(table, record_id)

# ====== BLUEPRINT ======
app.register_blueprint(user_routes, url_prefix="/api/user")

app.register_blueprint(payment_routes, url_prefix="/api/payment") 
# ====== RUN APP ======
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
