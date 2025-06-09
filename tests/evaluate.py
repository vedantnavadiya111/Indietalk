import time
import logging
from typing import Dict, List, Tuple
from dataclasses import dataclass
from load_model import IndicTransModel
from config.translation_config import DEFAULT_CONFIG, FAST_CONFIG, HIGH_QUALITY_CONFIG
from tests.test_data import TestCase, TEST_CASES, EXPECTED_TIMES, CATEGORIES, DIFFICULTIES

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class TestResult:
    """Results of a single test case."""
    test_case: TestCase
    translation: str
    translation_time: float
    is_correct: bool
    error_message: str = ""

@dataclass
class EvaluationResults:
    """Aggregated evaluation results."""
    total_tests: int
    correct_translations: int
    average_time: float
    category_results: Dict[str, Dict[str, int]]
    difficulty_results: Dict[str, Dict[str, int]]
    failed_cases: List[TestResult]

def evaluate_translation(translator: IndicTransModel, test_case: TestCase) -> TestResult:
    """
    Evaluate a single test case.
    
    Args:
        translator: The IndicTransModel instance
        test_case: The test case to evaluate
        
    Returns:
        TestResult: Results of the evaluation
    """
    try:
        start_time = time.time()
        translation = translator.translate(test_case.hindi)
        translation_time = time.time() - start_time
        
        # Simple correctness check (can be enhanced with more sophisticated metrics)
        is_correct = translation.lower().strip() == test_case.english.lower().strip()
        
        return TestResult(
            test_case=test_case,
            translation=translation,
            translation_time=translation_time,
            is_correct=is_correct
        )
        
    except Exception as e:
        logger.error(f"Error evaluating test case: {str(e)}")
        return TestResult(
            test_case=test_case,
            translation="",
            translation_time=0,
            is_correct=False,
            error_message=str(e)
        )

def run_evaluation(translator: IndicTransModel) -> EvaluationResults:
    """
    Run a complete evaluation of the translation model.
    
    Args:
        translator: The IndicTransModel instance
        
    Returns:
        EvaluationResults: Aggregated evaluation results
    """
    results = []
    total_time = 0
    
    # Initialize category and difficulty counters
    category_results = {cat: {"total": 0, "correct": 0} for cat in CATEGORIES}
    difficulty_results = {diff: {"total": 0, "correct": 0} for diff in DIFFICULTIES}
    
    # Run all test cases
    for test_case in TEST_CASES:
        result = evaluate_translation(translator, test_case)
        results.append(result)
        
        # Update statistics
        total_time += result.translation_time
        category_results[test_case.category]["total"] += 1
        difficulty_results[test_case.difficulty]["total"] += 1
        
        if result.is_correct:
            category_results[test_case.category]["correct"] += 1
            difficulty_results[test_case.difficulty]["correct"] += 1
    
    # Calculate final statistics
    total_tests = len(results)
    correct_translations = sum(1 for r in results if r.is_correct)
    average_time = total_time / total_tests if total_tests > 0 else 0
    
    return EvaluationResults(
        total_tests=total_tests,
        correct_translations=correct_translations,
        average_time=average_time,
        category_results=category_results,
        difficulty_results=difficulty_results,
        failed_cases=[r for r in results if not r.is_correct]
    )

def print_evaluation_results(results: EvaluationResults):
    """Print evaluation results in a readable format."""
    print("\n=== Translation Evaluation Results ===")
    print(f"Total Tests: {results.total_tests}")
    print(f"Correct Translations: {results.correct_translations}")
    print(f"Accuracy: {(results.correct_translations / results.total_tests * 100):.2f}%")
    print(f"Average Translation Time: {results.average_time:.3f} seconds")
    
    print("\n=== Results by Category ===")
    for category, stats in results.category_results.items():
        accuracy = (stats["correct"] / stats["total"] * 100) if stats["total"] > 0 else 0
        print(f"{category.capitalize()}: {stats['correct']}/{stats['total']} ({accuracy:.2f}%)")
    
    print("\n=== Results by Difficulty ===")
    for difficulty, stats in results.difficulty_results.items():
        accuracy = (stats["correct"] / stats["total"] * 100) if stats["total"] > 0 else 0
        print(f"{difficulty.capitalize()}: {stats['correct']}/{stats['total']} ({accuracy:.2f}%)")
    
    if results.failed_cases:
        print("\n=== Failed Cases ===")
        for case in results.failed_cases:
            print(f"\nInput: {case.test_case.hindi}")
            print(f"Expected: {case.test_case.english}")
            print(f"Got: {case.translation}")
            if case.error_message:
                print(f"Error: {case.error_message}")

def main():
    """Run the evaluation with different configurations."""
    # Initialize translator
    translator = IndicTransModel()
    if not translator.load_model():
        logger.error("Failed to load model")
        return
    
    # Test with default configuration
    print("\n=== Testing with Default Configuration ===")
    results = run_evaluation(translator)
    print_evaluation_results(results)
    
    # Test with fast configuration
    print("\n=== Testing with Fast Configuration ===")
    translator.set_config(FAST_CONFIG)
    results = run_evaluation(translator)
    print_evaluation_results(results)
    
    # Test with high quality configuration
    print("\n=== Testing with High Quality Configuration ===")
    translator.set_config(HIGH_QUALITY_CONFIG)
    results = run_evaluation(translator)
    print_evaluation_results(results)

if __name__ == "__main__":
    main() 