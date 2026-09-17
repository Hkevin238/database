import os
from supabase import create_client, Client

# Gufata Credentials za Supabase muri Environment Variables cyangwa kuzishyiramo aho uzikoresha
SUPABASE_URL = os.environ.get("SUPABASE_URL", "YOUR_SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "YOUR_SUPABASE_ANON_KEY")

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

def load_chat_history(username: str) -> list:
    """Gukurura amateka y'ibiganiro by'umukoresha runaka"""
    response = supabase.table("chats").select("role, content, show_image").eq("username", username).order("id", desc=False).execute()
    
    messages = []
    for row in response.data:
        messages.append({
            "role": row["role"],
            "content": row["content"],
            "show_image": bool(row["show_image"])
        })
    return messages

def save_message_to_db(username: str, role: str, content: str, show_image: bool = False):
    """Kubika ubutumwa bushya bw'umukoresha cyangwa bwa AI"""
    try:
        supabase.table("chats").insert({
            "username": username,
            "role": role,
            "content": content,
            "show_image": show_image
        }).execute()
    except Exception as e:
        print(f"Error saving message: {e}")

def clear_chat_history(username: str):
    """Gusiba amateka y'ibiganiro by'umukoresha"""
    try:
        supabase.table("chats").delete().eq("username", username).execute()
    except Exception as e:
        print(f"Error clearing history: {e}")