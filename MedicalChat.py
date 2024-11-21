from SpeechLibrary import *
import logging
from AiModel import AiModel

class MedicalChat:

    def __init__(self, debug=False):
        # Ustawienie poziomu logowania
        self.logger = logging.getLogger(__name__)
        if debug:
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.basicConfig(level=logging.INFO)
        
        # Parametry
        self.symptoms_table = SpeechLibrary.symptoms_table
        self.required_symptoms = SpeechLibrary.required_symptoms
        self.user_symptoms = {}
        self.check_syndroms = {}
        self.first_info_pack = True
        self.prev_question = None

        self.ai_model = AiModel()

    # Funkcja odpowiadająca poczatkowy monolog klienta
    def analyze_monolog(self, user_input):
        for symptom in self.required_symptoms:
            self.check_syndroms[symptom] = symptom.lower() in user_input.lower()
            self.user_symptoms[symptom] = symptom.lower() in user_input.lower()

    # Główna funkcja
    def analyze_symptoms(self, user_input):
        # Inicjalizacja objawów
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

        logging.info(self.check_syndroms)
        logging.info(self.user_symptoms)

        # Sprawdzenie, czy wszystkie objawy są obecne
        if all(self.check_syndroms.values()):
            i_know, message = True, self.get_recommendation()
        else:
            i_know, message = False, self.ask_missing_symptom()
        if self.first_info_pack:
            message = SpeechLibrary.first_response(self.user_symptoms, message)
            self.first_info_pack = False
        return i_know, message
    
    # Funkcja sprawdzająca czy klient odpowiedział twierdzaco czy zaprzeczył
    def does_agree(self,message):
        logging.info(message)
        logging.info(self.prev_question)
        switcher = SpeechLibrary.response_yes_no_pettern
        for key in switcher:
            if key in message.lower(): 
                return switcher[key]
        return None

    # Funkcja odpowiedzialna za dopytanie klienta o nieokreślone syndromy
    def ask_missing_symptom(self):
        for symptom, present in self.check_syndroms.items():
            if present is False:
                self.prev_question = symptom
                return SpeechLibrary.ask_first(symptom)
            elif present is None:
                self.prev_question = symptom
                return SpeechLibrary.ask_error(symptom)
        return SpeechLibrary.ask_error(symptom)

    # Funkcja zwracająca zalecenia
    def get_recommendation(self):
        for disease in self.symptoms_table:
            if all(disease[symptom] == self.user_symptoms[symptom] for symptom in self.required_symptoms):
                return SpeechLibrary.find_disease(disease)
        response = self.ai_model.ask(f"Jaka to może być choroba i jakie zalecenia mi dasz. Odpowiedz mi bardzo krótko w dwóch zdaniach. Objawy:{self.user_symptoms}")
        return response
        # return SpeechLibrary.not_find_disease()
