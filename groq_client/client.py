import os
from groq import Groq

class GroqClient:
    """
    A client class for interacting with the Groq model API for text summarization.
    """

    def __init__(self):
        """
        Initializes the Groq client using the API key stored in environment variables.
        """
        api_key = os.getenv("GROQ_API_KEY")
        self.client = Groq(api_key=api_key)

    def summarize(self, prompt: str) -> str:
        """
        Sends a prompt to the Groq model for summarization and retrieves the result.

        :param prompt: The prompt to be sent for summarization.
        :return: The AI-generated summary.
        """
        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="gemma-7b-it",
        )
        return chat_completion.choices[0].message.content
