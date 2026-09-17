import os
import streamlit as st
from supabase import create_client, Client

# Gufata Credentials za Supabasehera muri Streamlit Secrets, hanyuma os.environ, cyangwa izo washyizemo
SUPABASE_URL = st.secrets.get("SUPABASE_URL") or os.environ.get("SUPABASE_URL", "https://frgxfkhsnfnmrxipzsdz.supabase.co")
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY") or os.environ.get("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZyZ3hma2hzbmZubXJ4aXB6c2R6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODk2Mjk4NDgsImV4cCI6MjEwNTIwNTg0OH0.khu7VPoRSW8pxcxOn8ZdjXj5J7dq060Z1M4oyOtBa6M")

# Guhuza na Supabase Client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# =========================================================
# 1. USERS FUNCTIONS (Kwiyandikisha no Kwinjira)
# =========================================================

def check_user_exists(username: str) -> bool:
    """Reba niba izina ry'ukoresha risanzwe muri Supabase"""
    response = supabase.table("users").select("*").eq("username", username).execute()
    return len(response.data) > 0

def create_user(username: str, password: str) -> bool:
    """Kwiyandikisha kwinjira muri database"""
    try:
        supabase.table("users").insert({"username": username, "password": password}).execute()
        return True
    except Exception as e:
        print(f"Error creating user: {e}")
        return False

def verify_user(username: str, password: str) -> bool:
    """Kwemeza niba ijambo ry'ibanga ari ryo"""
    response = supabase.table("users").select("password").eq("username", username).execute()
    if response.data:
        return response.data[0]["password"] == password
    return False


# =========================================================
# 2. CHAT HISTORY FUNCTIONS (Amateka y'Ibiganiro)
# =========================================================

def load_chat_history(username: str, session_id: str = "Main Chat") -> list:
    """Gukurura amateka y'ibiganiro by'umukoresha runaka"""
    try:
        response = supabase.table("chats_history").select("role, content, show_image").eq("username", username).order("id", desc=False).execute()
        
        messages = []
        if response.data:
            for row in response.data:
                messages.append({
                    "role": row["role"],
                    "content": row["content"],
                    "show_image": bool(row["show_image"])
                })
        return messages
    except Exception as e:
        print(f"Error loading history: {e}")
        return []

def save_message_to_db(username: str, session_id: str, role: str, content: str, show_image: bool = False):
    """Kubika ubutumwa bushya bw'umukoresha cyangwa bwa AI"""
    try:
        supabase.table("chats_history").insert({
            "username": username,
            "session_id": session_id,
            "role": role,
            "content": content,
            "show_image": show_image
        }).execute()
    except Exception as e:
        print(f"Error saving message: {e}")

def clear_chat_history(username: str):
    """Gusiba amateka y'ibiganiro by'umukoresha"""
    try:
        supabase.table("chats_history").delete().eq("username", username).execute()
    except Exception as e:
        print(f"Error clearing history: {e}")
