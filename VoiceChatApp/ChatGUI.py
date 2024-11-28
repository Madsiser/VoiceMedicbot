import tkinter as tk
from tkinter import scrolledtext
import logging


class ChatGUI:
    """
    Klasa ChatGUI odpowiada za zarządzanie graficznym interfejsem użytkownika (GUI) aplikacji czatu głosowego.
    """

    def __init__(self, parent, debug=False):
        """
        Inicjalizuje obiekt GUI i jego komponenty.

        Args:
            parent (VoiceChatApp): Referencja do rodzica (głównej aplikacji).
            debug (bool): Flaga określająca, czy włączyć tryb debugowania.
        """
        from VoiceChatApp import VoiceChatApp
        if not isinstance(parent, VoiceChatApp):
            raise TypeError(f"Expected parent to be an instance of VoiceChatApp, got {type(parent).__name__} instead.")
        self.parent = parent
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.DEBUG if debug else logging.INFO)

        # Inicjalizacja głównego okna aplikacji
        self.root = tk.Tk()
        self.root.title("Czat Głosowy")
        self.create_widgets()

    def start(self):
        """
        Uruchamia główną pętlę GUI.
        """
        self.root.mainloop()

    def create_widgets(self):
        """
        Tworzy wszystkie widżety interfejsu użytkownika i dodaje je do głównego okna.
        """
        self.logger.debug("Rozpoczynam tworzenie widżetów GUI")

        # Wyświetlacz czatu
        self.chat_display = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=50, height=20, state='normal')
        self.chat_display.pack(padx=10, pady=10)

        # Panel do wyświetlania rozpoznanego tekstu
        self.user_input_voice = tk.Label(self.root, width=50, text="Tekst główny", anchor="w")
        self.user_input_voice.pack(padx=10, pady=10)

        # Panel do wyświetlania częściowo rozpoznanego tekstu
        self.user_input_voice_partial = tk.Label(self.root, width=50, text="Tekst pomocniczy", anchor="w")
        self.user_input_voice_partial.pack(padx=10, pady=10)

        # Przycisk: Rozpocznij mówienie
        self.start_button = tk.Button(self.root, text="Rozpocznij Mówienie", command=self.parent.start_speaking_button)
        self.start_button.pack(padx=10, pady=5)

        # Przycisk: Potwierdź tekst
        self.confirm_button = tk.Button(self.root, text="Potwierdź", command=self.parent.ev_confirm_button)
        self.confirm_button.pack(padx=10, pady=5)

        # Przycisk: Zatrzymaj mówienie
        self.stop_button = tk.Button(self.root, text="Stop", command=self.parent.stop_speaking_button)
        self.stop_button.pack(padx=10, pady=5)

        # Zamykanie aplikacji przez kliknięcie "X"
        self.root.protocol("WM_DELETE_WINDOW", self.__del__)

    def __del__(self):
        """
        Zamyka aplikację, zwalnia zasoby i wywołuje funkcję zamykającą w głównej aplikacji.
        """
        self.logger.debug("Zamykanie GUI")
        self.root.destroy()
        self.parent.on_closing()
