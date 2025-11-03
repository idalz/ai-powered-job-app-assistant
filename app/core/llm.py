from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from app.core.config import settings
from app.core.logger import logger
import json
import re 

llm = ChatOpenAI(
    temperature=0.2,
    model="gpt-4o-mini",
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
        - Skills (be careful! try to return the whole skill name, not just a letters of it!)
        - Work Experience (Be careful! Return the whole experience, not just letters of it! Also for each one make it a summary instead of nested list!)
        - Education (Return it as a whole for each education bullet: ex. bachelor, university name, location, year. Also for each one make it a summary instead of nested list! )
        - Summary
        - Extra achievements or projects (Be careful! Return the whole achievements or projects, not just a letters of it! Also for each one make it a summary instead of nested list! )
                                                  
        Instructions:
        If a category is not given return a blank ("").

        Resume:
        {resume_text}
        """)

        chain = prompt | llm
        result = chain.invoke({"resume_text":resume_text})
        logger.info("LangChain LLM extraction successful")

        # Extract JSON from response (handle markdown code blocks)
        content = result.content.strip()

        # Remove markdown code blocks if present
        if content.startswith("```"):
            json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', content, re.DOTALL)
            if json_match:
                content = json_match.group(1)
            else:
                content = content.replace("```json", "").replace("```", "").strip()

        return {"extracted_info": content}
    except Exception as e:
        logger.error(f"Resume extraction failed: {e}")
        logger.error(f"Raw LLM response: {result.content if 'result' in locals() else 'N/A'}")
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

        # Extract JSON from response (handle markdown code blocks)
        content = result.content.strip()

        # Remove markdown code blocks if present
        if content.startswith("```"):
            # Find the JSON content between ```json and ```
            json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', content, re.DOTALL)
            if json_match:
                content = json_match.group(1)
            else:
                # Try removing just the ``` markers
                content = content.replace("```json", "").replace("```", "").strip()

        job_info = json.loads(content)

        return job_info
    except Exception as e:
        logger.error(f"Job info extraction failed: {e}")
        logger.error(f"Raw LLM response: {result.content if 'result' in locals() else 'N/A'}")
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
    