# models/db.py
from supabase import create_client, Client
import os

# You can set these as environment variables in Render dashboard
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://lwismkvrwljapnhckdjz.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "sb_secret_DYnlNj9MqsipFM0Ntm9QLQ_euu5yRb4")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


