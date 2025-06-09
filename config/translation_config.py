from dataclasses import dataclass
from typing import Optional

@dataclass
class TranslationConfig:
    """Configuration for translation parameters."""
    max_length: int = 512
    num_beams: int = 4
    early_stopping: bool = True
    temperature: float = 1.0
    top_k: Optional[int] = None
    top_p: Optional[float] = None
    repetition_penalty: float = 1.0
    length_penalty: float = 1.0
    no_repeat_ngram_size: int = 3
    context_prompt: str = ""  # Prompt to guide the translation context

# Default configuration
DEFAULT_CONFIG = TranslationConfig(
    context_prompt="Translate this text maintaining its original tone:"
)

# Formal context configuration
FORMAL_CONFIG = TranslationConfig(
    num_beams=6,
    temperature=0.8,
    top_k=40,
    top_p=0.9,
    repetition_penalty=1.1,
    context_prompt="Translate this text into formal and professional English:"
)

# Casual context configuration
CASUAL_CONFIG = TranslationConfig(
    temperature=1.2,
    top_k=50,
    top_p=0.95,
    repetition_penalty=1.0,
    context_prompt="Translate this text into casual, conversational English:"
)

# Fast configuration (faster but potentially lower quality)
FAST_CONFIG = TranslationConfig(
    num_beams=1,
    early_stopping=False,
    context_prompt="Translate this text quickly:"
)

# High quality configuration (slower but potentially better quality)
HIGH_QUALITY_CONFIG = TranslationConfig(
    num_beams=8,
    temperature=0.7,
    top_k=50,
    top_p=0.95,
    repetition_penalty=1.2,
    length_penalty=1.2,
    context_prompt="Translate this text with high accuracy and natural flow:"
) 