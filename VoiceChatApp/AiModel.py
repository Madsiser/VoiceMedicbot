from openai import OpenAI
from dotenv import load_dotenv
import os


class AiModel:
    """
    Klasa AiModel zarządza interakcjami z modelem AI dostarczanym przez OpenAI.
    """

    def __init__(self):
        """
        Inicjalizuje obiekt AiModel i konfiguruje klienta OpenAI.
        Wczytuje dane uwierzytelniające z plików środowiskowych za pomocą dotenv.
        """
        load_dotenv()  # Wczytanie zmiennych środowiskowych z pliku .env
        self.client = OpenAI(
            organization=os.getenv('OPENAI_ORGANIZATION'),
            project=os.getenv('OPENAI_PROJECT'),
            api_key=os.getenv('OPENAI_API_KEY')
        )

    def ask(self, prompt: str) -> str:
        """
        Wysyła zapytanie do modelu AI i zwraca jego odpowiedź.

        Args:
            prompt (str): Tekst zapytania, który ma zostać przesłany do modelu.

        Returns:
            str: Odpowiedź wygenerowana przez model AI. W przypadku błędu zwraca opis błędu.
        """
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "system", "content": "Odpowiedź od chatbota odnośnie zaleceń do twoich objawów."},
                    {"role": "user", "content": prompt},
                     {"role": "system", "content": "Nadal zaleca się skontaktować z lekarzem pierwszego kontaktu."}],
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            # Logowanie i zwrócenie opisu błędu
            error_message = f"Error podczas komunikacji z API: {e}"
            print(error_message)  # Można zastąpić logowaniem, np. logging.error(error_message)
            return error_message
