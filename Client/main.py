import requests
import json

# === CONFIG CONSTANTS ===
API_URL = "http://127.0.0.1:8000"  # Deine lokale API
PDF_PATH = r"C:\Users\Roy von der Locht\Dropbox\Workspace\priv\Gesundheit\BEFUNDProfDirkHempel.pdf"          # Pfad zur PDF-Datei
OUTPUT_PATH = r"C:\Users\Roy von der Locht\Dropbox\Workspace\DATA\SoftwareEntwicklung\SectionFinalProject\Files\extraktion.json"    # Pfad zur gespeicherten Antwort

# === OPEN FILE AND CALL API ===
with open(PDF_PATH, "rb") as pdf_file:
    files = {"file": ("BEFUNDProfDirkHempel.pdf", pdf_file)}
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
