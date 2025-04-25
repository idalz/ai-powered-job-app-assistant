from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Test Root
def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

# Test resume upload
def test_upload_resume():
    file_path = "tests/sample_resume.txt" # Temporary .txt file
    with open(file_path, "w") as f:
        f.write("Name: John Doe\nSkills: Python, SQL")

    with open(file_path, "rb") as file:
        response = client.post(
            "/api/v1/resumes/upload",
            files={"file": ("sample_resume.txt", file, "text/plain")}
        )
    
    assert response.status_code == 200
    data = response.json()
    assert "parsed_text" in data
    assert "uploaded" in data["message"].lower()

# Test job description parse
def test_parse_job_description():
    payload = {
        "job_text": "Job Title: AI Engineer\nRequirements: Python, ML, LangChain"
    }
    response = client.post("/api/v1/jobs/parse", json=payload)
    assert response.status_code == 200
    assert "extracted_info" in response.json()

# Test resume-job match
def test_match_resume_and_job():
    payload = {
        "resume_info": "Skills: Python, SQL",
        "job_info": "Job Title: Data Engineer\nRequirements: Python, SQL, Airflow"
    }
    response = client.post("/api/v1/assistant/match", json=payload)
    assert response.status_code == 200
    assert "match_result" in response.json()

# Test cover letter generation
def test_cover_letter_endpoint():
    payload = {
        "resume_info": "Skills: Python, FastAPI",
        "job_info": "Job Title: Developer\nRequirements: Python",
        "guidelines": "Make it concise"
    }
    response = client.post("/api/v1/letters/generate", json=payload)
    assert response.status_code == 200
    assert "cover_letter" in response.json()

# Test upload + auto store
def test_upload_and_store_resume(tmp_path):
    # Create fake resume file
    file_path = tmp_path / "resume.txt"
    file_path.write_text("Yannis is a backend engineer skilled in FastAPI and LangChain.")

    with open(file_path, "rb") as file:
        response = client.post(
            "/api/v1/resumes/upload",
            files={"file": ("resume.txt", file, "text/plain")}
        )

    assert response.status_code == 200
    data = response.json()
    assert "parsed_text" in data
    assert "pinecone_store" in data
    assert data["pinecone_store"]["status"] == "stored"

def test_auto_generate_letter():
    payload = {
        "job_text": "We are hiring a backend engineer with Python, FastAPI, and LangChain skills.",
        "guidelines": "Mention my passion for clean code and remote work."
    }
    response = client.post("/api/v1/assistant/auto-generate-letter", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert "job_info" in data
    assert "matched_resume" in data
    assert "match_result" in data
    assert "cover_letter" in data
    