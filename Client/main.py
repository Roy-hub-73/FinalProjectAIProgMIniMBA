import requests
import json

# === CONFIG CONSTANTS ===
API_URL = "http://127.0.0.1:8000"           # Replace by your host address
PDF_FILE_NAME = "your-filename-here"        # Just the filename, like "input_doctorsletter.pdf"
PDF_PATH = r"your-path-and-file-here"       # Path to PDF file to read, like "c://Files/input_doctorsletter.pdf"
OUTPUT_PATH = r"your-path-and-file-here"    # Path where to save the output to, like "c://Files/output.json"

# === OPEN FILE AND CALL API ===
with open(PDF_PATH, "rb") as pdf_file:
    files = {"file": (PDF_FILE_NAME, pdf_file)}
    response = requests.post(f"{API_URL}/extract_from_pdf", files=files)

# === CHECK ANSWER AND SAVE JSON FILE ===
if response.status_code == 200:
    data = response.json()
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"✅ Extraction saved under: {OUTPUT_PATH}")
else:
    print(f"❌ Error: {response.status_code}")
    print(response.text)
