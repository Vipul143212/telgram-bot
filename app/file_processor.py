import PyPDF2
import docx 
from pptx import Presentation
from io import BytesIO

class FileProcessor:
    """
    This class handles the extraction of text from PDF, DOCX, and PPTX files.
    """

    def extract_text(self, file) -> str:
        """
        Determines the file type and extracts text accordingly.
        
        :param file: Uploaded file object
        :return: Extracted text from the file
        """
        file_extension = file.name.split('.')[-1].lower()
        
        if file_extension == "pdf":
            return self._extract_text_from_pdf(file)
        elif file_extension in ["doc", "docx"]:
            return self._extract_text_from_docx(file)
        elif file_extension in ["ppt", "pptx"]:
            return self._extract_text_from_pptx(file)
        else:
            return "Unsupported file type."

    def _extract_text_from_pdf(self, file) -> str:
        """
        Extracts text from a PDF file.
        
        :param file: PDF file object
        :return: Extracted text from PDF
        """
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text

    def _extract_text_from_docx(self, file) -> str:
        """
        Extracts text from a DOCX file.
        
        :param file: DOCX file object
        :return: Extracted text from DOCX
        """
        doc = docx.Document(file)
        return "\n".join([para.text for para in doc.paragraphs])

    def _extract_text_from_pptx(self, file) -> str:
        """
        Extracts text from a PPTX file.
        
        :param file: PPTX file object
        :return: Extracted text from PPTX
        """
        ppt = Presentation(file)
        text = ""
        for slide in ppt.slides:
            for shape in slide.shapes:
                if hasattr(shape, "text"):
                    text += shape.text + "\n"
        return text
