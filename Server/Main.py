import os
import tempfile
import json
from typing import Optional, List, Dict

from openai import OpenAI
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel, Field, ValidationError
from pdf2image import convert_from_bytes
import pytesseract
import uvicorn

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


# === CONFIG ===
client = OpenAI(api_key="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")  # must be set

# === Schema definitions ===
class Medication(BaseModel):
    name: str
    dose: Optional[str] = None
    frequency: Optional[str] = None
    route: Optional[str] = None

class LabValue(BaseModel):
    test_name: str
    value: str
    unit: Optional[str] = None
    reference_range: Optional[str] = None
    date: Optional[str] = None

class Anamnesis(BaseModel):
    smoking_status: Optional[str] = None
    allergies: Optional[str] = None
    past_conditions: Optional[List[str]] = None

class ExtractionResult(BaseModel):
    medications: List[Medication] = Field(default_factory=list)
    lab_values: List[LabValue] = Field(default_factory=list)
    anamnesis: Anamnesis = Field(default_factory=Anamnesis)


# === FastAPI app ===
app = FastAPI(title="Clinical Document IE Prototype")


def ocr_pdf_bytes(pdf_bytes: bytes) -> str:
    """Convert PDF to text via image-based OCR."""
    try:
        images = convert_from_bytes(
            pdf_bytes,
            dpi=300,
            poppler_path=r"C:\Program Files\poppler-24.08.0\Library\bin"
        )
    except Exception as e:
        raise RuntimeError(f"PDF to image conversion failed: {e}")
    text_chunks = []
    for img in images:
        text = pytesseract.image_to_string(img)
        text_chunks.append(text)
    return "\n\n".join(text_chunks)


def build_prompt(document_text: str) -> str:
    """Prompt to extract structured fields. Adjust few-shot or instructions here."""
    system_instructions = (
        "You are a clinical information extraction assistant. "
        "Given the text of a doctor letter / report, extract the following into JSON:\n"
        "1. Medications with name, dose, frequency, route.\n"
        "2. Laboratory values: test_name, value, unit, reference_range, date.\n"
        "3. Anamnesis: smoking status, allergies, past medical conditions.\n"
        "Output strictly valid JSON matching this schema:\n"
        "{\n"
        "  \"medications\": [{\"name\":\"...\",\"dose\":\"...\",\"frequency\":\"...\",\"route\":\"...\"}],\n"
        "  \"lab_values\": [{\"test_name\":\"...\",\"value\":\"...\",\"unit\":\"...\",\"reference_range\":\"...\",\"date\":\"...\"}],\n"
        "  \"anamnesis\": {\"smoking_status\":\"...\",\"allergies\":\"...\",\"past_conditions\":[\"...\", ...]}\n"
        "}\n"
        "If a field is missing, use null or empty list. Do not add any commentary. For laboratory values choose only those which are outside the recommended range, maximum of 10 values. For the past medical conditions scan the text and identify diagnosis like cancer or other diseases."
    )
    return f"{system_instructions}\n\nDocument:\n{document_text}"


def call_openai_extract(prompt: str) -> dict:
    """Call OpenAI ChatCompletion to get the extraction."""
    try:
        resp = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
            max_tokens=1000,
        )
        content = resp.choices[0].message.content
        # Get rid of Markdown-Wrapper
        if content.startswith("```json"):
            content = content[len("```json"):].strip()
        if content.endswith("```"):
            content = content[:-3].strip()

        return json.loads(content)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse JSON from model output: {e}. Raw output: {resp}")
    except Exception as e:
        raise RuntimeError(f"OpenAI API error: {e}")


def validate_extraction(raw: dict) -> ExtractionResult:
    """Validate and coerce the raw dictionary into typed model. Raises on mismatch."""
    return ExtractionResult.parse_obj(raw)


# === Endpoints ===
@app.post("/extract_from_pdf", response_model=ExtractionResult)
async def extract_from_pdf(file: UploadFile = File(...)):
    content = await file.read()
    try:
        ocr_text = ocr_pdf_bytes(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    prompt = build_prompt(ocr_text)
    try:
        raw = call_openai_extract(prompt)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    try:
        structured = validate_extraction(raw)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=f"Schema validation failed: {e}")

    return structured


# @app.get("/ping")
# def ping():
#     return {"status": "alive"}
if __name__ == "__main__":
    uvicorn.run("Main:app", reload=True)