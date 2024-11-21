from gtts import gTTS
import pygame
import os
import tempfile
import threading


class SoundEngine:
    def __init__(self, lang='pl'):
        """
        Inicjalizuje silnik dźwięku z określonym językiem dla gTTS.
        """
        self.lang = lang
        self.temp_dir = tempfile.gettempdir()  # Katalog tymczasowy
        self.current_thread = None  # Aktualny wątek odtwarzania
        pygame.init()
        pygame.mixer.init()

    def say(self, text):
        """
        Generuje dźwięk na podstawie tekstu i odtwarza go w tle.
        Jeśli inne odtwarzanie trwa, zostaje przerwane.

        Args:
            text (str): Tekst do wymówienia.
        """
        # Jeśli istnieje aktywny wątek, zatrzymaj odtwarzanie i poczekaj na jego zakończenie
        if self.current_thread and self.current_thread.is_alive():
            pygame.mixer.music.stop()
            self.current_thread.join()

        # Tworzenie i uruchamianie nowego wątku
        self.current_thread = threading.Thread(target=self._play_sound, args=(text,))
        self.current_thread.start()

    def _play_sound(self, text):
        """
        Funkcja pomocnicza: generuje dźwięk i odtwarza go.
        """
        try:
            # Utwórz tymczasowy plik audio
            temp_file = os.path.join(self.temp_dir, "temp_sound.mp3")
            tts = gTTS(text=text, lang=self.lang)
            tts.save(temp_file)

            # Odtwarzanie dźwięku
            pygame.mixer.music.load(temp_file)
            pygame.mixer.music.play()

            # Czekanie na zakończenie odtwarzania
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)

        except Exception as e:
            print(f"Error: {e}")

    def __del__(self):
        """
        Czyszczenie zasobów podczas usuwania obiektu.
        """
        if self.current_thread and self.current_thread.is_alive():
            pygame.mixer.music.stop()
            self.current_thread.join()
        pygame.mixer.quit()
        pygame.quit()
