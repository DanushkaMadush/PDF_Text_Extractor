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

def is_scanned_pdf(filepath : str , threshold : float = 0.7) -> bool:
    # If most pages have no text , assume it as a scanned doc
    try:
        doc = fitz.open(filepath)
        no_text_pages = sum(1 for page in doc if not page.get_text().strip())
        ratio = no_text_pages / len(doc)
        logger.info(f"Scanned page ratio: {ratio:.2f}")
        return ratio >= threshold
    
    except Exception as e:
        logger.error(f"Failed to detect scanned PDF: {e}")
        return False 

def process_pdf(uploaded_file) -> dict:
    with tempfile.NamedTemporaryFile(delete=False , suffix=".pdf") as tmp:
        tmp.write(uploaded_file.file.read())
        tmp_path = tmp.name
        
    logger.info(f"Processing PDF:{uploaded_file.filename}")
    
    is_scanned = is_scanned_pdf(tmp_path)
    logger.info(f"PDF classified as: {'scanned' if is_scanned else 'digital'}")
    
    if is_scanned:
        text_blocks = extract_text_ocr(tmp_path)
        tables = []
    else:
        text_blocks , _ = extract_text_pdfplumber(tmp_path)
        tables = extract_tables_camelot(tmp_path)
        
    os.remove(tmp_path)
    
    return {
        "text_blocks" : text_blocks,
        "tables" : tables,
        "ocr_fallback" : [] if not is_scanned else text_blocks  
    }    