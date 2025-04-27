import streamlit as st

# Streamlit page settings
st.set_page_config(
    page_title="AI Job Application Assistant",
    page_icon="🤖",
    layout="centered",
)

st.title("Welcome to AI Job Application Assistant 🤖")

st.markdown(
    """
    ## Empower Your Job Search with AI

    Upload your resume, analyze job descriptions, generate tailored cover letters,
    or find your perfect match instantly!

    ---
    """
)

st.write("Already have an account?")
if st.button("Login"):
    st.switch_page("pages/login.py")

st.write("New here?")
if st.button("Register"):
    st.switch_page("pages/register.py")
