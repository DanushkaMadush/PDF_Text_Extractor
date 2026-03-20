from pydantic import BaseModel
from typing import List , Optional

class ExtractResponse(BaseModel):
    text_blocks: List[str]
    tables: List[List[List[Optional[str]]]]
    ocr_fallback: List[str]