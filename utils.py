import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import streamlit as st
import json

# Load credentials from Streamlit secrets
data = json.loads(st.secrets["GOOGLE_SHEET_JSON"])

scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_info(data, scopes=scope)
client = gspread.authorize(creds)
sheet = client.open("AniGPT_DB")  # ✅ Sheet name

# Ensure Users tab exists
def ensure_users_tab():
    try:
        sheet.worksheet("Users")
    except gspread.WorksheetNotFound:
        sheet.add_worksheet(title="Users", rows="100", cols="5")
        ws = sheet.worksheet("Users")
        ws.append_row(["Name", "Password", "CreatedAt"])

# Login
def login_user(name, password):
    ensure_users_tab()
    users_ws = sheet.worksheet("Users")
    users = users_ws.get_all_records()
    for user in users:
        if not isinstance(user, dict):
            continue
        if not user.get("Name") or not user.get("Password"):
            continue
        if str(user["Name"]).strip().lower() == name.strip().lower() and str(user["Password"]).strip() == password.strip():
            return True
    return False

# Register
def register_user(name, password):
    ensure_users_tab()
    users_ws = sheet.worksheet("Users")
    users = users_ws.get_all_records()
    for user in users:
        if not isinstance(user, dict):
            continue
        if str(user.get("Name", "")).strip().lower() == name.strip().lower():
            return False
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    users_ws.append_row([name.strip(), password.strip(), created_at])
    return True
