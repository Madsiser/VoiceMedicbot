import logging
from .SpeechLibrary import SpeechLibrary
from .AiModel import AiModel


class MedicalChat:
    """
    Klasa MedicalChat obsługuje analizę zgłoszonych objawów, generowanie pytań uzupełniających
    oraz rekomendacji medycznych.

    Funkcjonalności:

    - Analiza początkowego monologu użytkownika w celu identyfikacji objawów.

    - Tworzenie pytań uzupełniających na podstawie brakujących danych.

    - Generowanie diagnoz i rekomendacji medycznych za pomocą wbudowanych reguł lub modelu AI.
    """

    def __init__(self, debug=False):
        """
        Inicjalizuje obiekt klasy MedicalChat, konfigurując logger i zmienne pomocnicze.

        Args:
            debug (bool): Flaga włączająca tryb debugowania. Domyślnie False.
        """
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.DEBUG if debug else logging.INFO)

        self.symptoms_table = SpeechLibrary.symptoms_table
        self.required_symptoms = SpeechLibrary.required_symptoms
        self.synonyms = SpeechLibrary.synonyms
        self.user_symptoms = {}
        self.check_syndroms = {}
        self.first_info_pack = True
        self.prev_question = None
        self.ai_model = AiModel()
        self.waiting_post_diagnosis = False

    def reset_conversation(self):
        """
        Resetuje wszystkie zmienne związane z analizą objawów, przygotowując system
        do rozpoczęcia nowej rozmowy medycznej.
        """
        self.user_symptoms = {}
        self.check_syndroms = {}
        self.first_info_pack = True
        self.prev_question = None
        self.waiting_post_diagnosis = False
        self.logger.info("Rozpoczęto nową rozmowę medyczną.")

    def analyze_monolog(self, user_input):
        """
        Analizuje początkowy monolog użytkownika, identyfikując obecne objawy oraz potencjalne
        frazy wskazujące na brak innych dolegliwości.

        Args:
            user_input (str): Tekstowy monolog użytkownika zawierający informacje o objawach.
        """
        for symptom in self.required_symptoms:
            # Domyślnie ustawiamy, że objawu nie wykryto.
            symptom_present = False

            # Sprawdzamy, czy dokładna fraza kluczowa znajduje się w monologu.
            if symptom.lower() in user_input.lower():
                symptom_present = True
            else:
                symptom_key_lower = symptom.lower()
                for syn_key, syn_list in self.synonyms.items():
                    if syn_key.lower() == symptom_key_lower:
                        for s in syn_list:
                            if s.lower() in user_input.lower():
                                symptom_present = True
                                break
                        break

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
        Główna funkcja analizująca objawy użytkownika i generująca odpowiedź.

        Args:
            user_input (str): Tekstowa odpowiedź użytkownika zawierająca objawy.

        Returns:
            tuple: (bool, str)
                - bool: Flaga wskazująca, czy analiza została zakończona.
                - str: Wiadomość zwrotna, w tym pytania uzupełniające lub rekomendacje.
        """
        # Jeżeli po diagnozie czekamy na odpowiedź na pytanie "Czy przejsc caly proces od nowa?"
        if self.waiting_post_diagnosis:
            answer = self.does_agree(user_input)
            if answer is False:
                # Użytkownik nie jest zadowolony – resetujemy rozmowę
                self.reset_conversation()
                return True, SpeechLibrary.reset_response()
            elif answer is True:
                # Użytkownik nie potrzebuje dalszej pomocy – kończymy rozmowę
                self.waiting_post_diagnosis = False
                return True, SpeechLibrary.end_response()
            else:
                # Brak jednoznacznej odpowiedzi – pytamy jeszcze raz
                return False,

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
            i_know, message = True, self.get_recommendation()
            self.waiting_post_diagnosis = True
        else:
            i_know, message = False, self.ask_missing_symptom()

        if self.first_info_pack:
            message = SpeechLibrary.first_response(self.user_symptoms, message)
            self.first_info_pack = False

        return i_know, message

    def does_agree(self, message):
        """
        Sprawdza, czy użytkownik odpowiedział twierdząco lub zaprzeczył na pytanie.

        Args:
            message (str): Odpowiedź użytkownika.

        Returns:
            bool | None: True, jeśli odpowiedź jest twierdząca; False, jeśli zaprzeczająca;
                         None, jeśli odpowiedź jest niejednoznaczna.
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
        Generuje rekomendacje medyczne na podstawie zgłoszonych objawów.

        Jeśli nie można dopasować diagnozy na podstawie zdefiniowanych reguł,
        metoda korzysta z modelu AI do wygenerowania odpowiedzi.

        Returns:
            str: Komunikat zawierający diagnozę, zalecenia oraz pytanie o dalszą pomoc.
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

        diagnosis += "\nCzy spełniłem twoje oczekiwania?"
        return diagnosis
