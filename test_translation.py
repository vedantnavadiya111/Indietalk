import requests
import json

def test_translation():
    url = "http://localhost:8000/translate"
    headers = {"Content-Type": "application/json"}
    
    # Test cases
    test_cases = [
        {
            "text": "यह एक परीक्षण वाक्य है।",
            "expected": "This is a test sentence."
        },
        {
            "text": "मैं आज बाजार जा रहा हूँ।",
            "expected": "I am going to the market today."
        },
        {
            "text": "क्या आप मेरी मदद कर सकते हैं?",
            "expected": "Can you help me?"
        }
    ]
    
    print("Testing translation service...")
    print("-" * 50)
    
    for test in test_cases:
        data = {
            "text": test["text"],
            "config": "default"
        }
        
        try:
            response = requests.post(url, headers=headers, json=data)
            result = response.json()
            
            print(f"Input (Hindi): {test['text']}")
            print(f"Expected: {test['expected']}")
            print(f"Output: {result['translated_text']}")
            print(f"Processing time: {result['processing_time']} seconds")
            print("-" * 50)
            
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            print("-" * 50)

if __name__ == "__main__":
    test_translation() 