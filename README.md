# IndieTalk Translator

A powerful and easy-to-use Hindi to English translation service using the IndicTrans model.

## Description
IndieTalk is a powerful and easy-to-use tool that provides accurate and real-time language translation.

##Screenshots
<img width="1919" height="968" alt="Screenshot 2025-05-07 202211" src="https://github.com/user-attachments/assets/e1890b45-4560-4e59-b26d-d61e0aac5de8" />
<img width="1919" height="972" alt="Screenshot 2025-05-07 202225" src="https://github.com/user-attachments/assets/9aee931a-4d3f-4b43-a8fa-e745abd41010" />
<img width="563" height="831" alt="Screenshot 2025-05-07 202239" src="https://github.com/user-attachments/assets/87eb5493-078d-413d-b86a-8970e62b006c" />
<img width="646" height="680" alt="Screenshot 2025-05-07 202255" src="https://github.com/user-attachments/assets/072989f0-a6d6-4aa7-9bdb-6cddf8d12076" />
<img width="1913" height="969" alt="Screenshot 2025-05-07 202341" src="https://github.com/user-attachments/assets/192194fc-8f0b-4d37-8d01-703251909fd0" />


## Features
- Supports Hindi to English translation
- Fast and reliable translation algorithms
- Simple and intuitive user interface
- RESTful API for easy integration
- Multiple translation configurations for different use cases

## Installation

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies using one of these methods:

   a. Using pip:
   ```bash
   pip install -r requirements.txt
   ```

   b. Using setup.py:
   ```bash
   pip install -e .
   ```

3. Verify installation:
```bash
python -c "import torch; import transformers; import numpy; print('All dependencies installed successfully')"
```

## Running the API

1. Start the API server:
```bash
python -m api.main
```

2. Access the API:
- API documentation: http://localhost:8000/docs
- Alternative documentation: http://localhost:8000/redoc
- Health check: http://localhost:8000/health

## Usage

### Translation API

Send a POST request to `/translate`:

```bash
curl -X POST "http://localhost:8000/translate" \
     -H "Content-Type: application/json" \
     -d '{"text": "यह एक परीक्षण वाक्य है।", "config": "default"}'
```

Response:
```json
{
    "translated_text": "This is a test sentence.",
    "processing_time": 0.345
}
```

### Configuration Options

- `default`: Balanced translation settings
- `fast`: Optimized for speed
- `high_quality`: Optimized for translation quality

## Troubleshooting

1. **Missing Dependencies**
   - If you see errors about missing modules, run:
     ```bash
     pip install -r requirements.txt
     ```

2. **CUDA/GPU Issues**
   - If you encounter CUDA-related errors, try running with CPU:
     ```bash
     export MODEL_DEVICE=cpu  # On Windows: set MODEL_DEVICE=cpu
     python -m api.main
     ```

3. **Memory Issues**
   - If you encounter memory errors, try using the `fast` configuration
   - Reduce batch size in the translation config

## Project Structure

- `api/` - FastAPI application
  - `config.py` - API configuration
  - `main.py` - API endpoints
- `config/` - Translation configuration
- `tests/` - Test cases and evaluation
- `utils/` - Utility functions
- `load_model.py` - Model loading and translation
- `requirements.txt` - Project dependencies
- `setup.py` - Installation script

## Requirements

- Python 3.8 or higher
- CUDA-capable GPU (optional, for faster processing)
- Dependencies listed in requirements.txt

## Contributing
Interested in contributing? Great! Please check out the CONTRIBUTING.md for details.

## License
Distributed under the Apache 2.0 License. See `LICENSE` for more information.

## Contact
Vedant Navadiya - [vedantnavadiya2004@gmail.com]
