from io import BytesIO

from gtts import gTTS
import pygame
import tempfile
import threading
import logging


class SoundEngine:
    """
    Klasa SoundEngine zarządza generowaniem i odtwarzaniem dźwięku za pomocą gTTS i Pygame.
    """

    def __init__(self, lang='pl', debug=False):
        """
        Inicjalizuje silnik dźwięku z określonym językiem dla gTTS.

        Args:
            lang (str): Kod języka (np. 'pl' dla polskiego, 'en' dla angielskiego).
            debug (bool): Flaga włączająca tryb debugowania logów. Domyślnie False.
        """
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.DEBUG if debug else logging.INFO)

        self.lang = lang
        self.temp_dir = tempfile.gettempdir()
        self.current_thread = None
        pygame.init()
        pygame.mixer.init()

    def say(self, text: str):
        """
        Generuje dźwięk na podstawie podanego tekstu i odtwarza go w tle.
        Przerywa aktualne odtwarzanie, jeśli takie istnieje.

        Args:
            text (str): Tekst do wymówienia.
        """
        self.logger.debug("Wywołanie say")
        # Zatrzymywanie aktywnego odtwarzania, jeśli istnieje wątek odtwarzania
        if self.current_thread and self.current_thread.is_alive():
            pygame.mixer.music.stop()
            self.current_thread.join()

        # Tworzenie nowego wątku do odtwarzania dźwięku
        self.current_thread = threading.Thread(target=self._play_sound, args=(text,), daemon=True)
        self.current_thread.start()

    def _play_sound(self, text: str):
        """
        Funkcja pomocnicza: generuje dźwięk i odtwarza go.

        Args:
            text (str): Tekst do wygenerowania i odtworzenia.
        """
        try:
            tts = gTTS(text=text, lang=self.lang)
            mp3 = BytesIO()
            tts.write_to_fp(mp3)
            mp3.seek(0)

            pygame.mixer.music.load(mp3)
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)

        except Exception as e:
            print(f"Błąd podczas odtwarzania dźwięku: {e}")

    def __del__(self):
        """
        Usuwa zasoby używane przez silnik dźwięku podczas niszczenia obiektu.
        Zatrzymuje odtwarzanie i zwalnia zasoby Pygame.
        """
        if self.current_thread and self.current_thread.is_alive():
            pygame.mixer.music.stop()
            self.current_thread.join()
        pygame.mixer.quit()
        pygame.quit()
