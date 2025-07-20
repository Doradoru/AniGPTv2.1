import streamlit as st
from utils import login_user, register_user

st.set_page_config(page_title="AniGPT v2.1 Login", page_icon="🧠")

st.title("🧠 AniGPT v2.1 Login Portal")

menu = ["Login", "Register"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Login":
    st.subheader("🔐 Login to AniGPT")

    uname = st.text_input("Username")
    upass = st.text_input("Password", type='password')

    if st.button("Login"):
        if login_user(uname, upass):
            st.success(f"Welcome {uname} 👋")
            st.info("Now you can start using AniGPT...")
        else:
            st.error("Invalid credentials")

elif choice == "Register":
    st.subheader("📝 Create New Account")

    new_user = st.text_input("New Username")
    new_pass = st.text_input("New Password", type='password')

    if st.button("Register"):
        if register_user(new_user, new_pass):
            st.success("Account created successfully!")
        else:
            st.warning("Username already exists!")
