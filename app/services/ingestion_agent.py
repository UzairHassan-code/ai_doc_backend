# File path: doc_intel_backend/app/services/ingestion_agent.py

from pathlib import Path
from pypdf import PdfReader

class IngestionAgent:
    """
    Agent responsible for reading raw files and extracting text.
    Currently supports: PDF
    Future support: Images (OCR), Text, Docx
    """
    
    def process(self, file_path: str) -> str:
        """
        Ingests a file and returns its textual content.
        """
        path_obj = Path(file_path)
        
        if not path_obj.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
            
        if path_obj.suffix.lower() == ".pdf":
            return self._parse_pdf(path_obj)
        else:
            # Placeholder for OCR/Image handling if needed later
            return "Image processing not yet implemented."

    def _parse_pdf(self, pdf_path: Path) -> str:
        reader = PdfReader(str(pdf_path))
        text_content = []
        
        for page in reader.pages:
            text = page.extract_text()
            if text:
                text_content.append(text)
                
        return "\n".join(text_content)