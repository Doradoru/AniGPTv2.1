import streamlit as st
from utils import login_user, register_user

st.set_page_config(page_title="AniGPT v2.1 Login", page_icon="🧠")

st.title("🧠 AniGPT v2.1 Login Portal")

menu = st.sidebar.selectbox("Menu", ["Login", "Register"])

if menu == "Login":
    st.subheader("🔐 Login to AniGPT")
    uname = st.text_input("Username")
    upass = st.text_input("Password", type='password')

    if st.button("Login"):
        success = login_user(uname, upass)
        if success:
            st.success(f"Welcome back, {uname} 👋")
            st.session_state['user'] = uname
        else:
            st.error("Invalid credentials")

elif menu == "Register":
    st.subheader("📝 Register New User")
    new_user = st.text_input("Create Username")
    new_pass = st.text_input("Create Password", type='password')

    if st.button("Register"):
        registered = register_user(new_user, new_pass)
        if registered:
            st.success("🎉 Registration successful! Please login.")
        else:
            st.warning("⚠️ Username already exists. Try a different one.")
