# AI-Powered Job Application Assistant

A **LangChain**-based app using **OpenAI**, **Pinecone**, and **FastAPI** to compare resumes with job descriptions, generate tailored cover letters, and perform recruiter-driven candidate search via **RAG**. Features include **Streamlit** UI, **JWT auth** and **PostgreSQL**.  

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

- **Backend**: FastAPI, SQLAlchemy 2.0, Alembic
- **Frontend**: Streamlit
- **AI**: LangChain 1.0+, OpenAI API
- **Vector Database**: Pinecone
- **Database**: PostgreSQL 15 with psycopg3
- **Authentication**: JWT (JSON Web Tokens)
- **Containerization**: Docker
- **Package Manager**: uv (fast Python package installer)
- **Testing**: Pytest
- **Environment**: Python 3.13+

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
- **Docker** and **Docker Compose**
- **Python 3.13+** (for local development)
- **uv** package manager (for local development)

### Quick Start with Docker (Recommended)

1. **Clone the repository**
```bash
git clone https://github.com/idalz/ai-powered-job-app-assistant.git
cd ai-powered-job-app-assistant
```

2. **Set up environment variables**

Copy the example file and fill in your credentials:
```bash
cp .env.example .env
```

Edit `.env` and add your keys:
```env
OPENAI_API_KEY=your-openai-api-key-here
PINECONE_API_KEY=your-pinecone-api-key-here
PINECONE_INDEX_NAME=your-pinecone-index-name

POSTGRES_USER=your-username
POSTGRES_PASSWORD=your-password
POSTGRES_DB=job_app_db

DATABASE_URL=postgresql+psycopg://${POSTGRES_USER}:${POSTGRES_PASSWORD}@db:5432/${POSTGRES_DB}
SECRET_KEY=your-secret-key-here-change-this-in-production
```

3. **Start the application**
```bash
docker-compose up --build
```

This will:
- Pull PostgreSQL 15 image
- Build backend and frontend containers
- Run database migrations automatically
- Persist data in a Docker volume

4. **Access the application**
- **Frontend (Streamlit)**: http://localhost:8501
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

---
## Development

### Local Development (without Docker)

1. **Install uv** (if not already installed)
```bash
# On macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

2. **Install dependencies**
```bash
# Install all dependencies (backend + frontend)
uv sync --all-groups
```

3. **Set up environment variables**

Update your `.env` to use `localhost` for the database:
```env
DATABASE_URL=postgresql+psycopg://${POSTGRES_USER}:${POSTGRES_PASSWORD}@localhost:15432/${POSTGRES_DB}
```

4. **Start PostgreSQL** (if not using Docker)
```bash
# Or start just the database container
docker-compose up db -d
```

5. **Run database migrations**
```bash
uv run alembic upgrade head
```

6. **Run the FastAPI backend**
```bash
uv run uvicorn app.main:app --reload
```

7. **Run the Streamlit frontend** (in a separate terminal)
```bash
uv run streamlit run streamlit_app/main.py
```

### Adding Dependencies

```bash
# Backend dependencies
uv add package-name

# Frontend dependencies
uv add --group frontend package-name
```

---
## Testing

Run tests using uv:
```bash
uv run pytest
```

Currently, tests are not connected to a database. Run only input/output tests for endpoints and llm tests.

---
## License
This project is licensed under the [MIT License](LICENSE).
