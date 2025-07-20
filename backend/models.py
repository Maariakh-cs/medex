from pydantic import BaseModel
from typing import List, Optional

class PatientInfo(BaseModel):
    name: Optional[str]
    dob: Optional[str]
    gender: Optional[str]
    patient_id: Optional[str]
    address: Optional[str]
    phone: Optional[str]

class MedicalRecord(BaseModel):
    diagnosis: Optional[str]
    medications: List[str] = []
    procedures: List[str] = []
    allergies: List[str] = []
    lab_results: List[str] = []
    notes: Optional[str]

class ExtractionResponse(BaseModel):
    patient_info: PatientInfo
    medical_record: MedicalRecord
    raw_text: Optional[str]
    success: bool
    message: Optional[str]