from app.core.llm import extract_resume_info, extract_job_info, match_resume_to_job, generate_cover_letter

def test_extract_resume_info():
    text = "Name: Test User\nSkills: Python, SQL\nExperience: 3 years BI"
    result = extract_resume_info(text)
    assert "Skills" in result["extracted_info"]

def test_extract_job_info():
    text = "Job Title: Data Analyst\nRequirements: SQL, Python"
    result = extract_job_info(text)
    assert "Job Title" in result["extracted_info"]

def test_resume_job_match():
    resume = "Skills: Python, SQL"
    job = "Requirements: Python, SQL, Power BI"
    result = match_resume_to_job(resume, job)
    assert "match_result" in result

def test_generate_cover_letter():
    resume = "Name: John Doe\nSkills: Python, SQL"
    job = "Job Title: Developer\nRequirements: Python"
    result = generate_cover_letter(resume, job, guidelines="Make it enthusiastic")
    assert "cover_letter" in result
