import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import streamlit as st
import json

# Load credentials from Streamlit secrets
data = json.loads(st.secrets["GOOGLE_SHEET_JSON"])

scope = ["https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive"]

creds = Credentials.from_service_account_info(data, scopes=scope)
client = gspread.authorize(creds)

# Open your sheet
sheet = client.open("AniGPT_DB")

def ensure_users_tab():
    try:
        sheet.worksheet("Users")
    except gspread.WorksheetNotFound:
        sheet.add_worksheet(title="Users", rows="100", cols="5")
        ws = sheet.worksheet("Users")
        ws.append_row(["Name", "Password", "CreatedAt"])

def login_user(name, password):
    ensure_users_tab()
    users_ws = sheet.worksheet("Users")
    users = users_ws.get_all_records()
    for user in users:
        if not isinstance(user, dict):   # कठोर चेक
            continue
        u_name = user.get("Name", "").strip().lower()
        u_pass = user.get("Password", "").strip()
        if u_name == name.strip().lower() and u_pass == password.strip():
            return True
    return False

def register_user(name, password):
    ensure_users_tab()
    users_ws = sheet.worksheet("Users")
    users = users_ws.get_all_records()
    for user in users:
        if not isinstance(user, dict):   # कठोर चेक
            continue
        if user.get("Name", "").strip().lower() == name.strip().lower():
            return False  # already exists

    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    users_ws.append_row([name.strip(), password.strip(), created_at])
    return True
