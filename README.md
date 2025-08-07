# FinalProjectAIProgMIniMBA
My final project for Sections AI Programmers Mini MBA

## Introduction
This project aims to extract relevant medical data from a typical doctors letter, which has structured parts as well as free text. The goal is, to analyze medical documents and save relevant information into a big database for later scientific purposes. Using OpenAI's GPT-4 model, the system can parse any medical PDF-document, and convert it into a standardized structure that includes laboratory values (with amounts, units and reference values), medications if stated in the doctor letter and mentioned medical indications (like cancer and others). This makes it easy to store, search, and manage medical information in a database system.
We use a server, which is an API, and a client, which calls the API, passes over the PDF-file and receives a JSON file as output. This JSON file is parsed and saved locally.

## Prerequisites
- Python 3.11 or higher
- OpenAI API key

## Installation

### Backend Setup
1. Navigate to the backend directory:
```bash
cd <directory where to find SectionFinalProject>
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

4. Set up your OpenAI API key:
```bash
export OPENAI_API_KEY='your-api-key-here'  # On Windows, use: set OPENAI_API_KEY=your-api-key-here
```

### Frontend Setup
1. Set API_URL
```bash
API_URL = "your-local-api-address" 	#like "http://127.0.0.1:8000"
```

2. Set input file and output-path
```bash
PDF_PATH = r"your-file-including-directory"  # like "c:\files\test.pdf"
OUTPUT_PATH =r"your-outputfilename-including-directory"  # like "c:\files\result.json"
```

## Usage
The backend provides an API endpoint that accepts a PDF-file and returns structured data. The client hands over the PDF-file and receives the analytical output to save in in a local file.
Make sure the API-Server-App is running before you start the client.

## License
This project is provided as the final project for the Section Programmers AI Mini MBA. 
