from fastapi import FastAPI
from app.api.v1 import endpoints
from app.core.logging_config import setup_logging

def create_app() -> FastAPI:
    setup_logging()
    
    app = FastAPI(
        title="PDF Text Extractor",
        version="1.0.0",
        description="API for extract text from PDF"
    )
    
    app.include_router(endpoints.router , prefix="/api/v1")
    
    return app

app = create_app()