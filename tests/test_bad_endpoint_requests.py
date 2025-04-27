# tests/test_auth_endpoints.py

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_login_endpoint_exists_and_returns_error():
    # Arrange (fake credentials)
    fake_credentials = {
        "email": "fake@example.com",
        "password": "fakepassword"
    }
    
    # Act
    response = client.post("/api/v1/endpoints/auth/login", json=fake_credentials)

    # Assert
    assert response.status_code in (401, 422)  # 401 = unauthorized, 422 = validation error if bad body
    assert response.headers["content-type"] == "application/json"
    
    # If 401, check correct error message
    if response.status_code == 401:
        assert "detail" in response.json()
        assert response.json()["detail"] == "Invalid email or password."

def test_register_endpoint_exists_and_returns():
    # Arrange: fake user
    fake_user = {
        "email": "fakeuser@example.com",
        "password": "securepassword",
        "name": "Fake User",
        "phone_number": "1234567890",
        "linkedin_url": "https://linkedin.com/in/fakeuser",
        "github_url": "https://github.com/fakeuser",
        "resume": "Sample resume text",
        "is_recruiter": False
    }

    # Act
    response = client.post("/api/v1/endpoints/users/register", json=fake_user)

    # Assert
    assert response.status_code in (200, 400)  # 400 if already exists, 200 if success
    assert response.headers["content-type"] == "application/json"
    
    # Additional check if it succeeded
    if response.status_code == 200:
        response_json = response.json()
        assert "email" in response_json or "message" in response_json  # depending on your register_user return
    elif response.status_code == 400:
        assert "detail" in response.json()

def test_read_my_own_info_requires_auth():
    # Act
    response = client.get("/api/v1/endpoints/users/me")
    
    # Assert
    assert response.status_code == 403 or response.status_code == 401  # 401/403 if no token
    assert "detail" in response.json()

def test_update_my_own_info_requires_auth():
    # Arrange
    fake_update_data = {
        "name": "Updated Name",
        "phone_number": "9999999999",
        "linkedin_url": "https://linkedin.com/in/updateduser",
        "github_url": "https://github.com/updateduser"
    }

    # Act
    response = client.put("/api/v1/endpoints/users/me", json=fake_update_data)

    # Assert
    assert response.status_code == 403 or response.status_code == 401  # No token provided
    assert "detail" in response.json()

def test_search_users_requires_auth():
    # Arrange
    fake_request = {
        "emails": ["test@example.com", "another@example.com"]
    }

    # Act
    response = client.post("/api/v1/endpoints/users/search-users", json=fake_request)

    # Assert
    assert response.status_code == 403 or response.status_code == 401  # Missing token
    assert "detail" in response.json()

def test_search_candidates_requires_auth():
    # Act
    response = client.post("/api/v1/endpoints/recruiter-search/candidates", json={"job_description": "Some job description"})

    # Assert
    assert response.status_code == 403 or response.status_code == 401  # Unauthorized
    assert "detail" in response.json()

def test_generate_cover_letter_requires_auth():
    # Act
    response = client.post("/api/v1/endpoints/letters/generate", json={"job_info": "Job description here."})

    # Assert
    assert response.status_code == 403 or response.status_code == 401
    assert "detail" in response.json()
 
def test_parse_job_description_requires_job_text():
    # Missing job_text
    response = client.post("/api/v1/endpoints/job-analysis/job-info", json={})

    assert response.status_code == 422  # FastAPI will throw 422 Unprocessable Entity if body field missing
    
def test_match_resume_and_job_requires_auth():
    # No token
    response = client.post("/api/v1/endpoints/job-analysis/match", json={"job_info": "Sample job description"})

    assert response.status_code == 403 or response.status_code == 401
    assert "detail" in response.json()