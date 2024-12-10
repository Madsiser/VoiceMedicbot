import tkinter as tk
from tkinter import scrolledtext
import logging
from PIL import Image, ImageTk, ImageDraw

class ChatGUI:
    """
    Klasa ChatGUI odpowiada za zarządzanie graficznym interfejsem użytkownika (GUI) aplikacji czatu głosowego.
    Obsługuje wyświetlanie wiadomości, rozpoznanego tekstu oraz przyciski do sterowania nagrywaniem.
    """

    def __init__(self, parent, debug=False):
        """
        Inicjalizuje obiekt GUI i jego komponenty.

        Args:
            parent (VoiceChatApp): Referencja do głównego obiektu aplikacji (VoiceChatApp).
            debug (bool): Flaga określająca, czy włączyć tryb debugowania (wyższy poziom logowania).
        """
        from VoiceChatApp import VoiceChatApp
        if not isinstance(parent, VoiceChatApp):
            raise TypeError(
                f"Expected parent to be an instance of VoiceChatApp, got {type(parent).__name__} instead."
            )

        self.parent = parent
        self.logger = logging.getLogger(__name__)
        # Ustawienie poziomu logowania w zależności od flagi debug
        logging.basicConfig(level=logging.DEBUG if debug else logging.INFO)

        # Utworzenie głównego okna aplikacji
        self.root = tk.Tk()
        self.root.title("Czat Głosowy")

        # Wygeneruj ikony mikrofonów (zielony i czerwony przekreślony)
        self.generate_icons()

        # Utworzenie i rozmieszczenie wszystkich widżetów GUI
        self.create_widgets()

    def start(self):
        """
        Uruchamia główną pętlę zdarzeń interfejsu graficznego (GUI).
        """
        self.root.mainloop()

    def generate_icons(self):
        """
        Generuje ikony dla przycisku mikrofonu.
        Ikona zielona - mikrofon wyłączony (gotowy do nagrywania).
        Ikona czerwona z przekreśleniem - mikrofon włączony (nagrywanie trwa).
        """
        self.green_mic_image = self.create_mic_icon(fill_color="green")
        self.red_mic_image = self.create_mic_icon(fill_color="red", cross=True)

    def create_mic_icon(self, fill_color="green", cross=False):
        """
        Tworzy ikonę mikrofonu za pomocą biblioteki PIL (Pillow).

        Args:
            fill_color (str): Kolor mikrofonu (np. "green", "red").
            cross (bool): Czy dodać przekreślenie mikrofonu (stosowane, gdy nagrywanie jest włączone).

        Returns:
            ImageTk.PhotoImage: Obiekt obrazu, który można przypisać do widgetu Tkinter (np. przycisku).
        """
        size = (50, 50)  # Rozmiar ikony
        # Tworzenie obrazu z przezroczystym tłem (RGBA)
        image = Image.new("RGBA", size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(image)

        # Rysowanie mikrofonu
        # Główka mikrofonu (elipsa)
        draw.ellipse((20, 10, 30, 25), fill=fill_color)
        # Trzonek mikrofonu (prostokąt)
        draw.rectangle((24, 25, 26, 35), fill=fill_color)
        # Podstawa mikrofonu (łuk)
        draw.arc((18, 30, 32, 40), start=0, end=180, fill=fill_color)

        # Jeśli cross=True, to dodajemy dwie linie przekreślające mikrofon
        if cross:
            draw.line((15, 15, 35, 35), fill="black", width=5)
            draw.line((15, 35, 35, 15), fill="black", width=5)

        # Konwersja obrazu PIL do formatu obsługiwanego przez Tkinter
        return ImageTk.PhotoImage(image)

    def create_widgets(self):
        """
        Tworzy wszystkie widżety interfejsu użytkownika i dodaje je do głównego okna.
        """
        self.logger.debug("Rozpoczynam tworzenie widżetów GUI")

        # Pole do wyświetlania czatu - ScrolledText z paskiem przewijania
        self.chat_display = scrolledtext.ScrolledText(
            self.root, wrap=tk.WORD, width=50, height=20, state='normal'
        )
        self.chat_display.pack(padx=10, pady=10)

        # Etykieta do wyświetlania rozpoznanego tekstu głównego
        self.user_input_voice = tk.Label(
            self.root, width=50, text="Tekst główny", anchor="w"
        )
        self.user_input_voice.pack(padx=10, pady=10)

        # Etykieta do wyświetlania częściowo rozpoznanego tekstu (pomocniczego)
        self.user_input_voice_partial = tk.Label(
            self.root, width=50, text="Tekst pomocniczy", anchor="w"
        )
        self.user_input_voice_partial.pack(padx=10, pady=10)

        # Przycisk mikrofonu - start/stop nagrywania
        # Domyślnie pokazujemy zieloną ikonę (nagrywanie wyłączone)
        self.speaking_button = tk.Button(
            self.root,
            image=self.green_mic_image,
            command=self.parent.ev_speaking_button,
            borderwidth=0
        )
        self.speaking_button.pack(padx=10, pady=5)

        # Przycisk do potwierdzenia tekstu (po zakończeniu nagrywania lub ręcznej edycji)
        self.confirm_button = tk.Button(
            self.root,
            text="Potwierdź",
            command=self.parent.ev_confirm_button,
            width=7
        )
        self.confirm_button.pack(padx=10, pady=5)

        # Obsługa zamykania okna aplikacji (kliknięcie "X")
        self.root.protocol("WM_DELETE_WINDOW", self.__del__)

    def update_speaking_button(self, is_speaking):
        """
        Aktualizuje ikonę przycisku mówienia w zależności od stanu nagrywania.

        Args:
            is_speaking (bool): True jeśli aktualnie nagrywamy, False jeśli nagrywanie jest wyłączone.
        """
        if is_speaking:
            # Jeśli nagrywanie jest włączone - pokazujemy czerwoną, przekreśloną ikonę
            self.speaking_button.config(image=self.red_mic_image)
        else:
            # Jeśli nagrywanie jest wyłączone - pokazujemy zieloną ikonę
            self.speaking_button.config(image=self.green_mic_image)

    def __del__(self):
        """
        Zamyka aplikację, zwalnia zasoby i wywołuje funkcję zamykającą w głównej aplikacji.
        """
        self.logger.debug("Zamykanie GUI")
        self.root.destroy()  # Zamyka okno główne
        self.parent.on_closing()  # Wywołuje metodę zamykającą w obiekcie głównej aplikacji
