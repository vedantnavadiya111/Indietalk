from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from cachetools import LRUCache, cached
from pydantic import BaseModel
from typing import Optional
import logging
import time
from datetime import datetime
from pathlib import Path
from prometheus_fastapi_instrumentator import Instrumentator
from load_model import IndicTransModel

# Configure logging
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_dir / "api_logs.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="IndicTrans Translation API",
    description="Optimized Hindi to English translation service",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this to specific domains for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize translation model
translator = IndicTransModel()
if not translator.load_model():
    logger.error("Failed to initialize translation model")
    raise RuntimeError("Translation model initialization failed")

# Initialize cache
cache = LRUCache(maxsize=1000)

class TranslationRequest(BaseModel):
    text: str
    config: Optional[str] = "default"  # "default", "fast", or "high_quality"

@cached(cache)
def cached_translation(text: str, config: str) -> str:
    """
    Cached translation function with configurable quality settings.
    """
    try:
        # Set configuration based on request
        if config == "fast":
            from config.translation_config import FAST_CONFIG
            translator.set_config(FAST_CONFIG)
        elif config == "high_quality":
            from config.translation_config import HIGH_QUALITY_CONFIG
            translator.set_config(HIGH_QUALITY_CONFIG)
        else:
            from config.translation_config import DEFAULT_CONFIG
            translator.set_config(DEFAULT_CONFIG)
        
        return translator.translate(text)
    except Exception as e:
        logger.error(f"Translation error: {str(e)}")
        raise

@app.get("/health")
async def health_check():
    """
    Health check endpoint to ensure the API is running.
    """
    return {"status": "ok", "model_loaded": translator.model is not None}

@app.post("/translate")
async def translate(request: TranslationRequest):
    """
    Optimized translation endpoint with caching.
    """
    try:
        # Use cached translation to reduce redundant computations
        translated_text = cached_translation(request.text, request.config)
        return {"translated_text": translated_text}
    except Exception as e:
        logger.error(f"Translation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Translation failed: {str(e)}")

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """
    Middleware to log all requests for monitoring and debugging.
    """
    start_time = time.time()
    logger.info(f"Request: {request.method} {request.url}")
    
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        
        # Log response details
        logger.info(
            f"Response: {request.method} {request.url} - Status: {response.status_code} - Time: {process_time:.2f}s"
        )
        
        # Add response time to headers
        response.headers["X-Process-Time"] = str(process_time)
        return response
        
    except Exception as e:
        process_time = time.time() - start_time
        logger.error(
            f"Error: {request.method} {request.url} - Error: {str(e)} - Time: {process_time:.2f}s"
        )
        raise

@app.get("/logs", include_in_schema=False)
async def get_logs(lines: int = 100):
    """
    Endpoint to retrieve the last N lines of the log file.
    """
    try:
        log_file = log_dir / "api_logs.log"
        if not log_file.exists():
            return {"logs": ["No logs available yet."]}
            
        with open(log_file, "r") as f:
            logs = f.readlines()[-lines:]
        return {"logs": logs}
    except Exception as e:
        logger.error(f"Failed to fetch logs: {str(e)}")
        raise HTTPException(status_code=500, detail="Unable to fetch logs.")

# Initialize Prometheus monitoring
Instrumentator().instrument(app).expose(app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 