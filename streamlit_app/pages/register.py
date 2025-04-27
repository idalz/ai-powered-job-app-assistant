import streamlit as st
from services.api_client import APIClient

# Streamlit page settings
st.set_page_config(
    page_title="Register - AI Job Application Assistant",
    page_icon="🤖",
    layout="centered",
)

st.title("Register")

# Initialize API client
api_client = APIClient()

# Input fields
email = st.text_input("Email")
password = st.text_input("Password", type="password")

# Optional extra fields
name = st.text_input("Name (optional)")
phone_number = st.text_input("Phone Number (optional)")
linkedin_url = st.text_input("LinkedIn URL (optional)")
github_url = st.text_input("GitHub URL (optional)")
is_recruiter = st.checkbox("Register as a recruiter?")

# Register button
if st.button("Register"):
    if not email or not password:
        st.warning("Please enter at least Email and Password.")
    else:
        try:
            payload = {
                "email": email,
                "password": password,
                "name": name,
                "phone_number": phone_number,
                "linkedin_url": linkedin_url,
                "github_url": github_url,
                "is_recruiter": is_recruiter
            }
            with st.spinner("Registering your account..."):
                response = api_client.post("users/register", json=payload)  # <-- No need BASE_API_URL manually
            if response.status_code == 200:
                st.success("Registration successful! Please log in now.")
                st.switch_page("pages/login.py")
            else:
                st.error(f"Registration failed: {response.json().get('detail', 'Unknown error')}")
        except Exception as e:
            st.error(f"Error connecting to server: {e}")

# Back button to Home
if st.button("Back to Home"):
    st.switch_page("main.py")
