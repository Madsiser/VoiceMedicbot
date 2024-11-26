from gtts import gTTS
import pygame
import os
import tempfile
import threading


class SoundEngine:
    """
    Klasa SoundEngine zarządza generowaniem i odtwarzaniem dźwięku za pomocą gTTS i Pygame.
    """

    def __init__(self, lang='pl'):
        """
        Inicjalizuje silnik dźwięku z określonym językiem dla gTTS.

        Args:
            lang (str): Kod języka (np. 'pl' dla polskiego, 'en' dla angielskiego).
        """
        self.lang = lang
        self.temp_dir = tempfile.gettempdir()  # Katalog tymczasowy dla plików audio
        self.current_thread = None  # Aktualny wątek odtwarzania
        pygame.init()
        pygame.mixer.init()

    def say(self, text: str):
        """
        Generuje dźwięk na podstawie podanego tekstu i odtwarza go w tle.
        Przerywa aktualne odtwarzanie, jeśli takie istnieje.

        Args:
            text (str): Tekst do wymówienia.
        """
        # Zatrzymaj aktywne odtwarzanie, jeśli istnieje wątek odtwarzania
        if self.current_thread and self.current_thread.is_alive():
            pygame.mixer.music.stop()
            self.current_thread.join()

        # Utwórz nowy wątek do odtwarzania dźwięku
        self.current_thread = threading.Thread(target=self._play_sound, args=(text,), daemon=True)
        self.current_thread.start()

    def _play_sound(self, text: str):
        """
        Funkcja pomocnicza: generuje dźwięk i odtwarza go.

        Args:
            text (str): Tekst do wygenerowania i odtworzenia.
        """
        try:
            # Ścieżka tymczasowego pliku audio
            temp_file = os.path.join(self.temp_dir, "temp_sound.mp3")

            # Generowanie pliku audio za pomocą gTTS
            tts = gTTS(text=text, lang=self.lang)
            tts.save(temp_file)

            # Odtwarzanie pliku audio za pomocą Pygame
            pygame.mixer.music.load(temp_file)
            pygame.mixer.music.play()

            # Czekaj, aż odtwarzanie zostanie zakończone
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
