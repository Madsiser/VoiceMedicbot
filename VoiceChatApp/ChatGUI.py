import tkinter as tk
from tkinter import scrolledtext
import logging
from PIL import Image, ImageTk


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

        # Wczytaj ikony mikrofonów (zielony i czerwony)
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
        Wczytuje ikony mikrofonu z plików graficznych.
        Ikona zielona - mikrofon wyłączony (gotowy do nagrywania).
        Ikona czerwona - mikrofon włączony (nagrywanie trwa).
        """
        try:
            # Wczytywanie obrazów mikrofonu
            self.green_mic_image = ImageTk.PhotoImage(Image.open("green_mic.png"))
            self.red_mic_image = ImageTk.PhotoImage(Image.open("red_mic.png"))
        except Exception as e:
            self.logger.error(f"Error loading mic icons: {e}")
            self.green_mic_image = None
            self.red_mic_image = None

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

        # Pole tekstowe do edycji rozpoznanego tekstu głównego
        self.user_input_voice = tk.Text(
            self.root, wrap=tk.WORD, width=50, height=2
        )
        self.user_input_voice.insert(tk.END, "")
        self.user_input_voice.pack(padx=10, pady=10)

        # Etykieta do wyświetlania częściowo rozpoznanego tekstu (pomocniczego)
        self.user_input_voice_partial = tk.Label(
            self.root, width=50, text="Aby rozpocząć mówienie wciśnij przycisk mikrofonu", anchor="w"
        )
        self.user_input_voice_partial.pack(padx=10, pady=10)

        # Przycisk do potwierdzenia tekstu (po zakończeniu nagrywania lub ręcznej edycji)
        self.confirm_button = tk.Button(
            self.root,
            text="Potwierdź",
            command=self.parent.ev_confirm_button,
            width=7
        )
        self.confirm_button.pack(padx=10, pady=5)
        # Przycisk mikrofonu - start/stop nagrywania
        # Domyślnie pokazujemy zieloną ikonę (nagrywanie wyłączone)
        self.speaking_button = tk.Button(
            self.root,
            image=self.green_mic_image,
            command=self.parent.ev_speaking_button,
            borderwidth=0
        )
        self.speaking_button.pack(padx=10, pady=5)



        # Obsługa zamykania okna aplikacji (kliknięcie "X")
        self.root.protocol("WM_DELETE_WINDOW", self.__del__)

    def update_speaking_button(self, is_speaking):
        """
        Aktualizuje ikonę przycisku mówienia w zależności od stanu nagrywania.

        Args:
            is_speaking (bool): True jeśli aktualnie nagrywamy, False jeśli nagrywanie jest wyłączone.
        """
        if is_speaking:
            # Jeśli nagrywanie jest włączone - pokazujemy czerwoną ikonę
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