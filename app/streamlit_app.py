import streamlit as st
import requests
from core.config import settings

API_URL = settings.API_URL

st.set_page_config(page_title="AI Job Assistant", layout="centered")

st.title("AI-Powered Job Application Assistant")
st.write("Upload your resume, paste a job description and generate a custom motivation letter!")

# tab1 for manual generation, tab 2 for auto generation
tab1, tab2, tab3 = st.tabs(["Manual Upload", "Auto Resume Match", "Job Insights"])

# -------- TAB 1: Manual Upload --------
with tab1:
    st.header("Upload Resume & Job Description")
    # Resume upload
    resume_file = st.file_uploader("Upload your resume", type=["pdf", "docx"])

    # Job description
    job_description = st.text_area("Paste the job description", height=300)

    # Extra guidelines
    guidelines = st.text_area("Any extra guidelines like max words, style, etc.? (Optional)", height=100)

    # Sumbit
    if st.button("Generate Letter", key="manual"):
        if resume_file is None or not job_description.strip():
            st.warning("Please upload a resume and paste a job description.")
        else:
            with st.spinner("Uploading resume and extracting text..."):
                # Upload resume extract text
                upload_response = requests.post(
                    f"{API_URL}/resumes/upload",
                    files={"file": resume_file},
                    data={"name": "Manual Upload"}
                )
                if upload_response.status_code == 200:
                    parsed_text = upload_response.json()["parsed_text"]

                    #  Generate letter
                    data = {
                        "resume_info": parsed_text,
                        "job_info": job_description,
                        "guidelines": guidelines or ""
                    }
                    response = requests.post(f"{API_URL}/letters/generate", json=data)

                    if response.status_code == 200:
                        result = response.json()
                        
                        col1, col2 = st.columns(2) 

                        with col1:
                            st.subheader("Resume Info")
                            st.text_area("Extracted Resume", result["resume_info"], height=300)

                        with col2:
                            st.subheader("Job Info")
                            st.text_area("Extracted Job Info", result["job_info"], height=300)
                        
                        st.success("Letter generated!")

                        cover_letter_text = result.get("cover_letter", "")

                        if isinstance(cover_letter_text, str) and cover_letter_text:
                            st.code(cover_letter_text, language="markdown")
                            st.download_button(
                                "Download Letter",
                                cover_letter_text,
                                file_name="cover_letter.txt"
                            )
                        else:
                            st.error("Cover letter not found or invalid format.")
                    else:
                        st.error(f"Error generating letter: {response.status_code} - {response.text}")
                else:
                    st.error(f"Error uploading resume: {upload_response.status_code} - {upload_response.text}")

# -------- TAB 2: Auto Resume Match --------
with tab2:
    st.header("Paste Job Description Only")

    # Job description input
    job_description_auto = st.text_area("Paste the job description here", height=250, key="desc_auto")

    # Extra guidelines input
    guidelines_auto = st.text_area("Any extra guidelines like max words, style, etc.? (Optional)", height=100, key="guidelines_auto")

    # Submit button
    if st.button("Generate Using Best Resume", key="auto"):
        if not job_description_auto.strip():
            st.warning("Please paste the job description.")
        else:
            with st.spinner("Finding best resume and generating your letter..."):
                data = {
                    "job_text": job_description_auto,
                    "guidelines": guidelines_auto or ""
                }
                response = requests.post(f"{API_URL}/assistant/auto-generate-letter", json=data)

                if response.status_code == 200:
                    result = response.json()

                    col1, col2 = st.columns(2) 

                    with col1:
                        st.subheader("Best Matching Resume")
                        st.text_area("Best Matching Resume", result.get("matched_resume", ""), height=300)

                    with col2:
                        st.subheader("Job Info")
                        st.text_area("Extracted Job Info", result.get("job_info", ""), height=300)

                    st.success("Letter generated using best-matching resume!")

                    cover_letter_text = result.get("cover_letter", "")

                    if isinstance(cover_letter_text, str) and cover_letter_text:
                        st.code(cover_letter_text, language="markdown")
                        st.download_button(
                            "Download Letter",
                            cover_letter_text,
                            file_name="cover_letter.txt"
                        )
                    else:
                        st.error("Cover letter not found or invalid format.")
                else:
                    st.error(f"Error: {response.status_code} - {response.text}")

# -------- TAB 3: Job Insights --------
with tab3:
    st.header("Analyze a Job Description")

    # SESSION STATE to remember if Analyze was clicked
    if "analyze_clicked" not in st.session_state:
        st.session_state["analyze_clicked"] = False

    # Input: Job Description
    job_description_insights = st.text_area("Paste the job description here", height=300, key="insights_desc")

    if st.button("Analyze Job Description", key="analyze"):
        if not job_description_insights.strip():
            st.warning("Please paste a job description first.")
        else:
            st.session_state["analyze_clicked"] = True
        
    if st.session_state["analyze_clicked"]:
        with st.spinner("Analyzing the job description..."):
            payload = {"job_text": job_description_insights}
            response = requests.post(f"{API_URL}/jobs/parse", json=payload)

            if response.status_code == 200:
                result = response.json()
                st.success("Job Description Analyzed!")

                # Display extracted fields
                if "job_title" in result:
                    st.subheader("Title")
                    st.write(result["job_title"])

                if "location" in result:
                    st.subheader("Location")
                    st.write(result["location"])

                if "experience_level" in result:
                    st.subheader("Experience Level")
                    st.write(result["experience_level"])

                if "description" in result:
                    st.subheader("Summary")
                    st.write(result["description"])
                
                if "company" in result:
                    st.subheader("Company Name")
                    st.write(result["company"])

                if "skills" in result and result["skills"]:
                    st.subheader("Skills / Tech Stack")

                    job_skills = set(result["skills"])
                    st.write(", ".join(job_skills))

                    # Skill chart
                    skill_counts = {skill: 1 for skill in job_skills}
                    st.bar_chart(skill_counts)

                    # Skill Gap Resume Upload
                    st.markdown("---")
                    st.subheader("Resume Skill Gap Analysis")

                    # Expand to show full raw data
                with st.expander("See Full Extracted Data"):
                    st.json(result)

                    # Upload a resume for comparison
                    resume_file_for_check = st.file_uploader(
                        "Upload your resume for skill comparison",
                        type=["pdf", "docx"],
                        key="resume_gap"
                    )

                    if resume_file_for_check:
                        with st.spinner("Parsing your resume..."):
                            upload_response = requests.post(
                                f"{API_URL}/resumes/upload",
                                files={"file": resume_file_for_check},
                                data={"name": "Skill Gap Check"}
                            )

                            if upload_response.status_code == 200:
                                parsed_resume = upload_response.json()
                                resume_info = parsed_resume.get("extracted_info", {})

                                resume_skills = set(resume_info.get("skills", []))

                                # Find matches and gaps
                                missing_skills = job_skills - resume_skills
                                matched_skills = job_skills & resume_skills

                                st.success(f"Skills you already have ({len(matched_skills)}):")
                                if matched_skills:
                                    st.write(", ".join(matched_skills))
                                else:
                                    st.write("No matches found yet.")

                                st.error(f"Missing Skills for this job ({len(missing_skills)}):")
                                if missing_skills:
                                    st.write(", ".join(missing_skills))
                                else:
                                    st.write("No missing skills! Your resume covers everything!")

                            else:
                                st.error(f"Error parsing resume: {upload_response.status_code} - {upload_response.text}")

            else:
                st.error(f"Error analyzing job description: {response.status_code} - {response.text}")
