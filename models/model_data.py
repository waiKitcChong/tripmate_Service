from models.db import supabase

def get_all_tables():
    """
    Retrieve all data from Supabase tables.
    Returns a dictionary with table names as keys and their data as values.
    """
    tables = ["users", "orders", "order_details", "payments"]
    data = {}

    for table in tables:
        try:
            result = supabase.table(table).select("*").execute()
            data[table] = result.data
        except Exception as e:
            data[table] = {"error": str(e)}

    return data
