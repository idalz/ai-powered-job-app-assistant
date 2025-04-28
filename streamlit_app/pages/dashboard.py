import streamlit as st
from services.api_client import APIClient

# Streamlit page settings
st.set_page_config(
    page_title="Dashboard - AI Job Application Assistant",
    page_icon="🤖",
    layout="wide",
)

# Check login status and access token
if not st.session_state.get("is_logged_in") or not st.session_state.get("access_token"):
    st.warning("You must be logged in to access the dashboard.")
    st.switch_page("pages/login.py")
    st.stop()

# Initialize API client with the access token
api_client = APIClient(token=st.session_state.access_token)

# IMPORTANT: If token exists, import tabs
from pages.tabs import info_tab, job_analysis_tab, cover_letter_tab, match_candidates_tab, extract_resume_tab

# Fetch user info if not already fetched
if not st.session_state.get("user_info"):
    try:
        with st.spinner("Loading your profile..."):
            response = api_client.get("users/me")
            if response.status_code == 200:
                st.session_state.user_info = response.json()
            else:
                st.error(f"Failed to fetch user info: {response.json().get('detail', 'Unknown error')}")
                st.switch_page("pages/login.py")
                st.stop()
    except Exception as e:
        st.error(f"Error connecting to server: {e}")
        st.switch_page("pages/login.py")
        st.stop()

# Get user_info safely
user_info = st.session_state.get("user_info")

if not user_info:
    st.error("Failed to load user information. Please login again.")
    st.switch_page("pages/login.py")
    st.stop()

# Main Title
st.title(f"Welcome, {user_info.get('name', 'User')}!")

# Sidebar navigation
st.sidebar.title("Navigation")

tab_titles = ["Info", "Job Analysis", "Cover Letter", "Extract Resume Info"]
if user_info.get("is_recruiter"):
    tab_titles.append("Match Candidates")

selected_tab = st.sidebar.radio("Select a page:", tab_titles)

# Show selected tab
if selected_tab == "Info":
    info_tab.show(user_info, api_client)
elif selected_tab == "Job Analysis":
    job_analysis_tab.show(api_client)
elif selected_tab == "Cover Letter":
    cover_letter_tab.show(api_client)
elif selected_tab == "Extract Resume Info":
    extract_resume_tab.show(api_client)
elif selected_tab == "Match Candidates" and user_info.get("is_recruiter"):
    match_candidates_tab.show(api_client)

# Sidebar logout button
if st.sidebar.button("Logout"):
    st.session_state.is_logged_in = False
    st.session_state.access_token = None
    st.session_state.user_info = None
    st.success("Logged out successfully.")
    st.rerun()
    st.switch_page("main.py")
