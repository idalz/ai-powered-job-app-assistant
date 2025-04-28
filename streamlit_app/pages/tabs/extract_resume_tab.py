import streamlit as st
import json
import docx
import pdfplumber
import io

def show(api_client):
    st.subheader("Extract Resume Information 🧠")

    uploaded_file = st.file_uploader(
        "Upload a Resume (PDF, DOCX, or TXT)",
        type=["pdf", "docx", "txt"]
    )

    if uploaded_file is not None:
        file_content = uploaded_file.read()

        # Simple check for file type
        if uploaded_file.type == "application/pdf" or uploaded_file.name.endswith(".pdf"):
            resume_text = extract_text_from_pdf(file_content)
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document" or uploaded_file.name.endswith(".docx"):
            resume_text = extract_text_from_docx(file_content)
        elif uploaded_file.type == "text/plain" or uploaded_file.name.endswith(".txt"):
            resume_text = file_content.decode("utf-8")
        else:
            st.error("Unsupported file format.")
            return

        st.success("Resume uploaded and parsed successfully!")
        st.text_area("Parsed Resume Text:", value=resume_text, height=300)

        if st.button("🔍 Extract Info"):
            with st.spinner("Extracting info with AI..."):
                try:
                    response = api_client.post(
                        "resumes/extract-resume-info",
                        json={"resume_text": resume_text}
                    )
                    if response.status_code == 200:
                        extracted_info = response.json().get("extracted_info", "{}")
                        display_extracted_info(extracted_info)
                    else:
                        st.error(f"Failed to extract: {response.json().get('detail', 'Unknown error')}")
                except Exception as e:
                    st.error(f"Error contacting server: {e}")

# Small helpers to extract text from files
def extract_text_from_pdf(file_content: bytes) -> str:
    text = ""
    with pdfplumber.open(io.BytesIO(file_content)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    return text

def extract_text_from_docx(file_content: bytes) -> str:
    doc = docx.Document(io.BytesIO(file_content))
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

# Display extracted fields
def display_extracted_info(extracted_info_text: str):
    try:
        extracted_info = json.loads(extracted_info_text)
    except Exception:
        st.error("Failed to parse extracted info.")
        return

    st.subheader("📋 Extracted Resume Information")

    # Top profile fields
    if extracted_info.get("Full Name"):
        st.markdown(f"**Full Name:** {extracted_info['Full Name']}")
    
    if extracted_info.get("Email"):
        st.markdown(f"**Email:** {extracted_info['Email']}")

    if extracted_info.get("Phone"):
        st.markdown(f"**Phone:** {extracted_info['Phone']}")

    if extracted_info.get("Github") and extracted_info["Github"] != "not mentioned":
        st.markdown(f"[GitHub Profile]({extracted_info['Github']})")

    if extracted_info.get("LinkedIn") and extracted_info["LinkedIn"] != "not mentioned":
        st.markdown(f"[LinkedIn Profile]({extracted_info['LinkedIn']})")

    st.markdown("---")

    if extracted_info.get("Summary"):
        st.markdown("### 🧠 Summary")
        st.write(extracted_info["Summary"])

    if extracted_info.get("Skills"):
        st.markdown("### 🛠 Skills")
        for skill in extracted_info["Skills"]:
            st.markdown(f"- {skill}")

    if extracted_info.get("Work Experience"):
        st.markdown("### 💼 Work Experience")
        for exp in extracted_info["Work Experience"]:
            st.markdown(f"- {exp}")

    if extracted_info.get("Education"):
        st.markdown("### 🎓 Education")
        for edu in extracted_info["Education"]:
            st.markdown(f"- {edu}")
 
    if extracted_info.get("Extra achievements or projects"):
        st.markdown("### 🏆 Achievements / Projects")
        for proj in extracted_info["Extra achievements or projects"]:
            st.markdown(f"- {proj}")
