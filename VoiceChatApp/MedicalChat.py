import random
import logging
from .SpeechLibrary import SpeechLibrary
from .AiModel import AiModel


class MedicalChat:
    """
    Klasa MedicalChat odpowiada za analizę objawów zgłaszanych przez użytkownika,
    zarządzanie pytaniami pomocniczymi oraz generowanie rekomendacji medycznych.
    """

    def __init__(self, debug=False):
        """
        Inicjalizuje obiekt klasy MedicalChat.

        Args:
            debug (bool): Flaga określająca, czy włączyć tryb debugowania.
        """
        # Konfiguracja loggera
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.DEBUG if debug else logging.INFO)

        # Inicjalizacja zmiennych
        self.symptoms_table = SpeechLibrary.symptoms_table
        self.required_symptoms = SpeechLibrary.required_symptoms
        self.synonyms = SpeechLibrary.synonyms
        self.user_symptoms = {}
        self.check_syndroms = {}
        self.first_info_pack = True
        self.prev_question = None
        self.ai_model = AiModel()
        # Flaga wskazująca, czy przekazaliśmy już diagnozę i czekamy na odpowiedź
        # na pytanie "Czy mogę coś dla ciebie zrobić?"
        self.waiting_post_diagnosis = False

    def reset_conversation(self):
        """
        Resetuje stan analizy objawów, aby rozpocząć nową rozmowę.
        """
        self.user_symptoms = {}
        self.check_syndroms = {}
        self.first_info_pack = True
        self.prev_question = None
        self.waiting_post_diagnosis = False
        self.logger.info("Rozpoczęto nową rozmowę medyczną.")

    def analyze_monolog(self, user_input):
        """
        Analizuje początkowy monolog użytkownika i identyfikuje obecne objawy.

        Args:
            user_input (str): Wprowadzenie użytkownika z potencjalnymi objawami.
        """
        for symptom in self.required_symptoms:
            # Domyślnie ustawiamy, że objawu nie wykryto.
            symptom_present = False

            # Sprawdzamy, czy dokładna fraza kluczowa znajduje się w monologu.
            if symptom.lower() in user_input.lower():
                symptom_present = True
            else:
                # Jeśli nie – sprawdzamy synonimy.
                symptom_key_lower = symptom.lower()
                for syn_key, syn_list in self.synonyms.items():
                    if syn_key.lower() == symptom_key_lower:
                        for s in syn_list:
                            if s.lower() in user_input.lower():
                                symptom_present = True
                                break
                        break  # Koniec, gdy znaleziono dopasowanie.

            self.check_syndroms[symptom] = symptom_present
            self.user_symptoms[symptom] = symptom_present

            for phrase in SpeechLibrary.no_other_symptoms_phrases:
                if phrase in user_input.lower():
                    self.logger.info(f"Wykryto frazę sugerującą brak innych objawów: '{phrase}'")
                    for symptom in self.required_symptoms:
                        self.check_syndroms[symptom] = True
                    break

    def analyze_symptoms(self, user_input):
        """
        Główna funkcja analizy objawów użytkownika.

        Args:
            user_input (str): Wprowadzenie użytkownika do analizy.

        Returns:
            tuple: (bool, str)
                - bool: Czy wszystkie etapy analizy zostały zakończone.
                - str: Wiadomość zwrotna do użytkownika.
        """
        # Jeżeli po diagnozie czekamy na odpowiedź na pytanie "Czy przejsc caly proces od nowa?"
        if self.waiting_post_diagnosis:
            answer = self.does_agree(user_input)
            if answer is True:
                # Użytkownik akceptuje – resetujemy rozmowę
                self.reset_conversation()
                return True, SpeechLibrary.reset_response()
            elif answer is False:
                # Użytkownik nie potrzebuje dalszej pomocy – kończymy rozmowę
                self.waiting_post_diagnosis = False
                return True, SpeechLibrary.end_response()
            else:
                # Brak jednoznacznej odpowiedzi – pytamy jeszcze raz
                return False, "Czy mogę coś dla Ciebie zrobić? Proszę odpowiedz 'tak' lub 'nie'."

        # Standardowa analiza objawów
        if self.first_info_pack:
            self.analyze_monolog(user_input)
        else:
            answer = self.does_agree(user_input)
            if answer is not None:
                self.check_syndroms[self.prev_question] = True
                self.user_symptoms[self.prev_question] = answer
            else:
                self.check_syndroms[self.prev_question] = None
                self.user_symptoms[self.prev_question] = None
            self.prev_question = ""

        self.logger.info(f"Sprawdzone objawy: {self.check_syndroms}")
        self.logger.info(f"Objawy użytkownika: {self.user_symptoms}")

        if all(self.check_syndroms.values()):
            # Jeśli wszystkie objawy są znane – generujemy rekomendację
            i_know, message = True, self.get_recommendation()
            # Ustawiamy flagę, aby po przekazaniu diagnozy poczekać na odpowiedź
            self.waiting_post_diagnosis = True
        else:
            i_know, message = False, self.ask_missing_symptom()

        if self.first_info_pack:
            message = SpeechLibrary.first_response(self.user_symptoms, message)
            self.first_info_pack = False

        return i_know, message

    def does_agree(self, message):
        """
        Sprawdza, czy użytkownik odpowiedział twierdząco lub zaprzeczył.

        Args:
            message (str): Odpowiedź użytkownika.

        Returns:
            bool lub None: True dla potwierdzenia, False dla zaprzeczenia, None gdy odpowiedź jest niejednoznaczna.
        """
        self.logger.info(f"Analiza odpowiedzi: {message}")
        self.logger.info(f"Poprzednie pytanie: {self.prev_question}")
        for key, value in SpeechLibrary.response_yes_no_pattern.items():
            if key in message.lower():
                return value
        return None

    def ask_missing_symptom(self):
        """
        Pyta użytkownika o brakujące lub niejednoznaczne objawy.

        Returns:
            str: Pytanie o brakujące objawy.
        """
        for symptom, present in self.check_syndroms.items():
            if present is False:
                self.prev_question = symptom
                return SpeechLibrary.ask_first(symptom)
            elif present is None:
                self.prev_question = symptom
                return SpeechLibrary.ask_error(symptom)

        self.prev_question = None
        return SpeechLibrary.ask_error("objawy")

    def get_recommendation(self):
        """
        Generuje rekomendacje na podstawie zgłoszonych objawów oraz dodaje pytanie
        po przedstawieniu diagnozy.

        Returns:
            str: Komunikat z diagnozą(Zalecenia lub odpowiedź modelu AI) i pytaniem o dalszą pomoc.
        """
        diagnosis = None
        for disease in self.symptoms_table:
            if all(
                disease.get(symptom, False) == self.user_symptoms.get(symptom, False)
                for symptom in self.required_symptoms
            ):
                diagnosis = SpeechLibrary.find_disease(disease)
                break

        if diagnosis is None:
            diagnosis = self.ai_model.ask(
                f"Jaka to może być choroba i jakie zalecenia mi dasz. "
                f"Odpowiedz bardzo krótko w dwóch zdaniach. Objawy: {self.user_symptoms}"
            )

        # Dodajemy pytanie o dalszą pomoc.
        diagnosis += "\nCzy spełniłem twoje oczekiwania?"
        return diagnosis
