from models.db import supabase

def get_all_tables():
    """
    Retrieve all data from Supabase tables.
    Returns a dictionary with table names as keys and their data as values.
    """
    tables = [
    "Booking",
    "Business",
    "Bussiness_Owner",
    "Bussiness_Staff",
    "Comments",
    "Community",
    "EmergencySupport",
    "Hotel",
    "HotelBookingDetails",
    "Insurance",
    "Itinerary",
    "Location",
    "Location_Rate",
    "Menu",
    "Promotion",
    "Promotion_Target",
    "RestBookingDetails",
    "Rest_Schedule",
    "Restaurant",
    "Room",
    "RoomType",
    "Room_Schedule",
    "SubComments",
    "TableList",
    "Tag",
    "Tourists",
    "TripPlan",
    "User"
]

    data = {}

    for table in tables:
        try:
            result = supabase.table(table).select("*").execute()
            data[table] = result.data
        except Exception as e:
            data[table] = {"error": str(e)}

    return data
