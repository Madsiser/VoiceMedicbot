from .MedicalChat import MedicalChat
from vosk import Model, KaldiRecognizer
import pyaudio
import json
import threading
import logging
from .ChatGUI import *
from .SoundEngine import SoundEngine
from .SpeechLibrary import SpeechLibrary


class VoiceChatApp:
    """
    Główna klasa aplikacji VoiceChatApp.

    Zarządza interfejsem graficznym, rozpoznawaniem mowy, przetwarzaniem tekstu
    oraz integracją z modułem medycznym.
    """

    def __init__(self, debug=False):
        """
        Inicjalizuje aplikację.

        Args:
            debug (bool): Flaga określająca, czy włączyć tryb debugowania.
        """
        # Konfiguracja loggera
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.DEBUG if debug else logging.INFO)

        # Inicjalizacja komponentów
        self.gui = ChatGUI(parent=self, debug=debug)
        self.lector = SoundEngine(debug=debug)
        self.medic = MedicalChat(debug=debug)
        self.user_input = ""
        self.is_speaking = False
        self.threads = []

        # Konfiguracja rozpoznawania mowy
        self.model = Model("VoiceChatApp/model")
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=8000
        )
        self.stream.start_stream()
        self.recognizer = KaldiRecognizer(self.model, 16000)

    def start(self):
        """Sekwencja startowa w której między innymi jest uruchamiany interfejs graficzny aplikacji."""
        self.logger.debug("Wywołanie start")

        message = SpeechLibrary.hello_phrase
        self.gui.chat_display.insert(tk.END, f"MedykBot: {message}\n")
        self.lector.say(message)

        self.gui.start()
        
    def ev_speaking_button(self):
        """
        Obsługuje przycisk mówienia..
        """
        self.logger.debug("Wywołanie speaking_button")
        if not self.is_speaking:
            self.start_speaking_button()
        else:
            self.stop_speaking_button()

    def start_speaking_button(self):
        """
        Obsługuje rozpoczęcie mówienia.

        Tworzy nowy wątek odpowiedzialny za rozpoznawanie mowy.
        """
        self.logger.debug("Wywołanie start_speaking_button")
        if not self.is_speaking:
            self.is_speaking = True
            thread = threading.Thread(target=self.hear, daemon=True)
            thread.start()
            self.threads.append(thread)
        else:
            self.stop_speaking_button()
        

    def stop_speaking_button(self):
        """Obsługuje zatrzymanie nagrywania mowy."""
        self.logger.debug("Wywołanie stop_speaking_button")
        self.is_speaking = False
        self.gui.user_input_voice.config(text=self.user_input)

    def clear_user_input(self):
        """Czyści bufor tekstowy użytkownika."""
        self.logger.debug("Wywołanie clear_user_input")
        self.user_input = ""

    def hear(self):
        """
        Wątek nasłuchujący, odpowiedzialny za przetwarzanie dźwięku na tekst.

        Dane są odczytywane z mikrofonu i rozpoznawane przy użyciu modelu VOSK.
        """
        self.logger.debug("Wywołanie hear")
        self.user_input = ""
        partial_result = ""

        while self.is_speaking:
            try:
                data = self.stream.read(4000, exception_on_overflow=False)
                if self.recognizer.AcceptWaveform(data):
                    result = self.recognizer.Result()
                    self.user_input += json.loads(result)["text"]
                    self.gui.user_input_voice.config(text=self.user_input)
                else:
                    partial_result = self.recognizer.PartialResult()
                    self.gui.user_input_voice_partial.config(
                        text=json.loads(partial_result)["partial"]
                    )
            except Exception as e:
                self.logger.error(f"Błąd podczas odczytu strumienia: {e}")
                break

        if self.user_input == "":
            self.user_input += json.loads(partial_result).get("partial", "")
        self.logger.debug("hear zakończył działanie")

    def process_text(self):
        """
        Przetwarza tekst wprowadzony przez użytkownika i wyświetla odpowiedź.

        Przesyła tekst do modułu analizy medycznej i wyświetla odpowiedź w GUI.
        """
        self.logger.debug("Wywołanie process_text")
        self.stop_speaking_button()
        user_text = self.user_input
        self.user_input = ""

        if not user_text.strip():
            return

        self.gui.chat_display.insert(tk.END, f"Ty: {user_text}\n")
        result, message = self.medic.analyze_symptoms(user_text)
        self.gui.chat_display.insert(tk.END, f"MedykBot: {message}\n")
        self.lector.say(message)

    def on_closing(self):
        """
        Zamyka aplikację i zwalnia zasoby.

        Zatrzymuje wątki, zamyka strumień audio oraz zatrzymuje GUI.
        """
        self.logger.debug("Wywołanie on_closing")
        self.is_speaking = False

        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        if self.p:
            self.p.terminate()

        for thread in self.threads:
            thread.join()

    def __del__(self):
        """Destruktor klasy, wywołuje funkcję on_closing w celu zwolnienia zasobów."""
        self.on_closing()
