import tkinter as tk
from tkinter import scrolledtext
import logging
from PIL import Image, ImageTk, ImageDraw

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

        # Generowanie ikon mikrofonów
        self.generate_icons()

        # Tworzenie widżetów interfejsu
        self.create_widgets()

    def start(self):
        """
        Uruchamia główną pętlę GUI.
        """
        self.root.mainloop()

    def generate_icons(self):
        """Generuje ikony zielonego i czerwonego przekreślonego mikrofonu."""
        self.green_mic_image = self.create_mic_icon(fill_color="green")
        self.red_mic_image = self.create_mic_icon(fill_color="red", cross=True)

    def create_mic_icon(self, fill_color="green", cross=False):
        """Tworzy ikonę mikrofonu z użyciem biblioteki PIL.

        Args:
            fill_color (str): Kolor mikrofonu (np. "green", "red").
            cross (bool): Czy dodać przekreślenie mikrofonu.

        Returns:
            ImageTk.PhotoImage: Obiekt obrazu do użycia w tkinter.
        """
        size = (50, 50)
        image = Image.new("RGBA", size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(image)

        # Główka mikrofonu
        draw.ellipse((20, 10, 30, 25), fill=fill_color)
        # Trzonek mikrofonu
        draw.rectangle((24, 25, 26, 35), fill=fill_color)
        # Podstawa mikrofonu (łuk)
        draw.arc((18, 30, 32, 40), start=0, end=180, fill=fill_color)

        if cross:
            # Dodanie przekreślenia gdy mikrofon jest aktywny
            draw.line((15, 15, 35, 35), fill="black", width=5)
            draw.line((15, 35, 35, 15), fill="black", width=5)

        return ImageTk.PhotoImage(image)

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

        # Przycisk: Rozpocznij/Zatrzymaj mówienie (ikona mikrofonu)
        # Domyślnie mikrofon jest wyłączony - zielona ikona
        self.speaking_button = tk.Button(self.root,
                                         image=self.green_mic_image,
                                         command=self.parent.ev_speaking_button,
                                         borderwidth=0)
        self.speaking_button.pack(padx=10, pady=5)

        # Przycisk: Potwierdź tekst
        self.confirm_button = tk.Button(self.root,
                                        text="Potwierdź",
                                        command=self.parent.ev_confirm_button,
                                        width=7)
        self.confirm_button.pack(padx=10, pady=5)

        # Zamykanie aplikacji przez kliknięcie "X"
        self.root.protocol("WM_DELETE_WINDOW", self.__del__)

    def update_speaking_button(self, is_speaking):
        """
        Aktualizuje ikonę przycisku mówienia w zależności od stanu.

        Args:
            is_speaking (bool): Czy aktualnie jest w trybie nagrywania.
        """
        if is_speaking:
            # Mikrofon włączony - czerwona przekreślona ikona
            self.speaking_button.config(image=self.red_mic_image)
        else:
            # Mikrofon wyłączony - zielona ikona
            self.speaking_button.config(image=self.green_mic_image)



    def __del__(self):
        """
        Zamyka aplikację, zwalnia zasoby i wywołuje funkcję zamykającą w głównej aplikacji.
        """
        self.logger.debug("Zamykanie GUI")
        self.root.destroy()
        self.parent.on_closing()
