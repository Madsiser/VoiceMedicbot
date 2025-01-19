from openai import OpenAI
from dotenv import load_dotenv
import os


class AiModel:
    """
    Klasa AiModel zarządza interakcjami z modelem AI dostarczanym przez OpenAI.

    Klasa ta umożliwia przesyłanie zapytań do modelu AI i odbieranie odpowiedzi.
    Dane uwierzytelniające są wczytywane z pliku środowiskowego `.env` za pomocą
    biblioteki dotenv.
    """

    def __init__(self):
        """
        Inicjalizuje obiekt AiModel i konfiguruje klienta OpenAI.

        Proces inicjalizacji obejmuje:
        - Wczytanie zmiennych środowiskowych z pliku `.env`.
        - Utworzenie klienta OpenAI za pomocą podanych danych uwierzytelniających.

        Zmienne środowiskowe:
        - OPENAI_ORGANIZATION: Organizacja OpenAI.
        - OPENAI_PROJECT: Projekt OpenAI.
        - OPENAI_API_KEY: Klucz API dla OpenAI.
        """
        load_dotenv()
        self.client = OpenAI(
            organization=os.getenv('OPENAI_ORGANIZATION'),
            project=os.getenv('OPENAI_PROJECT'),
            api_key=os.getenv('OPENAI_API_KEY')
        )

    def ask(self, prompt: str) -> str:
        """
        Wysyła zapytanie w formie tekstu do modelu AI i odbiera wygenerowaną przez niego odpowiedź.

        Args:
            prompt (str): Tekst zapytania, które ma zostać przesłane do modelu.

        Returns:
            str: Odpowiedź wygenerowana przez model AI.
                  W przypadku wystąpienia błędu zwraca opis błędu w formie tekstowej.
        """
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "system", "content": "Odpowiedź od chatbota odnośnie zaleceń do twoich objawów."},
                          {"role": "user", "content": prompt},
                          {"role": "system", "content": "Nadal zaleca się skontaktować z lekarzem pierwszego kontaktu."}
                          ],
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            error_message = f"Error podczas komunikacji z API: {e}"
            print(error_message)
            return error_message
