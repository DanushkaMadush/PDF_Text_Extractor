# app/api/v1/endpoints.py

from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import logging
from app.services.extractor import process_pdf

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/extract")
async def extract_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    
    try:
        result = process_pdf(file)
        return JSONResponse(content=result)
    
    except Exception as e:
        logger.error(f"Failed to response PDF : {e}")
        raise HTTPException(status_code=500 , detail="Internal PDF processing PDF error")

    # Placeholder logic until we implement extractor service
    return JSONResponse({
        "message": "File received successfully.",
        "filename": file.filename,
        "content_type": file.content_type
    })
