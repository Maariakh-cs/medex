# 🩺 MedEx – Medical Data Extractor

**MedEx** is an AI-powered web application that extracts meaningful medical information from PDFs and image files using OCR and NLP. Built with **FastAPI**, **Tesseract**, and **SciSpacy**, this tool makes it easy to convert raw medical documents into structured, analyzable data.

![Made with Python](https://img.shields.io/badge/Built%20with-Python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![SciSpacy](https://img.shields.io/badge/SciSpacy-NLP%20Medical-brightgreen)
![OCR](https://img.shields.io/badge/OCR-Tesseract-orange)

---

## 🔍 Features

- 📄 Upload medical PDFs or image files
- 🔍 Perform OCR using **Tesseract + PyMuPDF**
- 🧠 Extract medical entities (Diseases, Drugs, Chemicals) using **SciSpacy**
- ⚡ Fast and lightweight backend with **FastAPI**
- 🌐 Intuitive, responsive frontend using **HTML/CSS/JS**
- 📊 Ready for integration into analytics dashboards

---

## 🛠️ Tech Stack

| Layer         | Tech                          |
|---------------|-------------------------------|
| Frontend      | HTML, CSS, JavaScript         |
| Backend       | Python, FastAPI               |
| OCR Engine    | Tesseract OCR, PyMuPDF        |
| NLP/NER Model | SciSpacy (`en_ner_bc5cdr_md`) |
| UI/UX         | Vanilla JS, Responsive Design |

---

## 🚀 How to Run Locally

### 🔧 Prerequisites

- Python 3.8+
- [Tesseract OCR installed](https://github.com/tesseract-ocr/tesseract)
- Git

### 🧪 Setup Steps

```bash
# 1. Clone the repo
git clone https://github.com/Maariakh-cs/medex.git
cd medex

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the backend
cd backend
uvicorn main:app --reload
