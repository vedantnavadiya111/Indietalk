import os
import sys
import logging
import torch
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def setup_environment():
    """Set up the necessary environment for the IndieTalk project."""
    try:
        # Check if CUDA is available for GPU acceleration
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        logger.info(f"Using device: {device}")

        # Create necessary directories
        base_dir = Path("indietalk")
        data_dir = base_dir / "data"
        models_dir = base_dir / "models"

        for directory in [base_dir, data_dir, models_dir]:
            directory.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created directory: {directory}")

        logger.info("Environment setup complete.")
        return True

    except Exception as e:
        logger.error(f"Error during environment setup: {str(e)}")
        return False

if __name__ == "__main__":
    success = setup_environment()
    if not success:
        sys.exit(1) 