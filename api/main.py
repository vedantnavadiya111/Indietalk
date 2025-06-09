import logging
import sys
import time
import os
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import uvicorn

# Add the project root to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

from load_model import IndicTransModel
from config.translation_config import (
    TranslationConfig,
    DEFAULT_CONFIG,
    FAST_CONFIG,
    HIGH_QUALITY_CONFIG,
    FORMAL_CONFIG,
    CASUAL_CONFIG
)
from api.config import settings

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,  # Set to DEBUG for more detailed logs
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Hindi-English Translation API",
    description="API for translating Hindi text to English with context-aware settings",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define data models
class TranslationRequest(BaseModel):
    """Request model for translation."""
    text: str
    config: Optional[str] = "default"
    context: Optional[str] = "auto"  # Options: auto, formal, casual

class TranslationResponse(BaseModel):
    """Response model for translation."""
    translated_text: str
    processing_time: float

# Initialize translator
translator = None

@app.on_event("startup")
async def startup_event():
    """Initialize the translator on startup."""
    global translator
    try:
        logger.info("Starting model initialization...")
        translator = IndicTransModel(device=settings.MODEL_DEVICE)
        logger.info("Created IndicTransModel instance")
        
        if not translator.load_model():
            logger.error("Failed to load translation model")
            raise Exception("Failed to load translation model")
        
        logger.info("Translation model loaded successfully")
    except Exception as e:
        logger.error(f"Error during startup: {str(e)}")
        logger.exception("Detailed traceback:")
        raise

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler."""
    logger.error(f"Global error: {str(exc)}")
    logger.exception("Detailed traceback:")
    return JSONResponse(
        status_code=500,
        content={"detail": f"Internal server error: {str(exc)}"}
    )

@app.post("/translate", response_model=TranslationResponse)
async def translate(request: TranslationRequest):
    """
    Translate Hindi text to English.
    
    Args:
        request (TranslationRequest): The translation request containing:
            - text: Hindi text to translate
            - config: Translation configuration ("default", "fast", or "high_quality")
            - context: Translation context ("auto", "formal", or "casual")
    
    Returns:
        TranslationResponse: The translation response containing:
            - translated_text: Translated English text
            - processing_time: Time taken for translation in seconds
    """
    try:
        if not translator:
            raise HTTPException(status_code=503, detail="Translation service not ready")
        
        # Set translation configuration
        config_map = {
            "default": DEFAULT_CONFIG,
            "fast": FAST_CONFIG,
            "high_quality": HIGH_QUALITY_CONFIG
        }
        
        context_map = {
            "auto": DEFAULT_CONFIG,
            "formal": FORMAL_CONFIG,
            "casual": CASUAL_CONFIG
        }
        
        if request.config not in config_map:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid config. Must be one of: {list(config_map.keys())}"
            )
            
        if request.context not in context_map:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid context. Must be one of: {list(context_map.keys())}"
            )
        
        # Set base configuration
        base_config = config_map[request.config]
        
        # If context is not auto, override with context-specific settings
        if request.context != "auto":
            context_config = context_map[request.context]
            # Merge configurations, preferring context-specific settings
            base_config = TranslationConfig(
                **{
                    **base_config.__dict__,
                    "context_prompt": context_config.context_prompt,
                    "temperature": context_config.temperature,
                    "top_k": context_config.top_k,
                    "top_p": context_config.top_p,
                    "repetition_penalty": context_config.repetition_penalty
                }
            )
        
        # Set configuration
        translator.set_config(base_config)
        
        # Perform translation
        start_time = time.time()
        translated_text = translator.translate(request.text)
        processing_time = time.time() - start_time
        
        return TranslationResponse(
            translated_text=translated_text,
            processing_time=processing_time
        )
        
    except Exception as e:
        logger.error(f"Translation error: {str(e)}")
        logger.exception("Detailed traceback:")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "model_loaded": translator is not None}

if __name__ == "__main__":
    uvicorn.run(app, host=settings.HOST, port=settings.PORT) 