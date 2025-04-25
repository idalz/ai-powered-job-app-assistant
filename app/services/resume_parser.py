import pdfplumber
import docx
from app.core.logger import logger

# Parse .pdf
def parse_pdf_resume(file_path: str) -> str:
    try:
        with pdfplumber.open(file_path) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() + "\n"
        logger.info(f"Parsed PDF resume: {file_path}")
        return text.strip()
    except Exception as e:
        logger.error(f"Error parsing PDF resume: {e}")
        return ""

# Parse .docx 
def parse_docx_resume(file_path: str) -> str:
    try:
        doc =  docx.Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])
        logger.info(f"Parsed DOCX resume: {file_path}")
        return text.strip()
    except Exception as e:
        logger.error(f"Error parsing DOCX resume: {e}")
        return ""