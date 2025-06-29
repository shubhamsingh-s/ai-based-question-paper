import os
import pdfplumber
import docx
import fitz  # PyMuPDF
import pytesseract
from typing import List
import re

class DocumentIngestor:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def parse_pdf(self) -> List[str]:
        """Extract text from a PDF file using pdfplumber. Falls back to OCR for scanned pages."""
        texts = []
        try:
            with pdfplumber.open(self.file_path) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        texts.append(text)
                    else:
                        # Fallback to OCR if no text is found (scanned image)
                        image = page.to_image(resolution=300)
                        ocr_text = pytesseract.image_to_string(image.original)
                        if ocr_text.strip():
                            texts.append(ocr_text)
        except Exception as e:
            print(f"Error parsing PDF: {e}")
        return texts

    def parse_word(self) -> List[str]:
        """Extract text from a Word (.docx) file using python-docx."""
        texts = []
        try:
            doc = docx.Document(self.file_path)
            for para in doc.paragraphs:
                if para.text.strip():
                    texts.append(para.text)
        except Exception as e:
            print(f"Error parsing Word file: {e}")
        return texts

    def parse_text(self) -> List[str]:
        """Extract text from a plain text file."""
        texts = []
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                texts = [line.strip() for line in f if line.strip()]
        except Exception as e:
            print(f"Error parsing text file: {e}")
        return texts

    def parse(self) -> List[str]:
        """Auto-detect file type and parse accordingly."""
        ext = os.path.splitext(self.file_path)[-1].lower()
        if ext == '.pdf':
            return self.parse_pdf()
        elif ext in ['.docx', '.doc']:
            return self.parse_word()
        elif ext in ['.txt', '.text']:
            return self.parse_text()
        else:
            print(f"Unsupported file type: {ext}")
            return []

    def extract_questions(self, text_list: List[str]) -> List[str]:
        """Extract questions from a list of text, splitting by 'Q' or 'Question'."""
        questions = []
        pattern = re.compile(r'(?:\bQ(?:uestion)?\s*\d+\b)', re.IGNORECASE)
        for text in text_list:
            # Split by the pattern, but keep the delimiter
            splits = pattern.split(text)
            matches = pattern.findall(text)
            # Recombine to keep question numbers
            for i, chunk in enumerate(splits[1:]):
                q_num = matches[i] if i < len(matches) else ''
                question = (q_num + ' ' + chunk).strip()
                if question:
                    questions.append(question)
        return questions 