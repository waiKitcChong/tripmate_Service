from flask import request, jsonify
from models.model_data import get_all_tables
from models.db import supabase

def fetch_all_data():
    return get_all_tables()

def insert_record(table):
    data = request.get_json() 
    result = supabase.table(table).insert(data).execute()
    return jsonify(result.data), 200

def update_record(table, record_id):
    data = request.get_json()
    result = supabase.table(table).update(data).eq("id", record_id).execute()
    return jsonify(result.data), 200

def delete_record(table, record_id):
    result = supabase.table(table).delete().eq("id", record_id).execute()
    return jsonify({"deleted": result.data}), 200
