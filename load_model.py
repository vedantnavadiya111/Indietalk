import logging
import torch
from transformers import MBartForConditionalGeneration, MBart50TokenizerFast
from pathlib import Path
from typing import Dict, Any, List, Union, Optional
from utils.text_processing import clean_text, split_long_text
from config.translation_config import TranslationConfig, DEFAULT_CONFIG

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class IndicTransModel:
    def __init__(self, device='cuda' if torch.cuda.is_available() else 'cpu'):
        """Initialize the IndicTrans model and tokenizer."""
        self.device = device
        self.model = None
        self.tokenizer = None
        self.MODEL_NAME = "facebook/mbart-large-50-many-to-many-mmt"
        self.src_lang = "hi_IN"  # Source language: Hindi
        self.tgt_lang = "en_XX"  # Target language: English
        self.config = DEFAULT_CONFIG

    def load_model(self):
        """Load the IndicTrans model and tokenizer."""
        try:
            logger.info("Downloading and loading the IndicTrans model...")
            
            # Load model and tokenizer
            self.model = MBartForConditionalGeneration.from_pretrained(self.MODEL_NAME)
            self.tokenizer = MBart50TokenizerFast.from_pretrained(self.MODEL_NAME)
            
            # Configure tokenizer
            self.tokenizer.src_lang = self.src_lang
            self.tokenizer.tgt_lang = self.tgt_lang
            
            # Move model to device
            self.model = self.model.to(self.device)
            
            logger.info(f"Model loaded successfully on device: {self.device}")
            return True
            
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            return False

    def set_config(self, config: TranslationConfig):
        """Set translation configuration parameters."""
        self.config = config
        logger.info("Translation configuration updated")

    def preprocess_text(self, text: str) -> Dict[str, torch.Tensor]:
        """
        Preprocess input text for the IndicTrans model.
        
        Args:
            text (str): Input text to be translated
            
        Returns:
            Dict[str, torch.Tensor]: Tokenized and encoded input ready for the model
        """
        try:
            # Clean the input text
            text = clean_text(text)
            
            # Add context prompt if specified
            if self.config.context_prompt:
                text = f"{self.config.context_prompt}\n{text}"
            
            # Tokenize and encode the input text
            inputs = self.tokenizer(
                text,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=self.config.max_length
            )
            
            # Move inputs to the selected device
            inputs = {key: value.to(self.device) for key, value in inputs.items()}
            return inputs
            
        except Exception as e:
            logger.error(f"Error preprocessing text: {str(e)}")
            raise

    def translate_chunk(self, inputs: Dict[str, torch.Tensor]) -> str:
        """
        Translate a single chunk of text.
        
        Args:
            inputs (Dict[str, torch.Tensor]): Preprocessed input text
            
        Returns:
            str: Translated text
        """
        try:
            with torch.no_grad():
                translated_tokens = self.model.generate(
                    **inputs,
                    max_length=self.config.max_length,
                    num_beams=self.config.num_beams,
                    early_stopping=self.config.early_stopping,
                    temperature=self.config.temperature,
                    top_k=self.config.top_k,
                    top_p=self.config.top_p,
                    repetition_penalty=self.config.repetition_penalty,
                    length_penalty=self.config.length_penalty,
                    no_repeat_ngram_size=self.config.no_repeat_ngram_size,
                    forced_bos_token_id=self.tokenizer.lang_code_to_id[self.tgt_lang]
                )
            
            return self.tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)[0]
            
        except Exception as e:
            logger.error(f"Error translating chunk: {str(e)}")
            raise

    def translate(self, text: str) -> str:
        """Translate text from Hindi to English."""
        if not self.model or not self.tokenizer:
            logger.error("Model or tokenizer not loaded")
            return None
            
        try:
            # Split long text into chunks if necessary
            text_chunks = split_long_text(text)
            translations = []
            
            for chunk in text_chunks:
                # Preprocess the text chunk
                inputs = self.preprocess_text(chunk)
                
                # Translate the chunk
                translation = self.translate_chunk(inputs)
                translations.append(translation)
            
            # Join translations if there were multiple chunks
            return " ".join(translations)
            
        except Exception as e:
            logger.error(f"Error during translation: {str(e)}")
            return None

def main():
    # Initialize and load model
    translator = IndicTransModel()
    if translator.load_model():
        logger.info("Model loaded successfully. Ready for translation.")
        
        # Test translation with default config
        example_text = "यह एक परीक्षण वाक्य है।"  # Example input text in Hindi
        translation = translator.translate(example_text)
        logger.info(f"Input: {example_text}")
        logger.info(f"Translation: {translation}")
        
        # Test translation with high quality config
        from config.translation_config import HIGH_QUALITY_CONFIG
        translator.set_config(HIGH_QUALITY_CONFIG)
        high_quality_translation = translator.translate(example_text)
        logger.info(f"High quality translation: {high_quality_translation}")
    else:
        logger.error("Failed to load model")
        return

if __name__ == "__main__":
    main() 