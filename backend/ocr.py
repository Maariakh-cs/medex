import easyocr
from pdf2image import convert_from_bytes
from io import BytesIO
import docx
from typing import Union

class OCRProcessor:
    def __init__(self):
        # Initialize EasyOCR reader
        self.reader = easyocr.Reader(['en'])  # Add more languages if needed
    
    def extract_text_from_image(self, image_bytes: bytes) -> str:
        """Extract text from image using EasyOCR"""
        result = self.reader.readtext(image_bytes)
        return " ".join([entry[1] for entry in result])

    def extract_text_from_pdf(self, pdf_bytes: bytes) -> str:
        """Extract text from PDF by converting pages to images"""
        images = convert_from_bytes(pdf_bytes)
        full_text = []
        for img in images:
            # Convert PIL image to bytes
            img_byte_arr = BytesIO()
            img.save(img_byte_arr, format='PNG')
            text = self.extract_text_from_image(img_byte_arr.getvalue())
            full_text.append(text)
        return "\n\n".join(full_text)

    def extract_text_from_docx(self, docx_bytes: bytes) -> str:
        """Extract text from DOCX file"""
        doc = docx.Document(BytesIO(docx_bytes))
        return "\n".join([para.text for para in doc.paragraphs])

    def extract_text(self, file_bytes: bytes, file_type: str) -> str:
        """Dispatch function to handle different file types"""
        if file_type in ("image/jpeg", "image/png"):
            return self.extract_text_from_image(file_bytes)
        elif file_type == "application/pdf":
            return self.extract_text_from_pdf(file_bytes)
        elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            return self.extract_text_from_docx(file_bytes)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")

# Singleton instance for easy import
ocr_processor = OCRProcessor()
extract_text = ocr_processor.extract_text