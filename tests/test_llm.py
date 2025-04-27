from app.core.llm import (
    extract_resume_info,
    extract_job_info,
    match_resume_to_job,
    generate_cover_letter,
)

def test_extract_resume_info_returns_content():
    dummy_resume = "John Doe\nEmail: john@example.com\nSkills: Python, Machine Learning"
    result = extract_resume_info(dummy_resume)

    assert isinstance(result, dict)
    assert "extracted_info" in result
    assert result["extracted_info"] != ""

def test_extract_job_info_returns_json():
    dummy_job = "We are hiring a Python Developer located in Amsterdam. Skills: Python, Django."
    result = extract_job_info(dummy_job)

    assert isinstance(result, dict)
    assert "job_title" in result
    assert "skills" in result
    assert result.get("skills", None) != ""

def test_match_resume_to_job_returns_match_result():
    dummy_resume = "Skills: Python, Machine Learning"
    dummy_job = "Looking for a Python Engineer experienced in Django."

    result = match_resume_to_job(dummy_resume, dummy_job)

    assert isinstance(result, dict)
    assert "match_result" in result
    assert result["match_result"] != ""

def test_generate_cover_letter_returns_text():
    dummy_resume = "John Doe - Python Developer"
    dummy_job = "We are hiring a Python Developer at Google."
    guidelines = "Make it short and enthusiastic."

    result = generate_cover_letter(dummy_resume, dummy_job, guidelines)

    assert isinstance(result, str)
    assert len(result) > 50  # Should be a decently long text