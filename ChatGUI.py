from tkinter import scrolledtext
import tkinter as tk
import logging
import VoiceChatApp

class ChatGUI:
    def __init__(self, parent: VoiceChatApp, debug=False):
        self.parent = parent
        # Ustawienie poziomu logowania
        self.logger = logging.getLogger(__name__)
        if debug:
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.basicConfig(level=logging.INFO)

        # Parametry
        self.root = tk.Tk()
        self.root.title("Czat Głosowy")
        self.create_widgets()
    
    # Uruchomienie GUI
    def start(self):
        self.root.mainloop()

    def create_widgets(self):
        self.logger.debug("Rozpoczynam działanie metody create_widgets")
        # Panel do wyświetlania czatu
        self.chat_display = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=50, height=20)
        self.chat_display.pack(padx=10, pady=10)

        # Panel do wyświetlania tekstu użytkownika
        # self.user_input = tk.Entry(self.root, width=50)
        # self.user_input.pack(padx=10, pady=10)
        

        # Panel do wyświetlania głosu użytkownika
        self.user_input_voice = tk.Label(self.root, width=50, text="Tekst główny")
        self.user_input_voice.pack(padx=10, pady=10)

        # Panel do wyświetlania głosu użytkownika now
        self.user_input_voice_partial = tk.Label(self.root, width=50, text="Teskt pomocniczy")
        self.user_input_voice_partial.pack(padx=10, pady=10)
        

        # Przycisk do rozpoczęcia mówienia
        self.start_button = tk.Button(self.root, text="Rozpocznij Mówienie", command=self.parent.start_speaking_button)
        self.start_button.pack(padx=10, pady=10)

        # Przycisk do potwierdzenia co powiedziane
        self.start_button = tk.Button(self.root, text="Potwierdź", command=self.parent.process_text)
        self.start_button.pack(padx=10, pady=10)
        
        # Przycisk do potwierdzenia co powiedziane
        self.start_button = tk.Button(self.root, text="Stop", command=self.parent.stop_speaking_button)
        self.start_button.pack(padx=10, pady=10)

        # Zamykanie aplikacji
        self.root.protocol("WM_DELETE_WINDOW", self.__del__)

    # Zamykanie aplikacji
    def __del__(self):
        self.root.destroy()
        self.parent.on_closing()
    
