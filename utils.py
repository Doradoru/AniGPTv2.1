import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import streamlit as st
import json

# Load credentials from secrets
data = json.loads(st.secrets["GOOGLE_SHEET_JSON"])

scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_info(data, scopes=scope)
client = gspread.authorize(creds)

# Connect to your sheet
sheet = client.open("AniGPT_DB")  # Make sure this matches your sheet name

def ensure_users_tab():
    try:
        sheet.worksheet("Users")
    except gspread.WorksheetNotFound:
        ws = sheet.add_worksheet(title="Users", rows="100", cols="3")
        ws.append_row(["Name", "Password", "CreatedAt"])

def login_user(name, password):
    ensure_users_tab()
    ws = sheet.worksheet("Users")
    users = ws.get_all_records()
    name = name.strip().lower()
    password = password.strip()
    for user in users:
        if not isinstance(user, dict):
            continue
        if str(user.get("Name", "")).strip().lower() == name and str(user.get("Password", "")).strip() == password:
            return True
    return False

def register_user(name, password):
    ensure_users_tab()
    ws = sheet.worksheet("Users")
    users = ws.get_all_records()
    name = name.strip()
    for user in users:
        if not isinstance(user, dict):
            continue
        if str(user.get("Name", "")).strip().lower() == name.lower():
            return False  # already registered
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ws.append_row([name, password.strip(), created_at])
    return True
