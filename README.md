# 🩺 MedEx – Medical Data Extractor Web App

**MedEx** is a modern web application that extracts structured medical data from uploaded documents (PDFs, DOCX, or images) using OCR and NLP techniques. The backend is built with **FastAPI**, **EasyOCR**, and **SciSpacy**, while the frontend offers an elegant UI for drag-and-drop file uploads and interactive result displays.

---

## 🚀 Features

- 📤 Drag-and-drop or file upload support
- 🧾 OCR using **EasyOCR** for images and scanned PDFs
- 📄 DOCX file extraction using `python-docx`
- 🧠 Medical entity recognition (diagnosis, medications, allergies, procedures, etc.) using **regex + spaCy**
- 👤 Patient info extraction (name, DOB, gender, contact)
- 🌐 Responsive, tabbed frontend built with vanilla JS + HTML/CSS
- 🔄 Animated loading indicator during file processing
- ✅ Health check endpoint for backend status

---

## 🧰 Tech Stack

| Layer     | Technology                                           |
|-----------|------------------------------------------------------|
| Backend   | [FastAPI](https://fastapi.tiangolo.com/), Python 3.10 |
| OCR       | [EasyOCR](https://github.com/JaidedAI/EasyOCR)      |
| NLP       | [spaCy](https://spacy.io/), [SciSpacy](https://allenai.github.io/scispacy/) |
| Parsing   | [PyMuPDF](https://pymupdf.readthedocs.io), [pdf2image](https://pypi.org/project/pdf2image/), `python-docx` |
| Frontend  | HTML5, CSS3, JavaScript                             |

---

## 📦 Requirements

Install these system dependencies before running:

- **Tesseract** not required (EasyOCR handles OCR)
- Python 3.8+
- [Poppler](https://github.com/oschwartz10612/poppler-windows) (for `pdf2image`) on Windows

---

## 🔧 Installation
# 1. Clone the repository
git clone https://github.com/Maariakh-cs/medex.git
cd medex
# 2. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # macOS/Linux
# 3. Install dependencies
pip install -r requirements.txt

---

## ▶️ Run the App
# Start FastAPI backend
uvicorn backend.main:app --reload
Then open frontend/index.html in your browser (you can use Live Server or just double-click to open locally).

---

## 📁 Folder Structure
medex/
├── backend/
│   ├── main.py          # FastAPI routes and endpoints
│   ├── config.py        # App configuration settings
│   ├── extract.py       # Regex + NLP-based data extraction
│   ├── ocr.py           # EasyOCR and file parsing logic
│   └── models.py        # Pydantic data models
├── frontend/
│   ├── index.html       # UI layout
│   ├── styles.css       # Styling and animations
│   └── app.js           # File handling, fetch calls, UI updates
├── requirements.txt     # All Python dependencies
└── README.md            # You're reading it!

---

## 🧪 Supported File Types
.pdf – scanned or digital PDFs

.jpg, .jpeg, .png – medical image scans or photos

.docx – Microsoft Word documents

---

## 🧠 Example Output
json
Copy code
{
  "patient_info": {
    "name": "Jane Doe",
    "dob": "01/01/1990",
    "gender": "female",
    "patient_id": "ABC123",
    "address": "123 Main Street",
    "phone": "123-456-7890"
  },
  "medical_record": {
    "diagnosis": "Hypertension",
    "medications": ["Lisinopril", "Amlodipine"],
    "allergies": ["Penicillin"],
    "procedures": ["CT Scan"],
    "lab_results": ["CBC normal"],
    "notes": "Follow-up in 2 weeks"
  },
  "raw_text": "...full extracted document text...",
  "success": true,
  "message": "Extraction successful"
}

---

## 📈 Future Enhancements
PDF section-wise analysis (e.g., headers like "Assessment", "Plan")
Export extracted data as CSV or PDF
User login and document history
LLM integration for summarization or diagnostics

---

## 🙋‍♀️ Author
Maaria Khan
Final Year Computer Science Engineering Student
🔗www.linkedin.com/in/maariakh-cs

