from setuptools import setup, find_packages

setup(
    name="indietalk-translator",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "numpy==1.24.3",
        "torch==2.1.0",
        "torchvision==0.16.0",
        "transformers==4.35.2",
        "indic-nlp-library==0.0.1",
        "sentencepiece==0.1.99",
        "fastapi==0.104.1",
        "uvicorn==0.24.0",
        "pydantic==2.4.2",
        "python-dotenv==1.0.0"
    ],
    python_requires=">=3.8,<3.12",
    author="Your Name",
    author_email="your.email@example.com",
    description="A Hindi to English translation service using IndicTrans model",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/indietalk-translator",
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
) 