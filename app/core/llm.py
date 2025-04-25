from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from app.core.config import settings
from app.core.logger import logger

llm = ChatOpenAI(
    temperature=0.2,
    model="gpt-3.5-turbo",
    openai_api_key=settings.OPENAI_API_KEY
)

prompt_template = ChatPromptTemplate.from_template("""
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

def extract_resume_info(resume_text: str) -> dict:
    try:
        chain = prompt_template | llm
        result = chain.invoke({"resume_text":resume_text})

        logger.info("LangChain LLM extraction successful")
        return {"extracted_info": result.content}
    except Exception as e:
        logger.error(f"LangChain extraction failed: {e}")
        return {"error": str(e)}
    