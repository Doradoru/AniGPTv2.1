import streamlit as st
from utils import login_user, register_user

# Set Streamlit Page Title
st.set_page_config(page_title="AniGPT Login", page_icon="🧠")

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = ""

# Main Title
st.markdown("<h1 style='color:#FF4B4B;'>🧠 Welcome to AniGPT v2.1</h1>", unsafe_allow_html=True)
st.write("___")

# If user is not logged in
if not st.session_state.logged_in:
    st.subheader("🔐 Login or Create Account")

    choice = st.radio("Choose action:", ["🔓 Login", "🆕 Register"], horizontal=True)

    uname = st.text_input("👤 Username")
    upass = st.text_input("🔑 Password", type="password")

    if choice == "🔓 Login":
        if st.button("🚀 Login Now"):
            if login_user(uname, upass):
                st.session_state.logged_in = True
                st.session_state.user = uname
                st.success(f"🎉 Welcome back, **{uname}** 👋")
                st.experimental_rerun()
            else:
                st.error("❌ Login failed. Please check your credentials.")

    elif choice == "🆕 Register":
        if st.button("✅ Create Account"):
            if register_user(uname, upass):
                st.success("✅ Registration successful! Now you can login.")
            else:
                st.warning("⚠️ Username already exists. Try another.")

# If already logged in
else:
    st.success(f"🟢 You are logged in as **{st.session_state.user}**")

    st.markdown("---")
    st.subheader("🎯 What do you want to do today?")
    st.markdown("📝 *Soon you’ll be able to:*")
    st.markdown("- Track your mood daily 😊😔😡")
    st.markdown("- Write your journal 📓")
    st.markdown("- Save your learnings 📚")
    st.markdown("- Set life goals 🎯")
    st.markdown("- And much more powered by AniGPT 🚀")

    st.markdown("---")
    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.user = ""
        st.experimental_rerun()
