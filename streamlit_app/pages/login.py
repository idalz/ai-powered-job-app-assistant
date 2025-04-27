import streamlit as st
from services.api_client import APIClient

# Streamlit page settings
st.set_page_config(
    page_title="Login - AI Job Application Assistant",
    page_icon="🤖",
    layout="centered",
)

# If already logged in, redirect to dashboard
if st.session_state.get("is_logged_in") and st.session_state.get("access_token"):
    st.switch_page("pages/dashboard.py")

api_client = APIClient()

st.title("Login")

# Email & Password input
email = st.text_input("Email")
password = st.text_input("Password", type="password")

# Login button
if st.button("Login"):
    if not email or not password:
        st.warning("Please enter both email and password.")
    else:
        try:
            response = api_client.post("auth/login", json={"email": email, "password": password})
            if response.status_code == 200:
                data = response.json()
                st.session_state.access_token = data["access_token"]
                st.session_state.is_logged_in = True
                st.success("Login successful! Redirecting...")
                st.rerun()
            else:
                st.error(f"Login failed: {response.json().get('detail', 'Unknown error')}")
        except Exception as e:
            st.error(f"Error connecting to server: {e}")

# Back to home button
if st.button("Back to Home"):
    st.switch_page("main.py")
