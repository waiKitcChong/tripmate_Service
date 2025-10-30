from flask import request, jsonify
from models.model_data import get_all_tables
from models.db import supabase

# === Define your table-to-primary-key mapping ===
PRIMARY_KEYS = {
    "User": "user_id",
    "Tourist": "tourist_id",
    "Business_Owner": "business_owner_id",
    "Business_Staff": "staff_id",
    "Business": "business_id",
    "Hotel": "hotel_id",
    "Room": "room_id",
    "RoomType": "roomtype_id",
    "Restaurant": "restaurant_id",
    "TripPlan": "tripplan_id",
    "Booking": "booking_id",
    "Promotion": "promotion_id",
    "Comments": "comment_id",
    "SubComments": "subcomment_id",
    # Add all other tables here
}


# === READ ===
def fetch_all_data():
    """Fetch all table data."""
    return get_all_tables()


# === CREATE ===
def insert_record(table):
    try:
        data = request.get_json()
        result = supabase.table(table).insert(data).execute()
        return jsonify({"status": "success", "data": result.data}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# === UPDATE ===
def update_record(table, record_id):
    try:
        data = request.get_json()

        # Find the correct primary key for the given table
        pk = PRIMARY_KEYS.get(table)
        if not pk:
            return jsonify({"status": "error", "message": f"No primary key mapping for table '{table}'"}), 400

        result = supabase.table(table).update(data).eq(pk, record_id).execute()
        return jsonify({"status": "success", "data": result.data}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# === DELETE ===
def delete_record(table, record_id):
    try:
        pk = PRIMARY_KEYS.get(table)
        if not pk:
            return jsonify({"status": "error", "message": f"No primary key mapping for table '{table}'"}), 400

        result = supabase.table(table).delete().eq(pk, record_id).execute()
        return jsonify({"status": "success", "deleted": result.data}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
