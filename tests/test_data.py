from dataclasses import dataclass
from typing import List, Dict, Tuple

@dataclass
class TestCase:
    """A test case for translation evaluation."""
    hindi: str
    english: str
    category: str
    difficulty: str  # 'easy', 'medium', 'hard'

# Test cases organized by category
TEST_CASES = [
    # Basic sentences
    TestCase(
        hindi="यह एक परीक्षण वाक्य है।",
        english="This is a test sentence.",
        category="basic",
        difficulty="easy"
    ),
    TestCase(
        hindi="भारत एक सुंदर देश है।",
        english="India is a beautiful country.",
        category="basic",
        difficulty="easy"
    ),
    TestCase(
        hindi="मुझे पढ़ाई करना पसंद है।",
        english="I like to study.",
        category="basic",
        difficulty="easy"
    ),
    
    # Complex sentences
    TestCase(
        hindi="जब मैं छोटा था, मैं हर रोज़ पार्क जाता था।",
        english="When I was young, I used to go to the park every day.",
        category="complex",
        difficulty="medium"
    ),
    TestCase(
        hindi="यदि आप मेहनत करेंगे, तो आप सफल होंगे।",
        english="If you work hard, you will succeed.",
        category="complex",
        difficulty="medium"
    ),
    
    # Technical sentences
    TestCase(
        hindi="कृत्रिम बुद्धिमत्ता भविष्य की तकनीक है।",
        english="Artificial intelligence is the technology of the future.",
        category="technical",
        difficulty="hard"
    ),
    TestCase(
        hindi="मशीन लर्निंग एल्गोरिदम डेटा से सीखते हैं।",
        english="Machine learning algorithms learn from data.",
        category="technical",
        difficulty="hard"
    )
]

# Expected translation time ranges (in seconds) by difficulty
EXPECTED_TIMES = {
    "easy": (0.1, 0.5),
    "medium": (0.3, 1.0),
    "hard": (0.5, 2.0)
}

# Categories for evaluation
CATEGORIES = ["basic", "complex", "technical"]
DIFFICULTIES = ["easy", "medium", "hard"] 