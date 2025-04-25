from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from app.core.config import settings
from app.core.logger import logger

llm = ChatOpenAI(
    temperature=0.2,
    model="gpt-3.5-turbo",
    openai_api_key=settings.OPENAI_API_KEY
)

def extract_resume_info(resume_text: str) -> dict:
    try:
        prompt = ChatPromptTemplate.from_template("""
        Extract the following information from the given resume text:
        - Full Name
        - Email
        - Skills
        - Work Experience
        - Education
        - Summary
        - Extra achievements or projects

        Resume:
        {resume_text}
        """)

        chain = prompt | llm
        result = chain.invoke({"resume_text":resume_text})
        logger.info("LangChain LLM extraction successful")
        return {"extracted_info": result.content}
    except Exception as e:
        logger.error(f"Resume extraction failed: {e}")
        return {"error": str(e)}
    
def extract_job_info(job_text: str) -> dict:
    try:
        prompt = ChatPromptTemplate.from_template("""
        Extract the following from this job description:
        - Job Title
        - Required Skills
        - Responsibilities
        - Company Name (if mentioned)

        Job Description:
        {job_text}       
        """)

        chain = prompt | llm
        result = chain.invoke({"job_text": job_text})
        logger.info("Job info extracted successfully")
        return {"extracted_info": result.content}
    except Exception as e:
        logger.error(f"Job info extraction failed: {e}")
        return {"error": str(e)}

def match_resume_to_job(resume_info: str, job_info: str) -> dict:
    try:
        prompt = ChatPromptTemplate.from_template("""
        Compare the following resume with the job description.

        Resume Info:
        {resume_info}

        Job Description Info:
        {job_info}

        Return:
        - A brief assessment of how well the resume fits the job
        - A list of missing skills or qualifications
        - A match score out of 100%
        """)  

        chain = prompt | llm
        result = chain.invoke({
            "resume_info": resume_info,
            "job_info": job_info
        }) 
        logger.info("Resume and job comparison complete.")
        return {"match_result": result.content}
    except Exception as e:
        logger.error(f"Resume-job matching failed: {e}")
        return {"error": str(e)}
    