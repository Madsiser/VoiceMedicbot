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
        self.user_symptoms = {}     # Słownik { "nazwa objawu": bool lub None }
        self.check_syndroms = {}    # Podobny słownik, informuje, czy objaw został ustalony (True/False) lub jest nieznany (None)
        self.first_info_pack = True # Oznacza, że jeszcze nie było analizy monologu
        self.prev_question = None   # Przechowuje nazwę ostatniego objawu, o który pytaliśmy
        self.ai_model = AiModel()

    def analyze_monolog(self, user_input):
        """
        Analizuje początkowy monolog użytkownika i identyfikuje obecne objawy.
        Uwzględnia synonimy zdefiniowane w SpeechLibrary.synonyms.

        Args:
            user_input (str): Monolog pacjenta z potencjalnymi objawami.
        """
        user_input_lower = user_input.lower()

        for symptom in self.required_symptoms:
            symptom_lower = symptom.lower()
            # Proste dopasowanie tekstowe
            symptom_present = symptom_lower in user_input_lower

            # Jeśli brak bezpośredniego dopasowania, sprawdzamy synonimy
            if not symptom_present:
                if symptom_lower in SpeechLibrary.synonyms:
                    for syn in SpeechLibrary.synonyms[symptom_lower]:
                        if syn.lower() in user_input_lower:
                            symptom_present = True
                            break

            # Uzupełniamy słowniki
            self.check_syndroms[symptom] = symptom_present
            self.user_symptoms[symptom] = symptom_present

    def analyze_symptoms(self, user_input):
        """
        Główna funkcja analizy objawów użytkownika.
        Najpierw (jeśli first_info_pack) analizuje monolog, a następnie pyta o brakujące objawy.

        Args:
            user_input (str): Wypowiedź użytkownika (monolog lub odpowiedź na dodatkowe pytanie).

        Returns:
            tuple: (bool, str)
                - bool: Czy znane są wszystkie objawy? (True/False)
                - str: Wiadomość zwrotna dla użytkownika (diagnoza lub pytania uzupełniające).
        """
        # Obsługa resetu rozmowy
        if SpeechLibrary.reset_conversation(user_input):
            # Resetowanie objawów użytkownika i zmiennych sterujących
            self.user_symptoms.clear()
            self.check_syndroms.clear()
            self.first_info_pack = True
            self.prev_question = None

            # Odpowiedź na reset
            reset_message = SpeechLibrary().reset_response()
            self.logger.info("Rozmowa została zresetowana.")
            return False, reset_message

        if self.first_info_pack:
            # Pierwsze wywołanie – analiza monologu
            self.analyze_monolog(user_input)
        else:
            # Odpowiedź na dodatkowe pytanie
            answer = self.does_agree(user_input)
            if answer is not None:
                # Użytkownik odpowiedział twierdząco/negatywnie
                self.check_syndroms[self.prev_question] = True
                self.user_symptoms[self.prev_question] = answer
            else:
                # Brak jasnej odpowiedzi
                self.check_syndroms[self.prev_question] = None
                self.user_symptoms[self.prev_question] = None
            self.prev_question = ""

        self.logger.info(f"Sprawdzone objawy: {self.check_syndroms}")
        self.logger.info(f"Objawy użytkownika: {self.user_symptoms}")

        # Sprawdzamy, czy wszystkie objawy zostały ustalone (True/False)
        if all(x is not None for x in self.check_syndroms.values()):
            i_know, message = True, self.get_recommendation()
        else:
            i_know, message = False, self.ask_missing_symptom()

        # Dodatkowa wiadomość powitalna przy pierwszym uruchomieniu
        if self.first_info_pack:
            message = SpeechLibrary.first_response(self.user_symptoms, message)
            self.first_info_pack = False

        return i_know, message

    def does_agree(self, message):
        """
        Sprawdza, czy użytkownik odpowiedział twierdząco lub zaprzeczył.

        Args:
            message (str): Odpowiedź użytkownika (np. "tak", "nie", "występują", itp.)

        Returns:
            bool or None: True/False w przypadku rozpoznania odpowiedzi, None jeśli brak jednoznaczności.
        """
        self.logger.info(f"Analiza odpowiedzi: {message}")
        self.logger.info(f"Poprzednie pytanie: {self.prev_question}")
        for key, value in SpeechLibrary.response_yes_no_pettern.items():
            if key in message.lower():
                return value
        return None

    def ask_missing_symptom(self):
        """
        Pyta użytkownika o objawy, które nie zostały jeszcze ustalone (False lub None).
        Jeśli objaw = False, oznacza że w monologu nie było wzmianki i dopytujemy 'czy występuje?'.
        Jeśli objaw = None, oznacza niejednoznaczną odpowiedź i ponawiamy pytanie.

        Returns:
            str: Komunikat/pytanie do użytkownika.
        """
        for symptom, present in self.check_syndroms.items():
            if present is False:
                # Objaw nie został potwierdzony – dopytujemy, czy jednak nie występuje
                self.prev_question = symptom
                return SpeechLibrary.ask_first(symptom)
            elif present is None:
                # Brak jednoznacznej odpowiedzi wcześniej
                self.prev_question = symptom
                return SpeechLibrary.ask_error(symptom)

        # Jeśli wszystko jest True albo w jakiś sposób pusta pętla,
        # ale nie przeszliśmy do get_recommendation(), pytamy ogólnie
        self.prev_question = None
        return SpeechLibrary.ask_error("objawy")

    def get_recommendation(self):
        """
        Generuje rekomendacje na podstawie tabeli chorób i/lub modelu AI.

        Returns:
            str: Krótka diagnoza lub odpowiedź modelu AI.
        """
        for disease in self.symptoms_table:
            # Porównujemy wymagane objawy z patternami z diseases
            if all(
                disease.get(symptom, False) == self.user_symptoms.get(symptom, False)
                for symptom in self.required_symptoms
            ):
                # Jeżeli wszystkie pasują do wzorca, zwracamy zalecenia
                return SpeechLibrary.find_disease(disease)

        # Jeśli nie znaleziono dopasowania w symptomach_table, pytamy model AI
        response = self.ai_model.ask(
            f"Jaka to może być choroba i jakie zalecenia mi dasz. "
            f"Odpowiedz bardzo krótko w dwóch zdaniach. Objawy: {self.user_symptoms}"
        )
        return response
