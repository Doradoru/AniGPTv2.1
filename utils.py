
import json
import streamlit as st
import gspread
from datetime import datetime
from google.oauth2.service_account import Credentials

# Load credentials from Streamlit secrets
scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
data = json.loads(st.secrets["GOOGLE_SHEET_JSON"])
creds = Credentials.from_service_account_info(data, scopes=scope)
client = gspread.authorize(creds)
sheet = client.open("AniGPT_DB")  # ✅ Make sure this name matches your Google Sheet

# 🔐 Ensure 'Users' tab exists
def ensure_users_tab():
    try:
        sheet.worksheet("Users")
    except gspread.exceptions.WorksheetNotFound:
        sheet.add_worksheet(title="Users", rows="100", cols="3")
        sheet.worksheet("Users").append_row(["Name", "Password", "CreatedAt"])

# ✅ Register user
def register_user(name, password):
    ensure_users_tab()
    users_ws = sheet.worksheet("Users")
    users = users_ws.get_all_records()
    
    for user in users:
        if user["Name"] == name:
            return False  # Already exists
    
    users_ws.append_row([name, password, datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
    return True

# ✅ Login user
def login_user(name, password):
    ensure_users_tab()
    users_ws = sheet.worksheet("Users")
    users = users_ws.get_all_records()
    
    for user in users:
        if user["Name"] == name and user["Password"] == password:
            return True
    return False
