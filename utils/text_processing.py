import re
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def clean_text(text: str) -> str:
    """
    Clean input text by removing extra whitespace and normalizing characters.
    
    Args:
        text (str): Input text to clean
        
    Returns:
        str: Cleaned text
    """
    try:
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove leading/trailing whitespace
        text = text.strip()
        return text
    except Exception as e:
        logger.error(f"Error cleaning text: {str(e)}")
        return text

def split_long_text(text: str, max_length: int = 500) -> list:
    """
    Split long text into smaller chunks that can be processed by the model.
    
    Args:
        text (str): Input text to split
        max_length (int): Maximum length of each chunk
        
    Returns:
        list: List of text chunks
    """
    try:
        # Split by sentences if possible
        sentences = re.split(r'(?<=[।।!?])', text)
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            if len(current_chunk) + len(sentence) <= max_length:
                current_chunk += sentence
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence
        
        if current_chunk:
            chunks.append(current_chunk.strip())
            
        return chunks
    except Exception as e:
        logger.error(f"Error splitting text: {str(e)}")
        return [text] 