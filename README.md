# JobMatch Assistant

> **AI-Powered Job Application Assistant**

A modern, production-ready application that leverages **GPT-4o-mini**, **LangChain**, **Pinecone**, and **FastAPI** to intelligently match resumes with job descriptions, generate tailored cover letters, and enable recruiter-driven candidate search via **RAG** (Retrieval-Augmented Generation).

**🚀 [Live Demo](https://your-railway-app.railway.app)** *(Coming soon)*

## Key Features

✅ **Secure Authentication** - JWT-based auth with rate limiting (5 login attempts/min)
✅ **Resume Analysis** - AI-powered resume parsing and job matching
✅ **Cover Letter Generation** - Personalized cover letters with custom guidelines
✅ **Recruiter Tools** - RAG-powered candidate search in vector database
✅ **Production-Ready** - CORS protection, MIME type validation, file size limits (10MB)
✅ **Modern Stack** - FastAPI, Streamlit, PostgreSQL, Pinecone, GPT-4o-mini  

---

## Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Usage](#usage)
- [How to Install](#how-to-install)
- [Development](#development)
- [Testing](#testing)
- [License](#license)

---

## Features

- Use the power of **OpenAI LLMs** to:
    1. Extract key details from job descriptions or resumes.
    2. Compare resumes to job descriptions and calculate a match score.
    3. Generate personalized cover letters based on job descriptions with custom guidelines.
- **RAG** using Pinecone Vector Store, enabling recruiters to find the ideal candidates with a single click.
- **Secure login and account management** using JWT tokens.
- **Data storage** in a PostgreSQL database to securely save user information.
- Simple and user-friendly interface built with Streamlit.
- **Dockerized** for fast and easy deployment.
---

## Tech Stack

### Backend
- **FastAPI** - Modern async Python web framework
- **SQLAlchemy 2.0** - SQL toolkit with psycopg3 driver
- **Alembic** - Database migrations
- **PostgreSQL 15** - Production database
- **SlowAPI** - Rate limiting middleware

### AI & ML
- **OpenAI GPT-4o-mini** - Latest, cost-effective LLM
- **LangChain 1.0+** - LLM orchestration framework
- **Pinecone** - Vector database for semantic search
- **text-embedding-3-small** - Efficient embeddings model

### Frontend
- **Streamlit** - Interactive Python web UI
- **Requests** - HTTP client for API calls

### Security & Auth
- **JWT** - Stateless token-based authentication
- **Passlib + Bcrypt** - Password hashing
- **CORS** - Configurable origin protection
- **Rate Limiting** - Brute force protection
- **MIME Validation** - File upload security

### DevOps & Tools
- **uv** - Fast Python package manager (Rust-based)
- **Docker** - Local development environment *(WIP for production)*
- **Railway** - Cloud deployment platform
- **Python 3.13** - Latest Python version

---

## Usage

- Visit the home page to signup or login

![main](app_screenshots/main.png)

- Register as a user or a recruiter

![register](app_screenshots/register.png)

- Upload your resume or update your info

![info_tab](app_screenshots/info.png)

Recruiters have an extra tab!

![info_tab_recruiter](app_screenshots/recruiters.png)

- Analyze jobs and see compatibility with your resume

![job_analysis_tab](app_screenshots/job-analysis.png)
![job_analysis_tab](app_screenshots/job-analysis-job.png)
![job_analysis_tab](app_screenshots/job-analysis-resume-match.png)

- Generate a cover letter with custom guidelines

![cover_letter_tab](app_screenshots/cover-letter.png)
![cover_letter_tab](app_screenshots/cover-letter-generate.png)

- See key details of a resume

![resume_tab](app_screenshots/resume.png)
![resume_tab](app_screenshots/resume-extract.png)

-  Find ideal candidates (only for recruiters)

![recruiter_tab](app_screenshots/find-candidates-match.png)

---

## How to Install

### Prerequisites
- **Python 3.13+**
- **uv** package manager
- **PostgreSQL 15** (or use Docker for DB only)
- API Keys: OpenAI, Pinecone

### Local Development Setup

1. **Clone the repository**
```bash
git clone https://github.com/idalz/jobmatch-assistant.git
cd jobmatch-assistant
```

2. **Install uv** (if not already installed)
```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

3. **Install dependencies**
```bash
uv sync
```

4. **Set up environment variables**

Copy the example file:
```bash
cp .env.example .env
```

Edit `.env` with your credentials:
```env
# OpenAI & Pinecone
OPENAI_API_KEY=your-openai-api-key
PINECONE_API_KEY=your-pinecone-api-key
PINECONE_INDEX_NAME=your-index-name
PINECONE_NAMESPACE=jobmatch

# Database (use localhost for local dev)
POSTGRES_USER=your-username
POSTGRES_PASSWORD=your-password
POSTGRES_DB=jobmatch_db
DATABASE_URL=postgresql+psycopg://${POSTGRES_USER}:${POSTGRES_PASSWORD}@localhost:15432/${POSTGRES_DB}

# Security
SECRET_KEY=your-secret-key-min-32-chars
CORS_ORIGINS=http://localhost:8501,http://localhost:3000

# API Config
API_URL=http://localhost:8000/api/v1/endpoints/
```

5. **Start PostgreSQL** (using Docker)
```bash
docker-compose up db -d
```

6. **Run database migrations**
```bash
uv run alembic upgrade head
```

7. **Start the backend** (terminal 1)
```bash
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

8. **Start the frontend** (terminal 2)
```bash
uv run streamlit run streamlit_app/main.py
```

9. **Access the application**
- **Frontend (Streamlit)**: http://localhost:8501
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

---

### Docker Setup *(Work in Progress)*

Docker Compose configuration is available but currently experiencing build issues. Recommended for local development: use uv directly (see above).

```bash
# Note: Docker build currently WIP
docker-compose up --build
```

---

## 🚀 Deployment (Railway)

The application is deployed on **Railway** with automatic deployments from GitHub.

### Architecture
- **Backend Service**: FastAPI app (`uvicorn app.main:app`)
- **Frontend Service**: Streamlit app (`streamlit run streamlit_app/main.py`)
- **Database**: Railway PostgreSQL plugin

### Environment Variables (Set in Railway Dashboard)

**Backend:**
```env
OPENAI_API_KEY=your-key
PINECONE_API_KEY=your-key
PINECONE_INDEX_NAME=your-index
PINECONE_NAMESPACE=jobmatch
DATABASE_URL=${{Postgres.DATABASE_URL}}
SECRET_KEY=your-32-char-secret
CORS_ORIGINS=https://your-frontend.railway.app
PORT=8000
```

**Frontend:**
```env
API_URL=https://your-backend.railway.app/api/v1/endpoints/
PORT=8501
```

### Deployment Steps

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Deploy to Railway"
   git push origin main
   ```

2. **Create Railway Project**
   - Go to [Railway.app](https://railway.app)
   - Create new project from GitHub repo
   - Add PostgreSQL plugin

3. **Deploy Backend Service**
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - Add environment variables (see above)
   - Deploy!

4. **Deploy Frontend Service**
   - Create new service in same project
   - Start Command: `streamlit run streamlit_app/main.py --server.port $PORT --server.address 0.0.0.0`
   - Add environment variables
   - Set `API_URL` to backend URL
   - Deploy!

5. **Run Migrations**
   - In backend service console: `python -m alembic upgrade head`

---
## Development

### Adding Dependencies

```bash
# Add any dependency
uv add package-name

# Update lockfile
uv lock

# Sync environment
uv sync
```

### Database Migrations

```bash
# Create a new migration
uv run alembic revision --autogenerate -m "description"

# Apply migrations
uv run alembic upgrade head

# Rollback one migration
uv run alembic downgrade -1
```

### Code Quality

```bash
# Run tests
uv run pytest

# Check types (if using mypy)
uv run mypy app/

# Format code (if using ruff)
uv run ruff format .
```

---
## Security Features

This application implements production-grade security measures:

- **JWT Authentication** - Stateless token-based auth with 2-hour expiration
- **Rate Limiting** - Login endpoint limited to 5 attempts/minute (prevents brute force)
- **Password Security** - Bcrypt hashing with salt
- **CORS Protection** - Configurable allowed origins (not `*`)
- **File Upload Security**:
  - MIME type validation (checks actual file content, not just extension)
  - File size limits (10MB max)
  - Secure filename generation (UUID-based)
- **Authorization Checks** - Recruiter-only endpoints properly verified
- **SQL Injection Protection** - SQLAlchemy ORM with parameterized queries
- **Secrets Management** - All keys in environment variables (never hardcoded)

---
## Testing

Run tests using uv:
```bash
uv run pytest
```

Note: Database tests currently not included. Focus on endpoint and LLM integration tests.

---
## License
This project is licensed under the [MIT License](LICENSE).
