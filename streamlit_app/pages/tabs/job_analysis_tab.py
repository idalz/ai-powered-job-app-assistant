import streamlit as st
import re

def show(api_client):
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

                    # Displaying the extracted information as individual fields
                    st.markdown("### Extracted Job Information")
                    
                    # Extracting each field with default fallback value "Not mentioned"
                    job_title = extracted_info.get('job_title', 'Not mentioned')
                    location = extracted_info.get('location', 'Not mentioned')
                    experience_level = extracted_info.get('experience_level', 'Not mentioned')
                    description = extracted_info.get('description', 'Not mentioned')
                    company = extracted_info.get('company', 'Not mentioned')
                    skills = ', '.join(extracted_info.get('skills', ['Not mentioned']))

                    # Display the information
                    st.write(f"**Job Title**: {job_title}")
                    st.write(f"**Location**: {location}")
                    st.write(f"**Experience Level**: {experience_level}")
                    st.write(f"**Description**: {description}")
                    st.write(f"**Company Name**: {company}")
                    st.write(f"**Required Skills**: {skills}")

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
