
import streamlit as st
import gspread
import json
from google.oauth2.service_account import Credentials

st.title("🧠 AniGPT v2.1 Sheet Test")

try:
scope = ["https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive"]

    data = json.loads(st.secrets["GOOGLE_SHEET_JSON"])

    creds = Credentials.from_service_account_info(data, scopes=scope)
    client = gspread.authorize(creds)

    sheet = client.open("AniGPT_DB")  # Sheet name must match
    tabs = [ws.title for ws in sheet.worksheets()]

    st.success("✅ Connected to Google Sheet Successfully!")
    st.write("📄 Available Tabs:", tabs)

except Exception as e:
    st.error("❌ Connection Failed")
    st.exception(e)
