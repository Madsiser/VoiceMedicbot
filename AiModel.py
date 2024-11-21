from openai import OpenAI
from dotenv import load_dotenv
import os

class AiModel:

    def __init__(self):
        self.client = OpenAI(
            organization=os.getenv('OPENAI_ORGANIZATION'),
            project=os.getenv('OPENAI_PROJECT'),
            api_key=os.getenv('OPENAI_API_KEY')
        )

    def ask(self, prompt: str):
        """
        Wysyła wiadomość do modelu czatu i zwraca odpowiedź.
        """
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],

            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {e}"