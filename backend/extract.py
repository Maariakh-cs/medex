import re
import spacy
from typing import Dict, List, Optional
from models import PatientInfo, MedicalRecord


# Load the spaCy model for medical text processing
nlp = spacy.load("en_core_web_sm")

class MedicalDataExtractor:
    def __init__(self):
        # Initialize patterns for common medical data
        self.patterns = {
            'patient_name': re.compile(r'(?:patient|name|pt)\s*[:]?\s*([A-Za-z]+ [A-Za-z-]+)', re.I),
            'dob': re.compile(r'(?:dob|date of birth|birth date)\s*[:]?\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})', re.I),
            'patient_id': re.compile(r'(?:patient id|medical record number|mrn)\s*[:]?\s*([A-Za-z0-9-]+)', re.I),
            'diagnosis': re.compile(r'(?:diagnosis|dx)\s*[:]?\s*(.+?)(?=\n|$)', re.I),
            'medication': re.compile(r'(?:medications|prescriptions|rx)\s*[:]?\s*(.+?)(?=\n|$)', re.I),
            'allergy': re.compile(r'(?:allergies|allergy)\s*[:]?\s*(.+?)(?=\n|$)', re.I)
        }

    def extract_patient_info(self, text: str) -> PatientInfo:
        """Extract patient information from text"""
        info = {}
        
        # Extract using regex patterns
        for field, pattern in self.patterns.items():
            if field in ['patient_name', 'dob', 'patient_id']:
                match = pattern.search(text)
                if match:
                    info[field] = match.group(1).strip()
        
        # Additional processing with spaCy
        doc = nlp(text)
        for ent in doc.ents:
            if ent.label_ == "PERSON" and 'patient_name' not in info:
                info['patient_name'] = ent.text
            elif ent.label_ == "DATE" and 'dob' not in info:
                info['dob'] = ent.text
        
        return PatientInfo(
            name=info.get('patient_name'),
            dob=info.get('dob'),
            gender=self._extract_gender(text),
            patient_id=info.get('patient_id'),
            address=self._extract_address(text),
            phone=self._extract_phone(text)
        )

    def extract_medical_data(self, text: str) -> MedicalRecord:
        """Extract medical information from text"""
        record = {}
        
        # Extract using regex patterns
        for field, pattern in self.patterns.items():
            if field in ['diagnosis', 'medication', 'allergy']:
                match = pattern.search(text)
                if match:
                    record[field] = match.group(1).strip()
        
        # Process medications with spaCy
        medications = []
        if 'medication' in record:
            medications = self._process_medications(record['medication'])
        else:
            # Fallback to general extraction
            medications = self._extract_medications_from_text(text)
        
        # Process allergies
        allergies = []
        if 'allergy' in record:
            allergies = [a.strip() for a in record['allergy'].split(',')]
        
        return MedicalRecord(
            diagnosis=record.get('diagnosis'),
            medications=medications,
            procedures=self._extract_procedures(text),
            allergies=allergies,
            lab_results=self._extract_lab_results(text),
            notes=self._extract_notes(text)
        )

    def _extract_gender(self, text: str) -> Optional[str]:
        """Extract patient gender from text"""
        gender_pattern = re.compile(r'(?:sex|gender)\s*[:]?\s*(male|female|m|f)', re.I)
        match = gender_pattern.search(text)
        if match:
            return match.group(1).lower()
        return None

    def _extract_address(self, text: str) -> Optional[str]:
        """Extract patient address from text"""
        address_pattern = re.compile(r'(?:address|residence)\s*[:]?\s*(.+?)(?=\n|$)', re.I)
        match = address_pattern.search(text)
        return match.group(1).strip() if match else None

    def _extract_phone(self, text: str) -> Optional[str]:
        """Extract patient phone number from text"""
        phone_pattern = re.compile(r'(?:phone|telephone)\s*[:]?\s*(\d{3}[-.]\d{3}[-.]\d{4})', re.I)
        match = phone_pattern.search(text)
        return match.group(1) if match else None

    def _process_medications(self, med_text: str) -> List[str]:
        """Process medication text into structured list"""
        # Split by commas, semicolons, or newlines
        meds = re.split(r'[,;\n]', med_text)
        return [m.strip() for m in meds if m.strip()]

    def _extract_procedures(self, text: str) -> List[str]:
        """Extract medical procedures from text"""
        procedure_pattern = re.compile(r'(?:procedure|surgery)\s*[:]?\s*(.+?)(?=\n|$)', re.I)
        matches = procedure_pattern.findall(text)
        return [m.strip() for m in matches]

    def _extract_lab_results(self, text: str) -> List[str]:
        """Extract lab results from text"""
        lab_pattern = re.compile(r'(?:lab|test)\s*[:]?\s*(.+?)(?=\n|$)', re.I)
        matches = lab_pattern.findall(text)
        return [m.strip() for m in matches]

    def _extract_notes(self, text: str) -> Optional[str]:
        """Extract clinical notes from text"""
        notes_pattern = re.compile(r'(?:notes|comments)\s*[:]?\s*(.+?)(?=\n|$)', re.I)
        match = notes_pattern.search(text)
        return match.group(1).strip() if match else None
    
    def extract_text(file_bytes: bytes, file_type: str) -> str:
        """Dispatch function to handle different file types"""
        if file_type == "image/jpeg" or file_type == "image/png":
            return extract_text_from_image(file_bytes)
        elif file_type == "application/pdf":
            return extract_text_from_pdf(file_bytes)
        elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            return extract_text_from_docx(file_bytes)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")