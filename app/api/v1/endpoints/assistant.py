from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse
from app.core.llm import extract_job_info, match_resume_to_job, generate_cover_letter
from app.core.rag import search_resumes
from app.core.logger import logger
from app.services.check_result_type import check_result_type

router = APIRouter()

# Resume-job match
@router.post("/match")
def match_resume_and_job(
    resume_info: str = Body(..., embed=True),
    job_info: str = Body(..., embed=True)
):
    logger.info("Running resume-job matching.")
    result = match_resume_to_job(resume_info, job_info)
    return JSONResponse(content=result)

# Auto generate a cover letter
@router.post("/auto-generate-letter")
async def auto_generate_letter(
    job_text: str = Body(..., embed=True),
    guidelines: str = Body(default="", embed=True)
):
    logger.info("Auto-generating letter.")

    # Extract job info
    job_info_result = extract_job_info(job_text)
    job_info = job_info_result.get("extracted_info", "")
    if not job_info:
        return JSONResponse(status_code=400, content={"error": "Failed to extract job info"})

    # Search for best matching resume from vector
    search_results = search_resumes(job_text, k=1)
    if not search_results:
        return JSONResponse(status_code=404, content={"error": "No resumes found in Pinecone"})

    best_resume = search_results[0]["text"]

    # Match resume to job
    match_result = match_resume_to_job(best_resume, job_info)

    # Generate cover letter
    raw_letter = generate_cover_letter(best_resume, job_info, guidelines)
    cover_letter = check_result_type(raw_letter, expected_type=str, fallback="")

    logger.info(f"Auto-generated cover letter: {cover_letter}")

    return JSONResponse(content={
        "job_info": job_info,
        "matched_resume": best_resume,
        "match_result": match_result,
        "cover_letter": cover_letter
    })
