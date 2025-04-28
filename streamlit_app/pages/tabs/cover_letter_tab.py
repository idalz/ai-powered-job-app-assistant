import streamlit as st

def show(api_client):
    st.subheader("Cover Letter Generator 📝")

    job_info = st.text_area("Paste the job description here:", key="cover_letter_job_info")
    guidelines = st.text_area("Any special guidelines? (Optional)", placeholder="e.g., emphasize leadership, make it formal, max words...")

    if st.button("Generate Cover Letter"):
        if not job_info.strip():
            st.warning("Please paste a job description first.")
            return

        with st.spinner("Generating your cover letter..."):
            try:
                response = api_client.post(
                    "letters/generate",
                    json={"job_info": job_info, "guidelines": guidelines}
                )
                if response.status_code == 200:
                    data = response.json()
                    generated_letter = data.get("cover_letter", "")
                    st.success("Cover letter generated successfully!")

                    st.text_area("Generated Cover Letter:", value=generated_letter, height=400, key="cover_letter_display")

                    st.download_button(
                        label="📋 Copy Cover Letter",
                        data=generated_letter,
                        file_name="cover_letter.txt",
                        mime="text/plain"
                    )
                else:
                    st.error(f"Failed to generate cover letter: {response.json().get('detail', 'Unknown error')}")
            except Exception as e:
                st.error(f"Error connecting to server: {e}")
