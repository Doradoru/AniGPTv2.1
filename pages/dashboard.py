import streamlit as st
import speech_recognition as sr
from datetime import datetime
import gspread
import json
from google.oauth2.service_account import Credentials

# Load creds
data = json.loads(st.secrets["GOOGLE_SHEET_JSON"])
scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_info(data, scopes=scope)
client = gspread.authorize(creds)
sheet = client.open("AniGPT_DB")

# Ensure Tabs
required_tabs = {
    "Mood logs": ["Date", "Mood", "Trigger"],
    "Daily journal": ["Date", "Summary", "Keywords"],
    "Learning": ["Date", "WhatWasLearned", "Context"],
    "Reminders": ["Task", "Date", "Time", "Status"],
    "Memory": ["Date", "Detail"],
    "Life goals": ["Goal", "Category", "Target Date", "Progress"],
    "Voice logs": ["Date", "Transcript", "Emotion"],
    "Anibook outline": ["Chapter", "Idea", "Importance"],
    "Improvement notes": ["Date", "Area", "Improvement"],
    "Quotes": ["Quote", "Author"],
    "User facts": ["Fact", "Context"],
    "Task done": ["Task", "Date"],
    "Auto backup logs": ["Date", "Data type", "Summary"],
}

def ensure_tabs():
    existing_tabs = [ws.title for ws in sheet.worksheets()]
    for tab, headers in required_tabs.items():
        if tab not in existing_tabs:
            ws = sheet.add_worksheet(title=tab, rows="100", cols="10")
            ws.append_row(headers)

ensure_tabs()

# Detect intent
def detect_intent(text):
    text = text.lower()
    if any(x in text for x in ["happy", "sad", "angry", "mood"]):
        return "Mood logs"
    elif "learn" in text:
        return "Learning"
    elif "journal" in text or "today was" in text:
        return "Daily journal"
    elif "remind" in text or "task" in text:
        return "Reminders"
    elif "goal" in text:
        return "Life goals"
    elif "quote" in text:
        return "Quotes"
    elif "improve" in text:
        return "Improvement notes"
    elif "fact" in text:
        return "User facts"
    elif "done" in text:
        return "Task done"
    else:
        return "Memory"

# Save data
def save_to_sheet(intent, user_input):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ws = sheet.worksheet(intent)

    if intent == "Mood logs":
        ws.append_row([now, "Auto", user_input])
    elif intent == "Learning":
        ws.append_row([now, user_input, "Context Unknown"])
    elif intent == "Daily journal":
        ws.append_row([now, user_input, "Keywords TBD"])
    elif intent == "Reminders":
        ws.append_row([user_input, now.split()[0], now.split()[1], "Pending"])
    elif intent == "Quotes":
        ws.append_row([user_input, "Unknown"])
    elif intent == "Life goals":
        ws.append_row([user_input, "General", "TBD", "0%"])
    elif intent == "Improvement notes":
        ws.append_row([now, "Area TBD", user_input])
    elif intent == "User facts":
        ws.append_row([user_input, "Context TBD"])
    elif intent == "Task done":
        ws.append_row([user_input, now])
    elif intent == "Voice logs":
        ws.append_row([now, user_input, "Unknown"])
    else:
        ws.append_row([now, user_input])

# UI
st.title("🎙️ AniGPT v2.1 with Voice Input")
st.write("Talk or type to AniGPT, and it will save everything smartly.")

user_input = st.text_area("Type here if you prefer:")

# 🎙 Voice input
if st.button("🎤 Speak"):
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        st.info("Listening...")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        st.success(f"You said: {text}")
        detected = detect_intent(text)
        save_to_sheet(detected, text)
        save_to_sheet("Voice logs", text)
        st.success(f"✅ Saved to **{detected}** and Voice logs.")
    except Exception as e:
        st.error("Could not recognize voice. Please try again.")

# Manual input handling
if st.button("📥 Submit"):
    if user_input.strip():
        intent = detect_intent(user_input)
        save_to_sheet(intent, user_input)
        st.success(f"✅ Saved to **{intent}** tab.")
    else:
        st.warning("Please type something before submitting.")
