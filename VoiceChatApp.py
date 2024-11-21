from tkinter import scrolledtext
import tkinter as tk
from MedicalChat import MedicalChat
from vosk import Model, KaldiRecognizer
import pyaudio
import json
from SpeechLibrary import SpeechLibrary
import threading
import logging
from ChatGUI import ChatGUI
from SoundEngine import SoundEngine

class VoiceChatApp:
    
    def __init__(self,debug=False):
        # Ustawienie poziomu logowania
        self.logger = logging.getLogger(__name__)
        if debug:
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.basicConfig(level=logging.INFO)

        # Parametry
        self.gui = ChatGUI(parent=self, debug=debug)
        self.lector = SoundEngine()
        self.medic = MedicalChat(debug)
        self.user_input = ""
        self.is_speaking = False

        self.threads = []

        # Wymagane do rozpoznawania głosu
        model = Model("model")
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
        self.stream.start_stream()
        self.recognizer = KaldiRecognizer(model, 16000)

        
    
    def start(self):
        self.gui.start()

    # Rozpoczecie watku mówienia
    def start_speaking_button(self):
        self.logger.debug("Wywołanie start_speaking_button")
        if not self.is_speaking:
            self.is_speaking = True
            thread = threading.Thread(target=self.hear, daemon=True)
            thread.start()
            self.threads.append(thread)
            
    # Zatrzymanie nagrywania
    def stop_speaking_button(self):
        self.logger.debug("Wywołanie stop_speaking_button")
        self.is_speaking = False
        self.gui.user_input_voice.config(text=self.user_input)

    # Czyszczenie bufora
    def clear_user_input(self):
        self.logger.debug("Wywołanie clear_user_input")
        self.user_input = ""

    # Wątek słuchania
    def hear(self):
        self.logger.debug("Wywołanie hear")
        self.user_input = ""
        partial_result = ""
        while self.is_speaking:
            try:
                data = self.stream.read(4000, exception_on_overflow=False)  # Użyj exception_on_overflow=False
                if self.recognizer.AcceptWaveform(data):
                    result = self.recognizer.Result()
                    self.user_input += json.loads(result)["text"]
                    self.gui.user_input_voice.config(text=self.user_input)
                else:
                    partial_result = self.recognizer.PartialResult()
                    self.gui.user_input_voice_partial.config(text=json.loads(partial_result)["partial"])
            except Exception as e:
                print(f"Error while reading stream: {e}")
                break

        if self.user_input == "":
            self.user_input += json.loads(partial_result)["partial"]
        self.logger.debug("hear zakończył działanie")

    # Przetwarzanie tekstu i wyswietlanie
    def process_text(self):
        self.logger.debug("Wywołanie process_text")
        self.stop_speaking_button()
        user_text = self.user_input
        self.user_input = ""
        if not user_text:  # Sprawdzenie, czy pole nie jest puste
            return
        self.gui.chat_display.insert(tk.END, f"Ty: {user_text}\n")
        result, message = self.medic.analyze_symptoms(user_text)
        self.gui.chat_display.insert(tk.END, f"MedykBot: {message}\n")
        self.lector.say(message)


    # Zamykanie aplikacji
    def on_closing(self):
        self.logger.debug("Wywołanie on_closing")
        self.is_speaking = False
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        for thread in self.threads:
            thread.join()

    def __del__(self):
        self.on_closing()
    
