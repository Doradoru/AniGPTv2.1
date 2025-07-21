import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import streamlit as st
import json

# Load credentials from Streamlit secrets
data = json.loads(st.secrets["GOOGLE_SHEET_JSON"])
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]
creds = Credentials.from_service_account_info(data, scopes=SCOPES)
client = gspread.authorize(creds)

# Open sheet by name (ensure correctly shared!)
# Alternatively, open by key for more reliability:
# sheet = client.open_by_key("YOUR_SHEET_ID")
sheet = client.open("AniGPT_DB")

def ensure_users_tab():
    try:
        sheet.worksheet("Users")
    except gspread.exceptions.WorksheetNotFound:  # precise exception
        ws = sheet.add_worksheet(title="Users", rows="100", cols="3")
        ws.append_row(["Name", "Password", "CreatedAt"])

def login_user(name, password):
    ensure_users_tab()
    if not name or not password:
        return False
    ws = sheet.worksheet("Users")
    users = ws.get_all_records()
    name = name.strip().lower()
    password = password.strip()
    for user in users:
        if not isinstance(user, dict):
            continue
        # Safe get and compare, lowercased user name
        if str(user.get("Name", "")).strip().lower() == name and \
           str(user.get("Password", "")).strip() == password:
            return True
    return False

def register_user(name, password):
    ensure_users_tab()
    if not name or not password:
        return False
    ws = sheet.worksheet("Users")
    users = ws.get_all_records()
    name_clean = name.strip()
    for user in users:
        if not isinstance(user, dict):
            continue
        if str(user.get("Name", "")).strip().lower() == name_clean.lower():
            return False  # User exists!
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ws.append_row([name_clean, password.strip(), created_at])
    return True
