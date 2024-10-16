from app.ui import PDFSummarizerUI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize UI and run the app
if __name__ == "__main__":
    summarizer_ui = PDFSummarizerUI()
    summarizer_ui.run()
