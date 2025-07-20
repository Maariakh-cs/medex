from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Optional
import logging
from models import ExtractionResponse
from ocr import extract_text
from extract import MedicalDataExtractor

app = FastAPI(
    title="Medical Data Extractor API",
    description="API for extracting structured medical data from documents",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize extractor
extractor = MedicalDataExtractor()

@app.post("/extract", response_model=ExtractionResponse)
async def extract_medical_data(file: UploadFile = File(...)):
    """Endpoint for processing medical documents"""
    try:
        # Read file content
        file_bytes = await file.read()
    
        # Extract raw text from file
        raw_text = extract_text(file_bytes, file.content_type)
        
        # Extract structured data
        patient_info = extractor.extract_patient_info(raw_text)
        medical_record = extractor.extract_medical_data(raw_text)
        
        return ExtractionResponse(
            patient_info=patient_info,
            medical_record=medical_record,
            raw_text=raw_text,
            success=True,
            message="Extraction successful"
        )
    except Exception as e:
        logging.error(f"Error processing file: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail=f"Error processing file: {str(e)}"
        )

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)