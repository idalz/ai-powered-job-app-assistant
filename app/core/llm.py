from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from app.core.config import settings
from app.core.logger import logger
import json 

llm = ChatOpenAI(
    temperature=0.2,
    model="gpt-3.5-turbo",
    openai_api_key=settings.OPENAI_API_KEY
)

def extract_resume_info(resume_text: str) -> dict:
    try:
        prompt = ChatPromptTemplate.from_template("""
        Extract the following information from the given resume text as a JSON:
        - Full Name
        - Email
        - Phone
        - Github
        - LinkedIn
        - Skills
        - Work Experience
        - Education
        - Summary
        - Extra achievements or projects
                                                  
        Instructions:
        If a category is not given return a blank ("").

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
        Extract the following and return it as a valid JSON object:
        - Job Title as job_title
        - Location as location
        - Experience Level as experience_level (search for keywords in the whole text provided)
        - Description as description
        - Company Name as company
        - Required Skills as skills (only keywords)

        Try to Search for these fields in the whole text provided.
        If something is not mentioned, return "Not mentioned" as its value.                                        
                                           
        Job Description:
        {job_text}       
        """)

        chain = prompt | llm
        result = chain.invoke({"job_text": job_text})

        logger.info("Job info extracted successfully")

        job_info = json.loads(result.content)

        return job_info
    except Exception as e:
        logger.error(f"Job info extraction failed: {e}")
        return {"error": str(e)}

def match_resume_to_job(resume_info: str, job_info: str) -> dict:
    try:
        prompt = ChatPromptTemplate.from_template("""
        Compare the following resume information with the job description.

        Resume Info:
        {resume_info}

        Job Description Info:
        {job_info}

        Instructions:
        - When comparing skills, understand common abbreviations and versions:
            - Python 3 is considered the same as Python
            - JS is the same as JavaScript
            - BUT Java is NOT JavaScript
            - C# is NOT the same as C or C++
        - Focus on practical relevance, not exact wording.
        - If a skill is logically equivalent, treat it as matching.
        - If a skill is different (even if similar sounding), treat it as missing.

        Return the following clearly:
        - A brief overall assessment of how well the resume fits the job
        - A bullet list of missing skills or qualifications
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
    
def generate_cover_letter(resume_info: str, job_info: str, guidelines: str = "") -> str:
    try:
        prompt = ChatPromptTemplate.from_template("""
        Write a professional, personalized cover letter based on the information given:

        Resume Info:
        {resume_info}

        Job Description Info:
        {job_info}

        Guidelines:
        - Address the hiring team (no specific name)
        - Mention how the applicant fits the role
        - Highlight relevant skills and experience
        - Extra guidelines given by the user: {guidelines}

        Cover Letter:                                    
        """)

        extra_guidelines = f"- Additional user guidelines:\n{guidelines}" if guidelines else ""
        chain = prompt | llm
        result = chain.invoke({
            "resume_info": resume_info,
            "job_info": job_info,
            "guidelines": extra_guidelines
        })
        logger.info("Cover letter generated successfully")
        return result.content
    except Exception as e:
        logger.error(f"Cover letter generation failed: {e}")
        return {"error": str(e)}
    