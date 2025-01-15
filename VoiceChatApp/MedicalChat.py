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
        self.synonyms=SpeechLibrary.synonyms
        self.user_symptoms = {}
        self.check_syndroms = {}
        self.first_info_pack = True
        self.prev_question = None
        self.ai_model = AiModel()

    def reset_conversation(self):
            """
            Resetuje stan analizy objawów, aby rozpocząć nową rozmowę.
            """
            self.user_symptoms = {}
            self.check_syndroms = {}
            self.first_info_pack = True
            self.prev_question = None
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
                # Jeżeli nie - sprawdzamy synonimy zdefiniowane w słowniku "synonyms".
                # Uwaga: klucz w słowniku synonyms musi odpowiadać temu z required_symptoms,
                # np. "Ból głowy" -> "ból głowy" lub odwrotnie, żeby przyporządkowanie
                # było jednoznaczne. W razie potrzeby możesz to znormalizować.
                # Tu dla pewności zrobiono .lower() na kluczu i symptomie.
                symptom_key_lower = symptom.lower()
                for syn_key, syn_list in self.synonyms.items():
                    # Synonimy są pod kluczami typu "ból głowy", a w "required_symptoms" mamy np. "Ból głowy".
                    # Dlatego normalizujemy:
                    if syn_key.lower() == symptom_key_lower:
                        # Sprawdzamy każdy synonim:
                        for s in syn_list:
                            if s.lower() in user_input.lower():
                                symptom_present = True
                                break
                        break  # Kończymy, jeżeli znaleźliśmy dopasowanie w synonimach.

            # Uzupełniamy nasze tabele / słowniki dotyczące wykrytych objawów.
            self.check_syndroms[symptom] = symptom_present
            self.user_symptoms[symptom] = symptom_present

    def analyze_symptoms(self, user_input):
        """
        Główna funkcja analizy objawów użytkownika.

        Args:
            user_input (str): Wprowadzenie użytkownika do analizy.

        Returns:
            tuple: (bool, str)
                - bool: Czy znane są wszystkie objawy?
                - str: Wiadomość zwrotna do użytkownika.
        """
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
            bool or None: True dla odpowiedzi twierdzącej, False dla zaprzeczenia, None dla braku jednoznaczności.
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
        Generuje rekomendacje na podstawie zgłoszonych objawów.

        Returns:
            str: Zalecenia lub odpowiedź modelu AI.
        """
        for disease in self.symptoms_table:
            if all(
                disease.get(symptom, False) == self.user_symptoms.get(symptom, False)
                for symptom in self.required_symptoms
            ):
                return SpeechLibrary.find_disease(disease)

        response = self.ai_model.ask(
            f"Jaka to może być choroba i jakie zalecenia mi dasz. "
            f"Odpowiedz bardzo krótko w dwóch zdaniach. Objawy: {self.user_symptoms}"
        )
        return response
