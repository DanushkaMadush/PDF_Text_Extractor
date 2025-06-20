import pdfplumber
import fitz
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import tempfile
import os
import logging
import camelot

logger = logging.getLogger(__name__)

def extract_text_pdfplumber(filepath : str):
    text_blocks = []
    tables = []
    
    try:
        with pdfplumber.open(filepath) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                table = page.extract_tables()
                text_blocks.append(text if text else "")
                tables.append(table if table else [])
    except Exception as e:
        logger.error(f"pdfplumber failed: {e}")
        
    return text_blocks , tables

def extract_text_ocr(filepath : str):
    ocr_texts = []
    
    try:
        images = convert_from_path(filepath)
        for image in images:
            ocr_result = pytesseract.image_to_string(image)
            ocr_texts.append(ocr_result)
            
    except Exception as e:
        logger.error(f"OCR failed: {e}")
        
    return ocr_texts

def extract_tables_camelot(filepath : str):
    extracted_tables = []
    
    try:
        tables = camelot.read_pdf(filepath , pages=all ,flavor='lattice')
        
        for table in tables:
                extracted_tables.append(table.data)
                
    except Exception as e:
        logger.error(f"Camelot failed to extract tables: {e}")
        
    return extracted_tables 

def process_pdf(uploaded_file) -> dict:
    with tempfile.NamedTemporaryFile(delete=False , suffix=".pdf") as tmp:
        tmp.write(uploaded_file.file.read())
        tmp_path = tmp.name
        
    logger.info(f"Processing PDF:{uploaded_file.filename}")
    
    text_blocks , tables = extract_text_pdfplumber(tmp_path)
    
    if all(not text for text in text_blocks):
        logger.warning("No text found with pdfplumber. Using OCR Fallback")
        ocr_fallback = extract_text_ocr(tmp_path)
        
    else:
        ocr_fallback = []
        
    os.remove(tmp_path)
    
    return {
        "text_blocks" : text_blocks,
        "tables" : tables,
        "ocr_fallback" : ocr_fallback   
    }    