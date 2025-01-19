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

    Klasa zarządza interfejsem graficznym, rozpoznawaniem mowy, przetwarzaniem tekstu
    oraz integracją z modułem medycznym.
    """

    def __init__(self, debug=False):
        """
        Inicjalizuje aplikację VoiceChatApp, konfigurując komponenty GUI, rozpoznawania mowy
        oraz przetwarzania tekstu.

        Args:
            debug (bool): Flaga określająca, czy włączyć tryb debugowania logów.
        """
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.DEBUG if debug else logging.INFO)

        self.gui = ChatGUI(parent=self, debug=debug)
        self.lector = SoundEngine(debug=debug)
        self.medic = MedicalChat(debug=debug)
        self.is_speaking = False
        self.threads = []

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
        """
        Sekwencja startowa, która uruchamia aplikację i interfejs graficzny.
        """
        self.logger.debug("Wywołanie start")

        message = SpeechLibrary.start_response()
        self.gui.chat_display.config(state="normal")
        self.gui.chat_display.insert(tk.END, f"MedykBot: {message}\n")
        self.gui.chat_display.config(state="disabled")
        self.lector.say(message)

        self.gui.start()

    def ev_speaking_button(self):
        """
        Obsługuje zdarzenie kliknięcia przycisku mówienia.

        Jeśli nagrywanie mowy nie jest aktywne, uruchamia nasłuchiwanie w nowym wątku.
        W przeciwnym razie zatrzymuje nagrywanie i aktualizuje elementy GUI.

        Zmiany w GUI:
        - Aktualizuje ikonę przycisku mówienia.
        - Ustawia odpowiedni status w interfejsie graficznym.
        """
        self.logger.debug("Wywołanie speaking_button")
        if not self.is_speaking:
            self.start_speaking_button()
            self.gui.update_status_label("nasłuchiwanie")
        else:
            self.stop_speaking_button()
            self.gui.update_status_label("sprawdź i potwierdź")

    def start_speaking_button(self):
        """
        Rozpoczyna nasłuchiwanie mowy w nowym wątku.

        Tworzy nowy wątek odpowiedzialny za odczyt dźwięku z mikrofonu i jego przetwarzanie.
        """
        self.logger.debug("Wywołanie start_speaking_button")
        self.gui.user_input_voice.delete("1.0", tk.END)
        self.gui.user_input_voice_partial.config(text="")
        if not self.is_speaking:
            self.is_speaking = True
            self.gui.update_speaking_button(self.is_speaking)

            thread = threading.Thread(target=self.hear, daemon=True)
            thread.start()
            self.threads.append(thread)
        else:
            self.stop_speaking_button()

    def stop_speaking_button(self):
        """
        Zatrzymuje nasłuchiwanie mowy.

        Aktualizuje odpowiednie elementy GUI oraz zatrzymuje przetwarzanie strumienia audio.
        """
        self.logger.debug("Wywołanie stop_speaking_button")
        self.is_speaking = False
        self.gui.update_speaking_button(self.is_speaking)

        # Pobierz rozpoznany tekst z pola tekstowego i zaktualizuj pole edycji - Wielka zagadka Szymka
        # recognized_text = self.gui.user_input_voice.get("1.0", tk.END).strip()
        # self.gui.user_input_voice.delete("1.0", tk.END)
        # self.gui.user_input_voice.insert(tk.END, recognized_text)
        self.gui.user_input_voice_partial.config(text="")

    def hear(self):
        """
        Wątek odpowiedzialny za nasłuchiwanie i przetwarzanie mowy na tekst.

        Dane są odczytywane z mikrofonu i przetwarzane przez model VOSK.
        """
        self.logger.debug("Wywołanie hear")
        recognized_text = ""
        partial_result = ""
        try:
            data = self.stream.read(4000, exception_on_overflow=False)
            self.recognizer.AcceptWaveform(data)
        except Exception as e:
            self.logger.error(f"Błąd podczas odczytu strumienia: {e}")

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

        if recognized_text.strip() == "" and False:
            recognized_text = json.loads(partial_result).get("partial", "")
            self.gui.user_input_voice.delete("1.0", tk.END)
            self.gui.user_input_voice.insert(tk.END, recognized_text.strip())
        self.logger.debug("hear zakończył działanie")

    def ev_confirm_button(self):
        """
        Obsługuje zdarzenie kliknięcia przycisku 'Potwierdź'.

        Zatrzymuje nasłuchiwanie, przetwarza wprowadzony tekst użytkownika
        oraz generuje odpowiedź, która jest wyświetlana w GUI.
        """
        self.stop_speaking_button()
        self.gui.user_input_voice_partial.config(text="Aby rozpocząć mówienie wciśnij ikonę mikrofonu")
        self.gui.update_status_label("mówię do ciebie")
        self.process_text()
        self.gui.user_input_voice.delete("1.0", tk.END)
        self.check_audio_status_thread()

    def process_text(self):
        """
        Przetwarza tekst wprowadzony przez użytkownika, generuje odpowiedź
        oraz wyświetla ją w GUI.
        """
        self.logger.debug("Wywołanie process_text")
        user_text = self.gui.user_input_voice.get("1.0", tk.END).strip()

        if not user_text:
            self.logger.debug("Brak tekstu do przetworzenia.")
            return

        # Wyświetlenie tekstu użytkownika w czacie
        self.gui.chat_display.config(state="normal")
        self.gui.chat_display.insert(tk.END, f"Ty: {user_text}\n")
        self.gui.chat_display.config(state="disabled")
        self.logger.debug(f"Wyświetlono tekst użytkownika: 'Ty: {user_text}'")

        if SpeechLibrary.is_reset_command(user_text.lower()):
            self.logger.info("Otrzymano komendę resetowania rozmowy.")
            self.medic.reset_conversation()
            response = SpeechLibrary.reset_response()
            # Wyświetlenie odpowiedzi bota w czacie
            self.gui.chat_display.config(state="normal")
            self.gui.chat_display.delete("1.0", tk.END)
            self.gui.chat_display.insert(tk.END, f"MedykBot: {response}\n")
            self.gui.chat_display.config(state="disabled")
            self.logger.debug(f"Wyświetlono odpowiedź bota: 'MedykBot: {response}'")
            self.lector.say(response)
            self.gui.user_input_voice.delete("1.0", tk.END)
            return

        result, message = self.medic.analyze_symptoms(user_text)
        self.logger.debug(f"Przetworzono tekst użytkownika przez MedicalChat: {message}")

        self.gui.chat_display.config(state="normal")
        self.gui.chat_display.insert(tk.END, f"MedykBot: {message}\n")
        self.gui.chat_display.config(state="disabled")
        self.gui.chat_display.see(tk.END)
        self.logger.debug(f"Wyświetlono odpowiedź bota: 'MedykBot: {message}'")

        self.lector.say(message)

        self.gui.user_input_voice.delete("1.0", tk.END)
        self.logger.debug("Pole tekstowe zostało wyczyszczone.")

    def on_closing(self):
        """
        Zamyka aplikację i zwalnia zasoby.

        Kończy działanie strumieni, zamyka wątki i zwalnia zasoby audio.
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
        """
        Destruktor klasy.

        Wywołuje funkcję on_closing w celu zwolnienia zasobów przed usunięciem obiektu.
        """
        self.on_closing()

    def check_audio_status_thread(self):
        """
        Cyklicznie sprawdza, czy wątek odpowiedzialny za odtwarzanie dźwięku (self.lector.current_thread)
        nadal działa. Gdy się zakończy, ustawia status na "możesz teraz mówić".
        """
        if self.lector.current_thread is not None and self.lector.current_thread.is_alive():
            self.gui.root.after(100, self.check_audio_status_thread)
        else:
            self.gui.update_status_label("możesz teraz mówić")
