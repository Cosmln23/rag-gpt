import fitz  # PyMuPDF

class PyMuPdfLoader:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def load(self) -> str:
        doc = fitz.open(self.file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text
