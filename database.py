import os
import streamlit as st
from supabase import create_client, Client

# Gufata Credentials za Supabase
SUPABASE_URL = st.secrets.get("SUPABASE_URL") or os.environ.get("SUPABASE_URL", "https://frgxfkhsnfnmrxipzsdz.supabase.co")
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY") or os.environ.get("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def check_user_exists(username: str) -> bool:
    try:
        response = supabase.table("users").select("*").eq("username", username).execute()
        return len(response.data) > 0
    except:
        return False

def create_user(username: str, password: str):
    """Isomeraho ikagarura (success: bool, msg: str)"""
    try:
        if check_user_exists(username):
            return False, "Izina ry'ukoresha risanzwe ryarafashwe!"
        
        supabase.table("users").insert({"username": username, "password": password}).execute()
        return True, "Konti yaremwe neza!"
    except Exception as e:
        return False, str(e)

def verify_user(username: str, password: str):
    """Isomeraho ikagarura (success: bool, msg: str)"""
    try:
        response = supabase.table("users").select("password").eq("username", username).execute()
        if response.data:
            if response.data[0]["password"] == password:
                return True, "Winjiye neza!"
            else:
                return False, "Ijambo ry'ibanga si ryo!"
        return False, "Izina ry'ukoresha ntiribaho!"
    except Exception as e:
        return False, str(e)

def load_chat_history(username: str, session_id: str = "Main Chat") -> list:
    try:
        response = supabase.table("chats_history").select("role, content, show_image").eq("username", username).order("id", desc=False).execute()
        messages = []
        if response.data:
            for row in response.data:
                messages.append({
                    "role": row["role"],
                    "content": row["content"],
                    "show_image": bool(row.get("show_image", False))
                })
        return messages
    except Exception as e:
        print(f"Error loading history: {e}")
        return []

def save_message_to_db(username: str, session_id: str, role: str, content: str, show_image: bool = False):
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
    try:
        supabase.table("chats_history").delete().eq("username", username).execute()
    except Exception as e:
        print(f"Error clearing history: {e}")
