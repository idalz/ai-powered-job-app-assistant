import streamlit as st
from services.api_client import APIClient

def show():
    st.subheader("Match Candidates 🎯")

    api_client = APIClient(token=st.session_state.access_token)

    job_description = st.text_area("Paste the job description here:")

    if st.button("Find Best Candidates 🚀"):
        if not job_description.strip():
            st.warning("Please paste a job description first.")
            return

        with st.spinner("Searching best candidates..."):
            candidates = search_best_candidates(api_client, job_description)

        if not candidates:
            st.info("No matching candidates found. Try adjusting the job description.")
            return

        st.success(f"Found {len(candidates)} candidates!")

        with st.spinner("Loading candidates' info..."):
            display_candidates(api_client, candidates)

# Find Best Candidates
def search_best_candidates(api_client: APIClient, job_description: str):
    try:
        response = api_client.post(
            "recruiter-search/candidates",
            json={"job_description": job_description}
        )
        if response.status_code == 200:
            return response.json().get("results", [])
        else:
            st.error(f"Search failed: {response.json().get('detail', 'Unknown error')}")
            return []
    except Exception as e:
        st.error(f"Error contacting server: {e}")
        return []

# Fetch multiple users by emails
def fetch_users_info(api_client: APIClient, emails: list):
    try:
        response = api_client.post(
            "users/search-users",
            json={"emails": emails}
        )
        if response.status_code == 200:
            users_list = response.json()
            return {user["email"]: user for user in users_list}
        else:
            return {}
    except Exception:
        return {}

# Display candidates 
def display_candidates(api_client: APIClient, candidates: list):
    # Collect all emails
    emails = [c.get("metadata", {}).get("email") for c in candidates if c.get("metadata", {}).get("email")]

    if not emails:
        st.error("No emails found in candidates.")
        return

    # Fetch all user infos at once
    users_info = fetch_users_info(api_client, emails)

    # Now display each candidate
    for idx, candidate in enumerate(candidates, start=1):
        email = candidate.get("metadata", {}).get("email")
        resume_text = candidate.get("text", "")

        if not email or email not in users_info:
            continue

        user_info = users_info[email]

        with st.expander(f"🎯 Candidate {idx}: {user_info.get('name', 'Unnamed')}"):
            st.markdown(f"**Name:** {user_info.get('name', '-')}")
            st.markdown(f"**Email:** {user_info.get('email', '-')}")
            st.markdown(f"**Phone:** {user_info.get('phone_number', '-')}")
            if user_info.get("linkedin_url"):
                st.markdown(f"[LinkedIn Profile]({user_info['linkedin_url']})")
            if user_info.get("github_url"):
                st.markdown(f"[GitHub Profile]({user_info['github_url']})")

            # Resume text in a text_area
            st.text_area(
                "Resume Text",
                value=resume_text,
                height=300,
                key=f"resume_{idx}"
            )

            # Download Button
            st.download_button(
                label="📥 Download Resume",
                data=resume_text,
                file_name=f"{user_info.get('name', 'resume')}_resume.txt",
                mime="text/plain",
                key=f"download_resume_{idx}"
            )
