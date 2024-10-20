import os
import logging
from telegram import Update
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from app.file_processor import FileProcessor
from groq_client.client import GroqClient

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

class DocuMateBot:
    def __init__(self, token):
        self.application = Application.builder().token(token).build()
        self.file_processor = FileProcessor()
        self.groq_client = GroqClient()
        self.user_files = {}  # To store file paths per user
        self.upload_directory = "uploads/"  # Directory to save user files
        os.makedirs(self.upload_directory, exist_ok=True)
        self.setup_handlers()

    def setup_handlers(self):
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("info", self.info_command))

        # Using MIME types for document filtering
        self.application.add_handler(MessageHandler(filters.Document.MimeType("application/pdf"), self.handle_file))
        self.application.add_handler(MessageHandler(filters.Document.MimeType("application/vnd.openxmlformats-officedocument.wordprocessingml.document"), self.handle_file))
        self.application.add_handler(MessageHandler(filters.Document.MimeType("application/vnd.openxmlformats-officedocument.presentationml.presentation"), self.handle_file))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_prompt))

    async def start(self, update: Update, context: CallbackContext):
        await update.message.reply_text("Welcome to DocuMate! Upload a PDF, DOCX, or PPTX file to get started. Once uploaded, you can ask questions based on the document content.")

    async def help_command(self, update: Update, context: CallbackContext):
        help_text = (
            "Commands you can use:\n"
            "/start - Start the bot and upload a document.\n"
            "/help - Get help on using the bot.\n"
            "/info - Learn more about DocuMate.\n"
            "After uploading a document, ask any question, and the bot will respond based on the document content."
        )
        await update.message.reply_text(help_text)

    async def info_command(self, update: Update, context: CallbackContext):
        info_text = (
            "DocuMate is an AI-powered document-based question-answering bot.\n"
            "Upload a document (PDF, DOCX, PPTX) and ask questions based on its content.\n"
            "The bot uses advanced language processing to provide precise answers."
            "The bot is created by Mr.Vipul"
        )
        await update.message.reply_text(info_text)

    async def handle_file(self, update: Update, context: CallbackContext):
        user_id = update.message.from_user.id
        document = update.message.document
        mime_type = document.mime_type

        # Validate supported MIME types
        if mime_type not in ["application/pdf", 
                            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                            "application/vnd.openxmlformats-officedocument.presentationml.presentation"]:
            await update.message.reply_text("Unsupported file type. Please upload a PDF, DOCX, or PPTX file.")
            return

        # Download and save the file
        file = await document.get_file()
        file_path = f"{document.file_id}.{mime_type.split('/')[-1]}"  # Save with correct extension
        await file.download_to_drive(file_path)

        # Replace any existing file for the user and store the file path
        previous_file = self.user_files.get(user_id)
        if previous_file and os.path.exists(previous_file):
            os.remove(previous_file)  # Delete the previous file from the directory
        self.user_files[user_id] = file_path

        await update.message.reply_text("File received! Now, you can ask questions related to this document.")

    async def handle_prompt(self, update: Update, context: CallbackContext):
        user_id = update.message.from_user.id
        user_prompt = update.message.text
        file_path = self.user_files.get(user_id)

        if not file_path:
            await update.message.reply_text("Please upload a document first. document should be a PDF, DOCX, or PPTX file.")
            return

        # Process the file content and generate a response based on the user’s question
        file_text = self.file_processor.extract_text(file_path)
        truncated_text = file_text[:3000]  # Truncate text to limit tokens
        complete_prompt = f"User Prompt:\n{user_prompt}\n\nDocument Text:\n{truncated_text}"
        summary = self.groq_client.summarize(complete_prompt)

        # Send the answer back to the user
        await update.message.reply_text("Answer:\n" + summary, parse_mode=None)

    def run(self):
        self.application.run_polling()

if __name__ == "__main__":
    load_dotenv()
    TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    bot = DocuMateBot(TOKEN)
    bot.run()
