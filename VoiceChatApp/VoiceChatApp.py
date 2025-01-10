from .MedicalChat import MedicalChat
from vosk import Model, KaldiRecognizer
import pyaudio
import json
import threading
import logging
from .ChatGUI import ChatGUI
from .SoundEngine import SoundEngine
from .SpeechLibrary import SpeechLibrary
import tkinter as tk


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
        self.gui.chat_display.config(state="normal")
        self.gui.chat_display.insert(tk.END, f"MedykBot: {message}\n")
        self.gui.chat_display.config(state="disabled")
        self.lector.say(message)

        self.gui.start()

    def ev_speaking_button(self):
        """
        Obsługuje przycisk mówienia.
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
            # Aktualizacja ikony po zmianie stanu
            self.gui.update_speaking_button(self.is_speaking)

            thread = threading.Thread(target=self.hear, daemon=True)
            thread.start()
            self.threads.append(thread)
        else:
            self.stop_speaking_button()

    def stop_speaking_button(self):
        """Obsługuje zatrzymanie nagrywania mowy."""
        self.logger.debug("Wywołanie stop_speaking_button")
        self.is_speaking = False
        # Aktualizacja ikony po zmianie stanu
        self.gui.update_speaking_button(self.is_speaking)

        # Pobierz rozpoznany tekst z pola tekstowego i zaktualizuj pole edycji
        recognized_text = self.gui.user_input_voice.get("1.0", tk.END).strip()
        self.gui.user_input_voice.delete("1.0", tk.END)
        self.gui.user_input_voice.insert(tk.END, recognized_text)

    def hear(self):
        """
        Wątek nasłuchujący, odpowiedzialny za przetwarzanie dźwięku na tekst.

        Dane są odczytywane z mikrofonu i rozpoznawane przy użyciu modelu VOSK.
        """
        self.logger.debug("Wywołanie hear")
        recognized_text = ""
        partial_result = ""

        while self.is_speaking:
            try:
                data = self.stream.read(4000, exception_on_overflow=False)
                if self.recognizer.AcceptWaveform(data):
                    result = self.recognizer.Result()
                    text = json.loads(result).get("text", "")
                    recognized_text += text + " "
                    # Aktualizacja pola tekstowego z rozpoznanym tekstem
                    self.gui.user_input_voice.delete("1.0", tk.END)
                    self.gui.user_input_voice.insert(tk.END, recognized_text.strip())
                else:
                    partial_result = self.recognizer.PartialResult()
                    partial_text = json.loads(partial_result).get("partial", "")
                    self.gui.user_input_voice_partial.config(text=partial_text)
            except Exception as e:
                self.logger.error(f"Błąd podczas odczytu strumienia: {e}")
                break

        if recognized_text.strip() == "":
            recognized_text = json.loads(partial_result).get("partial", "")
            self.gui.user_input_voice.delete("1.0", tk.END)
            self.gui.user_input_voice.insert(tk.END, recognized_text.strip())
        self.logger.debug("hear zakończył działanie")

    def ev_confirm_button(self):
        """
        Obsługa przycisku 'Potwierdź'
        """
        self.gui.user_input_voice_partial.config(text="Aby rozpocząć mówienie wciśnij ikonę mikrofonu")
        self.process_text()

    def process_text(self):
        """
        Przetwarza tekst wprowadzony przez użytkownika i wyświetla odpowiedź.
        """
        self.logger.debug("Wywołanie process_text")
        # Pobierz tekst z pola edycji i przekształć go na małe litery dla lepszej zgodności
        user_text = self.gui.user_input_voice.get("1.0", tk.END).strip()

        if not user_text:
            self.logger.debug("Brak tekstu do przetworzenia.")
            return

        # Wyświetlenie tekstu użytkownika w czacie
        self.gui.chat_display.config(state="normal")
        self.gui.chat_display.insert(tk.END, f"Ty: {user_text}\n")
        self.gui.chat_display.config(state="disabled")
        self.logger.debug(f"Wyświetlono tekst użytkownika: 'Ty: {user_text}'")

        # Sprawdź, czy użytkownik chce zresetować rozmowę
        if SpeechLibrary.is_reset_command(user_text.lower()):
            self.logger.info("Otrzymano komendę resetowania rozmowy.")
            self.medic.reset_conversation()
            response = "Rozumiem, tak więc opisz mi jeszcze raz co Ci dolega?"
            # Wyświetlenie odpowiedzi bota w czacie
            self.gui.chat_display.config(state="normal")
            self.gui.chat_display.insert(tk.END, f"MedykBot: {response}\n")
            self.gui.chat_display.config(state="disabled")
            self.logger.debug(f"Wyświetlono odpowiedź bota: 'MedykBot: {response}'")
            # Odtworzenie odpowiedzi
            self.lector.say(response)
            # Czyszczenie pola tekstowego po potwierdzeniu
            self.gui.user_input_voice.delete("1.0", tk.END)
            return

        # Przetwarzanie tekstu przez moduł medyczny
        result, message = self.medic.analyze_symptoms(user_text)
        self.logger.debug(f"Przetworzono tekst użytkownika przez MedicalChat: {message}")

        # Wyświetlenie odpowiedzi bota w czacie
        self.gui.chat_display.config(state="normal")
        self.gui.chat_display.insert(tk.END, f"MedykBot: {message}\n")
        self.gui.chat_display.config(state="disabled")
        self.logger.debug(f"Wyświetlono odpowiedź bota: 'MedykBot: {message}'")

        # Odtworzenie odpowiedzi
        self.lector.say(message)

        # Czyszczenie pola tekstowego po potwierdzeniu
        self.gui.user_input_voice.delete("1.0", tk.END)
        self.logger.debug("Pole tekstowe zostało wyczyszczone.")



    def on_closing(self):
        """
        Zamyka aplikację i zwalnia zasoby.
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
