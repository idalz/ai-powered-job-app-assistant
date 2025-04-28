import streamlit as st
from typing import Dict, Any

def show(user_info: Dict[str, Any], api_client):
    st.subheader("Your Personal Info 📄")

    st.title(user_info.get("email"))
    # Resume Upload Section
    uploaded_file = st.file_uploader("Upload your updated resume", type=["pdf", "docx"])

    if st.button("Update Resume") and uploaded_file is not None and user_info.get("email"):
        with st.spinner("Uploading your resume..."):
            files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
            try:
                response = api_client.post("resumes/upload", files=files)
                if response.status_code == 200:
                    st.success("Resume uploaded and updated successfully!")
                else:
                    if response.content:
                        error_detail = response.json().get('detail', 'Unknown error')
                    else:
                        error_detail = "Empty response from server."
                    st.error(f"Failed to upload resume: {error_detail}")
            except Exception as e:
                st.error(f"Error uploading resume: {e}")
    
    # User info
    st.text_input("Email", value=user_info.get("email", ""), disabled=True)
    name = st.text_input("Name", value=user_info.get("name", ""))
    phone_number = st.text_input("Phone Number", value=user_info.get("phone_number", ""))
    linkedin_url = st.text_input("LinkedIn URL", value=user_info.get("linkedin_url", ""))
    github_url = st.text_input("GitHub URL", value=user_info.get("github_url", ""))

    if st.button("Update Info"):
        updated_fields = {
            "name": name,
            "phone_number": phone_number,
            "linkedin_url": linkedin_url,
            "github_url": github_url,
        }
        with st.spinner("Updating your info..."):
            try:
                response = api_client.put("users/me", json=updated_fields)
                if response.status_code == 200:
                    st.success("Info updated successfully!")
                    st.session_state.user_info['name'] = updated_fields['name']
                    st.session_state.user_info['phone_number'] = updated_fields['phone_number']
                    st.session_state.user_info['linkedin_url'] = updated_fields['linkedin_url']
                    st.session_state.user_info['github_url'] = updated_fields['github_url']
                else:
                    if response.content:
                        error_detail = response.json().get('detail', 'Unknown error')
                    else:
                        error_detail = "Empty response from server."
                    st.error(f"Failed to update info: {error_detail}")
            except Exception as e:
                st.error(f"Error updating info: {e}")
