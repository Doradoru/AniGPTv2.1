import streamlit as st
from utils import login_user, register_user

st.set_page_config(page_title="AniGPT Login", page_icon="🧠")

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = ""

st.title("🧠 AniGPT v2.1 Login System")

# If not logged in
if not st.session_state.logged_in:
    st.markdown("### 👤 Login or Create Account")

    menu = ["Login", "Register"]
    choice = st.selectbox("Select Action", menu)

    uname = st.text_input("Username")
    upass = st.text_input("Password", type="password")

    if choice == "Login":
        if st.button("Login"):
            if login_user(uname, upass):
                st.session_state.logged_in = True
                st.session_state.user = uname
                st.success(f"Welcome back, {uname} 👋")
                st.rerun()
            else:
                st.error("Login Failed. Please check your credentials.")

    elif choice == "Register":
        if st.button("Register"):
            if register_user(uname, upass):
                st.success("Registration Successful! Now you can login.")
            else:
                st.warning("User already exists. Please try a different name.")

# If already logged in
else:
    st.success(f"🟢 Logged in as {st.session_state.user}")
    st.markdown("### 🎯 What do you want to do today?")
    st.write("✅ Mood log, 📝 Journal, 📚 Learnings, 🗓️ Goals — coming soon...")

    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.user = ""
        st.rerun()
