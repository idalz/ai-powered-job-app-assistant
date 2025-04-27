import streamlit as st
from services.api_client import APIClient
import re

api_client = APIClient(token=st.session_state.access_token)

def show():
    st.subheader("Job Analysis 🧠")

    job_text = st.text_area("Paste the job description here:", key="job_analysis_job_text")

    # Analyze Job Button
    if st.button("Analyze Job"):
        if not job_text.strip():
            st.warning("Please paste a job description first.")
            return

        with st.spinner("Analyzing job description..."):
            try:
                response = api_client.post("job-analysis/job-info", json={"job_text": job_text})
                if response.status_code == 200:
                    extracted_info = response.json()
                    st.success("Job analysis completed!")
                    st.json(extracted_info)
                else:
                    st.error(f"Failed to analyze job: {response.json().get('detail', 'Unknown error')}")
            except Exception as e:
                st.error(f"Error connecting to server: {e}")

    st.divider()

    st.subheader("🔍 Compare Your Resume to This Job")

    if st.button("Compare Resume to Job"):
        if not job_text.strip():
            st.warning("Please paste a job description first.")
            return

        with st.spinner("Matching resume to job..."):
            try:
                response = api_client.post(
                    "job-analysis/match",
                    json={
                        "job_info": job_text
                    }
                )
                if response.status_code == 200:
                    match_result = response.json().get("match_result", "")
                    st.success("Match analysis complete!")

                    # Try to extract the Match Score using regex
                    match = re.search(r"(\d+)%", match_result)
                    if match:
                        score = int(match.group(1))
                        st.markdown("### 📋 Match Results:")

                        # Display score with color badge
                        if score >= 80:
                            st.success(f"🟢 Excellent Fit: {score}%")
                        elif score >= 60:
                            st.warning(f"🟠 Moderate Fit: {score}%")
                        else:
                            st.error(f"🔴 Weak Fit: {score}%")
                    else:
                        st.info("Match score not found.")

                    # Show full match result text
                    st.markdown("---")
                    st.markdown(match_result)
                else:
                    st.error(f"Failed to match: {response.json().get('detail', 'Unknown error')}")
            except Exception as e:
                st.error(f"Error contacting server: {e}")
