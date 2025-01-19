import tkinter as tk
from tkinter import scrolledtext
import logging
from PIL import Image, ImageTk


class ChatGUI:
    """
    Klasa ChatGUI odpowiada za zarządzanie graficznym interfejsem użytkownika (GUI) aplikacji czatu głosowego.

    Zapewnia funkcjonalności, takie jak:
    - Wyświetlanie historii wiadomości.
    - Edycja i podgląd rozpoznanego tekstu.
    - Sterowanie nagrywaniem za pomocą przycisków.
    """

    def __init__(self, parent, debug=False):
        """
        Inicjalizuje obiekt ChatGUI i konfiguruje środowisko GUI i ładuje wymagane zasoby.

        Args:
            parent (VoiceChatApp): Instancja klasy VoiceChatApp, która zarządza logiką aplikacji.
            debug (bool, optional): Jeśli True, włącza tryb debugowania w logach. Domyślnie False.

        Raises:
            TypeError: Jeśli `parent` nie jest instancją klasy VoiceChatApp.
        """
        from VoiceChatApp import VoiceChatApp
        if not isinstance(parent, VoiceChatApp):
            raise TypeError(
                f"Expected parent to be an instance of VoiceChatApp, got {type(parent).__name__} instead."
            )

        self.parent = parent
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.DEBUG if debug else logging.INFO)

        self.root = tk.Tk()
        self.root.title("Czat Głosowy")
        self.generate_icons()
        self.create_widgets()

    def create_widgets(self):
        """
        Tworzy wszystkie widżety interfejsu użytkownika i dodaje je do głównego okna aplikacji.

        Widżety obejmują:
        - Pole tekstowe do wyświetlania historii wiadomości czatu.
        - Pole edycyjne do wprowadzania tekstu rozpoznanego przez system.
        - Etykiety do wyświetlania stanu systemu oraz rozpoznanego tekstu.
        - Przycisk mikrofonu do sterowania nagrywaniem.
        - Przycisk potwierdzenia tekstu.
        """
        self.logger.debug("Rozpoczynam tworzenie widżetów GUI")

        #Pole tekstowe do wyświetlania historii wiadomości czatu
        self.chat_display = scrolledtext.ScrolledText(
            self.root, wrap=tk.WORD, width=50, height=20, state='normal'
        )
        self.chat_display.pack(padx=10, pady=10)

        #Pole edycyjne do wprowadzania tekstu rozpoznanego przez system
        self.user_input_voice = tk.Text(
            self.root, wrap=tk.WORD, width=50, height=2
        )
        self.user_input_voice.insert(tk.END, "")
        self.user_input_voice.pack(padx=10, pady=10)

        #Etykieta do wyświetlania rozpoznanego tekstu
        self.user_input_voice_partial = tk.Label(
            self.root, width=50, text="Aby rozpocząć mówienie wciśnij przycisk mikrofonu", anchor="w"
        )
        self.user_input_voice_partial.pack(padx=10, pady=10)

        #Etykieta do wyświetlania stanu systemu
        self.system_status = tk.Label(
            self.root,
            text="rozpoczęcie rozmowy",
            fg="blue",
            font=("Arial", 10, "italic")
        )
        self.system_status.pack(padx=10, pady=5)

        #Przycisk mikrofonu do sterowania nagrywaniem - start/stop nagrywania
        self.speaking_button = tk.Button(
            self.root,
            image=self.green_mic_image,
            command=self.parent.ev_speaking_button,
            borderwidth=0
        )
        self.speaking_button.pack(padx=10, pady=5)

        #Przycisk potwierdzenia tekstu
        self.confirm_button = tk.Button(
            self.root,
            text="Potwierdź",
            command=self.parent.ev_confirm_button,
            width=7
        )
        self.confirm_button.pack(padx=10, pady=5)

        self.root.protocol("WM_DELETE_WINDOW", self.__del__)

    def update_status_label(self, status: str):
        """
        Aktualizuje etykietę stanu systemu w GUI.

        Args:
            status (str): Tekst reprezentujący aktualny stan systemu.
        """
        self.system_status.config(text=status)

    def update_speaking_button(self, is_speaking):
        """
        Aktualizuje ikonę przycisku mikrofonu w zależności od stanu nagrywania.

        Args:
            is_speaking (bool): True, jeśli nagrywanie jest aktywne, False w przeciwnym przypadku.
        """
        if is_speaking:
            self.speaking_button.config(image=self.red_mic_image)
        else:
            self.speaking_button.config(image=self.green_mic_image)

    def start(self):
        """
        Rozpoczyna główną pętlę aplikacji GUI.
        """
        self.root.mainloop()

    def generate_icons(self):
        """
        Ładuje ikony przycisków mikrofonu z plików graficznych.

        Obsługuje błędy ładowania ikon i loguje odpowiednie informacje.
        """
        try:
            self.green_mic_image = ImageTk.PhotoImage(Image.open("green_mic.png"))
            self.red_mic_image = ImageTk.PhotoImage(Image.open("red_mic.png"))
        except Exception as e:
            self.logger.error(f"Error loading mic icons: {e}")
            self.green_mic_image = None
            self.red_mic_image = None

    def __del__(self):
        """
        Obsługuje zamykanie GUI i wywołuje zdarzenie zamknięcia w klasie nadrzędnej.
        """
        self.logger.debug("Zamykanie GUI")
        self.root.destroy()
        self.parent.on_closing()
