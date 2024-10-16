import streamlit as st
from app.file_processor import FileProcessor
from groq_client.client import GroqClient

class PDFSummarizerUI:
    """
    This class manages the Streamlit UI for the PDF summarizer bot.
    """
    
    def __init__(self):
        """
        Initializes the UI components, file processor, and Groq client.
        """
        self.file_processor = FileProcessor()
        self.groq_client = GroqClient()

    def run(self):
        """
        Runs the main UI for file upload and summarization interaction.
        """
        st.title("DocuMate")
        st.write("Upload a document file (PDF, DOCX, PPTX) and get an AI-generated summary.")

        # File uploader
        uploaded_file = st.file_uploader("Upload your document", type=["pdf", "doc", "docx", "ppt", "pptx"])
        
        if uploaded_file:
            # Display input box after file upload
            user_prompt = st.text_input("Enter your prompt for the AI model", "Summarize the main points")
            if st.button("Send"):
                # Process the file and generate summary
                file_text = self.file_processor.extract_text(uploaded_file)
                complete_prompt = f"{user_prompt}\n\nDocument Text:\n{file_text[:3000]}"  # Limited to 3000 chars for concise summarization
                summary = self.groq_client.summarize(complete_prompt)
                
                # Display summary
                st.write("### Answer:")
                st.write(summary)
