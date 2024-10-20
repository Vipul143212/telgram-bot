import os
from groq import Groq

class GroqClient:
    """
    A client class for interacting with the Groq model API for text summarization.
    """

    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        self.client = Groq(api_key=api_key)

    def summarize(self, prompt: str) -> str:
        chat_completion = self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="gemma-7b-it",
        )
        return chat_completion.choices[0].message.content
