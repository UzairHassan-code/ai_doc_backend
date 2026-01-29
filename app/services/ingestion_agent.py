# File path: doc_intel_backend/app/services/ingestion_agent.py

import base64
import mimetypes
from pathlib import Path
from pypdf import PdfReader
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from app.core.config import settings

class IngestionAgent:

    """
    Agent responsible for reading raw files and extracting text.
    Capabilities:
    """
    def __init__(self):
        self.vision_llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=settings.GOOGLE_API_KEY,
            temperature=0.0
        )

    def process(self, file_path: str) -> str:
        """
        Ingests a file and returns its textual content.
        """
        path_obj = Path(file_path)
        
        if not path_obj.exists():
            raise FileNotFoundError(f"File not found: {file_path}")     
        mime_type, _ = mimetypes.guess_type(file_path)
        
        # Strategy 1: Native PDF Text
        if path_obj.suffix.lower() == ".pdf":
            return self._parse_pdf(path_obj)

        # Strategy 2: Image OCR (PNG/JPG/JPEG/WEBP)
        elif mime_type and mime_type.startswith("image"):
            return self._perform_ocr(path_obj, mime_type)
        
        else:
            return f"Unsupported file type: {path_obj.suffix}"

    def _parse_pdf(self, pdf_path: Path) -> str:
        """Extracts text from native PDFs."""
        try:
            reader = PdfReader(str(pdf_path))
            text_content = []
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    text_content.append(text)
            
            return "\n".join(text_content)
        except Exception as e:
            return f"Error reading PDF: {str(e)}"

    def _perform_ocr(self, image_path: Path, mime_type: str) -> str:
        try:
            # 1. Read image bytes and encode to Base64
            with open(image_path, "rb") as image_file:
                image_data = base64.b64encode(image_file.read()).decode("utf-8")

            message = HumanMessage(
                content=[
                    {"type": "text", "text": "Extract all the text from this image exactly as it appears. Do not summarize."},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:{mime_type};base64,{image_data}"},
                    },
                ]
            )

            # 3. Call Vision Model
            response = self.vision_llm.invoke([message])
            return response.content
            
        except Exception as e:
            return f"Error performing OCR: {str(e)}"