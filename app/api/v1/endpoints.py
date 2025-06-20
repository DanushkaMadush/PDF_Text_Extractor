# app/api/v1/endpoints.py

from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post("/extract")
async def extract_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    # Placeholder logic until we implement extractor service
    return JSONResponse({
        "message": "File received successfully.",
        "filename": file.filename,
        "content_type": file.content_type
    })
