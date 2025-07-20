### ✅ FILE: app.py (Main Login/Register)

import streamlit as st
from utils import login_user, register_user

st.set_page_config(page_title="AniGPT Login", page_icon="🧠")
st.title("🧠 AniGPT v2.1 Login")

menu = ["Login", "Register"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Login":
    st.subheader("Login to your Account")
    uname = st.text_input("Username")
    upass = st.text_input("Password", type='password')
    if st.button("Login"):
        if login_user(uname, upass):
            st.session_state['user'] = uname
            st.success(f"Welcome back, {uname} 👋")
            st.switch_page("pages/dashboard.py")
        else:
            st.error("Incorrect Username or Password")

elif choice == "Register":
    st.subheader("Create New Account")
    new_user = st.text_input("Choose a Username")
    new_pass = st.text_input("Choose a Password", type='password')
    if st.button("Register"):
        if register_user(new_user, new_pass):
            st.success("Account created successfully. Now login.")
        else:
            st.warning("Username already exists. Try a different one.")
