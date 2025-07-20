import streamlit as st
import gspread
import json
from google.oauth2.service_account import Credentials

data = json.loads(st.secrets["GOOGLE_SHEET_JSON"])

scope = ["https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive"]

creds = Credentials.from_service_account_info(data, scopes=scope)
client = gspread.authorize(creds)

# Try to open your Google Sheet
try:
    sheet = client.open("AniGPT_DB")
    st.success("✅ Connected to AniGPT_DB")
except Exception as e:
    st.error(f"❌ Connection Failed\n\n{e}")
