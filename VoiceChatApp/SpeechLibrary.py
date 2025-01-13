class SpeechLibrary:
    """
    Biblioteka obsługująca logikę rozmów w aplikacji medycznej, w tym:
    - Tabelę chorób z objawami i zaleceniami.
    - Obsługę odpowiedzi użytkownika na pytania o objawy.
    - Generowanie odpowiedzi i pytań opartych na danych wejściowych.
    """

    # Model wzorów chorobowych
    symptoms_table = [
        {
            "Choroba": "Grypa",
            "Ból głowy": True,
            "Wymioty": True,
            "Gorączka": True,
            "Ból kości i stawów": False,
            "Nudności": True,
            "Ból brzucha": False,
            "Kaszel": True,
            "Duszności": False,
            "Zmęczenie": True,
            "Utrata wagi": False,
            "Problemy ze snem": False,
            "Ból mięśni": True,
            "Dreszcze": True,
            "Specjalista": "Internista",
            "Zalecenia": "Odpoczynek, nawadnianie, leki przeciwgorączkowe"
        },
        {
            "Choroba": "Zapalenie płuc",
            "Ból głowy": False,
            "Wymioty": False,
            "Gorączka": True,
            "Ból kości i stawów": False,
            "Nudności": False,
            "Ból brzucha": False,
            "Kaszel": True,
            "Duszności": True,
            "Zmęczenie": True,
            "Utrata wagi": False,
            "Problemy ze snem": False,
            "Ból mięśni": True,
            "Dreszcze": True,
            "Specjalista": "Pulmonolog",
            "Zalecenia": "Antybiotyki, nawadnianie, odpoczynek"
        },
        {
            "Choroba": "Zapalenie wyrostka",
            "Ból głowy": False,
            "Wymioty": True,
            "Gorączka": True,
            "Ból kości i stawów": False,
            "Nudności": True,
            "Ból brzucha": True,
            "Kaszel": False,
            "Duszności": False,
            "Zmęczenie": True,
            "Utrata wagi": False,
            "Problemy ze snem": False,
            "Ból mięśni": False,
            "Dreszcze": True,
            "Specjalista": "Chirurg ogólny",
            "Zalecenia": "Natychmiastowa pomoc medyczna, operacja"
        },
        {
            "Choroba": "Migrena",
            "Ból głowy": True,
            "Wymioty": False,
            "Gorączka": False,
            "Ból kości i stawów": False,
            "Nudności": False,
            "Ból brzucha": False,
            "Kaszel": False,
            "Duszności": False,
            "Zmęczenie": True,
            "Utrata wagi": False,
            "Problemy ze snem": False,
            "Ból mięśni": False,
            "Dreszcze": False,
            "Specjalista": "Neurolog",
            "Zalecenia": "Leki przeciwbólowe, unikanie czynników wywołujących"
        },
        {
            "Choroba": "Infekcja wirusowa",
            "Ból głowy": True,
            "Wymioty": False,
            "Gorączka": True,
            "Ból kości i stawów": False,
            "Nudności": True,
            "Ból brzucha": False,
            "Kaszel": True,
            "Duszności": False,
            "Zmęczenie": True,
            "Utrata wagi": False,
            "Problemy ze snem": False,
            "Ból mięśni": True,
            "Dreszcze": True,
            "Specjalista": "Internista",
            "Zalecenia": "Odpoczynek, nawadnianie, leki objawowe"
        },
        {
            "Choroba": "Choroby autoimmunologiczne",
            "Ból głowy": True,
            "Wymioty": False,
            "Gorączka": True,
            "Ból kości i stawów": True,
            "Nudności": False,
            "Ból brzucha": False,
            "Kaszel": False,
            "Duszności": False,
            "Zmęczenie": True,
            "Utrata wagi": True,
            "Problemy ze snem": True,
            "Ból mięśni": True,
            "Dreszcze": True,
            "Specjalista": "Reumatolog",
            "Zalecenia": "Leki immunosupresyjne, regularne kontrole"
        },
        {
            "Choroba": "Nowotwory",
            "Ból głowy": True,
            "Wymioty": False,
            "Gorączka": True,
            "Ból kości i stawów": True,
            "Nudności": False,
            "Ból brzucha": False,
            "Kaszel": False,
            "Duszności": False,
            "Zmęczenie": True,
            "Utrata wagi": True,
            "Problemy ze snem": True,
            "Ból mięśni": True,
            "Dreszcze": True,
            "Specjalista": "Onkolog",
            "Zalecenia": "Diagnostyka, leczenie onkologiczne"
        },
        {
            "Choroba": "Zatrucie pokarmowe",
            "Ból głowy": True,
            "Wymioty": True,
            "Gorączka": False,
            "Ból kości i stawów": False,
            "Nudności": True,
            "Ból brzucha": True,
            "Kaszel": False,
            "Duszności": False,
            "Zmęczenie": False,
            "Utrata wagi": False,
            "Problemy ze snem": False,
            "Ból mięśni": False,
            "Dreszcze": True,
            "Specjalista": "Internista",
            "Zalecenia": "Nawadnianie, dieta lekkostrawna"
        },
        {
            "Choroba": "Cukrzyca",
            "Ból głowy": False,
            "Wymioty": False,
            "Gorączka": False,
            "Ból kości i stawów": False,
            "Nudności": False,
            "Ból brzucha": False,
            "Kaszel": False,
            "Duszności": False,
            "Zmęczenie": True,
            "Utrata wagi": True,
            "Problemy ze snem": True,
            "Ból mięśni": False,
            "Dreszcze": False,
            "Specjalista": "Diabetolog",
            "Zalecenia": "Monitorowanie poziomu cukru, dieta, leki"
        },
        {
            "Choroba": "Choroby tarczycy",
            "Ból głowy": True,
            "Wymioty": False,
            "Gorączka": True,
            "Ból kości i stawów": False,
            "Nudności": False,
            "Ból brzucha": False,
            "Kaszel": False,
            "Duszności": False,
            "Zmęczenie": True,
            "Utrata wagi": True,
            "Problemy ze snem": False,
            "Ból mięśni": False,
            "Dreszcze": False,
            "Specjalista": "Endokrynolog",
            "Zalecenia": "Badania hormonalne, leczenie hormonalne"
        },
        {
            "Choroba": "Zespół przewlekłego zmęczenia",
            "Ból głowy": True,
            "Wymioty": False,
            "Gorączka": False,
            "Ból kości i stawów": False,
            "Nudności": False,
            "Ból brzucha": False,
            "Kaszel": False,
            "Duszności": False,
            "Zmęczenie": True,
            "Utrata wagi": True,
            "Problemy ze snem": True,
            "Ból mięśni": True,
            "Dreszcze": False,
            "Specjalista": "Internista",
            "Zalecenia": "Odpoczynek, terapia, zmiana stylu życia"
        },
        {
            "Choroba": "Astma",
            "Ból głowy": False,
            "Wymioty": False,
            "Gorączka": False,
            "Ból kości i stawów": False,
            "Nudności": False,
            "Ból brzucha": False,
            "Kaszel": True,
            "Duszności": True,
            "Zmęczenie": True,
            "Utrata wagi": False,
            "Problemy ze snem": False,
            "Ból mięśni": False,
            "Dreszcze": False,
            "Specjalista": "Pulmonolog",
            "Zalecenia": "Leki rozszerzające oskrzela, unikanie alergenów"
        },
        {
            "Choroba": "Wrzody żołądka",
            "Ból głowy": False,
            "Wymioty": True,
            "Gorączka": False,
            "Ból kości i stawów": False,
            "Nudności": True,
            "Ból brzucha": True,
            "Kaszel": False,
            "Duszności": False,
            "Zmęczenie": True,
            "Utrata wagi": False,
            "Problemy ze snem": False,
            "Ból mięśni": False,
            "Dreszcze": False,
            "Specjalista": "Gastroenterolog",
            "Zalecenia": "Leki zobojętniające, dieta, unikanie stresu"
        },
        {
            "Choroba": "Mononukleoza",
            "Ból głowy": True,
            "Wymioty": False,
            "Gorączka": True,
            "Ból kości i stawów": False,
            "Nudności": True,
            "Ból brzucha": False,
            "Kaszel": False,
            "Duszności": False,
            "Zmęczenie": True,
            "Utrata wagi": True,
            "Problemy ze snem": False,
            "Ból mięśni": True,
            "Dreszcze": True,
            "Specjalista": "Internista",
            "Zalecenia": "Odpoczynek, nawadnianie, leki przeciwbólowe"
        },
        {
            "Choroba": "Zespół jelita drażliwego",
            "Ból głowy": False,
            "Wymioty": True,
            "Gorączka": False,
            "Ból kości i stawów": False,
            "Nudności": True,
            "Ból brzucha": True,
            "Kaszel": False,
            "Duszności": False,
            "Zmęczenie": True,
            "Utrata wagi": False,
            "Problemy ze snem": False,
            "Ból mięśni": False,
            "Dreszcze": False,
            "Specjalista": "Gastroenterolog",
            "Zalecenia": "Dieta, leki przeciwbólowe, terapia psychologiczna"
        },









        # Możliwość rozszerzenia o kolejne choroby
    ]

    # Lista zwrotów do zakończenia rozmowy
    end_speech_phrases = [
        "koniec", "dziękuję", "do widzenia"
    ]
    # zwroty do resetowania rozmowy
    reset_phrases = [
        "zacznijmy od nowa", "restart", "rozpocznij ponownie"
    ]

    # Lista zwrotów do resetowania rozmowy
    reset_speech_phrases = [
        "zacznijmy od nowa",
        "zacznijmy jeszcze raz",
        "chcę zacząć od nowa",
        "zacznijmy ponownie",
        "zrestartujmy rozmowę",
        "zróbmy to jeszcze raz",
        "zacznijmy od początku",
        "chciałbym zacząć od nowa",
        "rozpocznijmy ponownie",
        "przeładujmy rozmowę",
        "zacznijmy wszystko od początku",
        "zrestartujmy naszą rozmowę",
        "zacznijmy jeszcze raz od początku",
        "proszę zacząć od nowa",
        "proszę rozpocząć ponownie",
        "zacznijmy od nowa proszę",
        "zróbmy to od nowa",
        "zacznijmy naszą rozmowę od nowa",
        "powtórzmy rozmowę od początku",
        "chcę zacząć jeszcze raz",
        "zacznijmy rozmowę jeszcze raz",
    ]


    # Lista objawów do odpytania
    required_symptoms = [
        "Ból głowy", "Wymioty", "Gorączka", "Ból kości i stawów",
        "Nudności", "Ból brzucha", "Kaszel", "Duszności",
        "Zmęczenie", "Utrata wagi", "Problemy ze snem", "Ból mięśni","Dreszcze"
    ]
    synonyms = {
        "Ból głowy": [
            "boli mnie głowa",
            "głowa mnie boli",
            "bol glowy",
            "migrena",
            "pulsuje mi w głowie",
            "pulsujący ból głowy"
        ],
        "Wymioty": [
            "rzyganie",
            "zwracam treść pokarmową",
            "chce mi się wymiotować"
        ],
        "Gorączka": [
            "temperatura 38",
            "wysoka temperatura",
            "mam ponad 37 stopni"
        ],
        "Ból kości i stawów": [
            "łamanie w kościach",
            "stawy mnie bolą"
        ],
        "Nudności": [
            "mdłości",
            "jest mi niedobrze",
            "zbiera mi się na wymioty"
        ],
        "Ból brzucha": [
            "boli mnie brzuch",
            "ból w okolicy żołądka"
        ],
        "Kaszel": [
            "kaszlę",
            "pokasłuję"
        ],
        "Duszności": [
            "ciężko mi oddychać",
            "brakuje mi tchu"
        ],
        "Zmęczenie": [
            "jestem wyczerpany",
            "brak mi energii"
        ],
        "Utrata wagi": [
            "schudłem",
            "chudnę ostatnio"
        ],
        "Problemy ze snem": [
            "bezsenność",
            "ciężko mi zasnąć",
            "nie mogę spać"
        ],
        "Ból mięśni": [
            "mięśnie mnie bolą",
            "zakwasy",
            "ciągnie mnie w mięśniach"
        ],
        "Dreszcze": [
            "mam dreszcze",
            "trzęsie mnie"
        ]
    }

    # Wzorce odpowiedzi użytkownika (tak/nie) - kolejność od najbardziej zaawansowanej
    response_yes_no_pattern = {
        # Odpowiedzi pozytywne
        "tak": True,
        "oczywiście": True,
        "występują": True,
        "mają miejsce": True,
        "potwierdzam": True,
        "prawda": True,
        "bez wątpienia": True,
        "pewnie": True,
        "zdecydowanie": True,
        "z całą pewnością": True,
        "zgadzam się": True,
        "to prawda": True,
        "dokładnie": True,
        "absolutnie": True,
        "tak jest": True,
        "na pewno": True,
        "zdecydowanie tak": True,

        # Odpowiedzi negatywne
        "zdecydowanie nie": False,
        "nie": False,
        "nie, dziękuję": False,
        "nie występuje": False,
        "brak": False,
        "nie ma": False,
        "nie potwierdzam": False,
        "absolutnie nie": False,
        "zdecydowanie nie": False,
        "nie zgadzam się": False,
        "to nieprawda": False,
        "niewystępują": False,
        "nie do końca": False,
        "nie jestem pewien": None,
        "nie wiem": None,
        "trudno powiedzieć": None,
        "nie jestem pewna": None,
        "nie jestem przekonany": None,
    }

    # Lista skrótów
    additional_yes_no_abbreviations = {
        "t": True,
        "n": False,
        "y": True,
    }

    # Integracja dodatkowych skrótów
    response_yes_no_pattern.update(additional_yes_no_abbreviations)


    # Zwrot witający
    hello_phrase = "Cześć! Opisz mi co Ci dolega."

    @staticmethod
    def is_reset_command(message: str) -> bool:
            """
            Sprawdza, czy wiadomość użytkownika jest komendą resetującą rozmowę.

            Args:
                message (str): Wiadomość użytkownika.

            Returns:
                bool: True jeśli jest komendą resetującą, False w przeciwnym razie.
            """
            message = message.lower()
            reset = any(phrase in message for phrase in SpeechLibrary.reset_speech_phrases)
            return reset
    

    @staticmethod
    def first_response(user_symptoms: dict, message: str) -> str:
        """
        Generuje pierwszą odpowiedź po monologu użytkownika.

        Args:
            user_symptoms (dict): Słownik z objawami użytkownika (objaw: True/False).
            message (str): Komunikat bazowy.

        Returns:
            str: Sformatowana odpowiedź.
        """
        active_symptoms = [symptom for symptom, has_symptom in user_symptoms.items() if has_symptom]
        if active_symptoms:
            symptoms_str = ", ".join(active_symptoms)
            message = f"Rozumiem. Czyli twoje objawy to: {symptoms_str}. {message}"
        else:
            message = f"Rozumiem. {message}"
        return message

    @staticmethod
    def ask_first(symptom: str) -> str:
        """
        Generuje pytanie o określony objaw.

        Args:
            symptom (str): Nazwa objawu.

        Returns:
            str: Pytanie o objaw.
        """
        return f"Czy występują u Ciebie objawy takie jak {symptom.lower()}?"

    @staticmethod
    def ask_error(symptom: str) -> str:
        """
        Generuje pytanie ponowne o określony objaw w przypadku niezrozumienia.

        Args:
            symptom (str): Nazwa objawu.

        Returns:
            str: Ponowne pytanie o objaw.
        """
        return f"Czy możesz powtórzyć? Czy występują u Ciebie objawy takie jak {symptom.lower()}?"

    @staticmethod
    def error() -> str:
        """
        Generuje komunikat błędu.

        Returns:
            str: Komunikat błędu.
        """
        return "Coś poszło nie tak :("

    @staticmethod
    def find_disease(disease: dict) -> str:
        """
        Generuje odpowiedź z zaleceniami i specjalistą dla zidentyfikowanej choroby.

        Args:
            disease (dict): Dane choroby.

        Returns:
            str: Odpowiedź z zaleceniami.
        """
        return (f"Najprawdopodobniej dolega ci {disease['Choroba']}\n"
                f"Zalecany specjalista: {disease['Specjalista']}\n"
                f"Zalecenia: {disease['Zalecenia']}")

    @staticmethod
    def not_find_disease() -> str:
        """
        Generuje odpowiedź w przypadku, gdy nie można zidentyfikować choroby.

        Returns:
            str: Komunikat o braku jednoznacznej diagnozy.
        """
        return "Nie mogę jednoznacznie stwierdzić, co to za choroba."

    @staticmethod
    def is_end_of_conversation(message: str) -> bool:
        """
        Sprawdza, czy użytkownik chce zakończyć rozmowę.

        Args:
            message (str): Wiadomość użytkownika.

        Returns:
            bool: True, jeśli rozmowa powinna się zakończyć; w przeciwnym razie False.
        """
        return any(phrase in message.lower() for phrase in SpeechLibrary.end_speech_phrases)

    @staticmethod
    def reset_conversation(message: str) -> bool:
        """
        Sprawdza, czy użytkownik chce zresetować rozmowę i zacząć od nowa.

        Args:
            message (str): Wiadomość użytkownika.

        Returns:
            bool: True, jeśli użytkownik chce zresetować rozmowę, w przeciwnym razie False.
        """
        return any(phrase in message.lower() for phrase in SpeechLibrary.reset_phrases)

    def reset_response(self) -> str:
        """
        Odpowiedź po zresetowaniu rozmowy.

        Returns:
            str: Komunikat o rozpoczęciu nowej rozmowy.
        """
        return "Rozumiem, tak więc opisz mi jeszcze raz co Ci dolega."

    @staticmethod
    def get_symptom_confirmation_status(message: str) -> bool:
        """
        Sprawdza, czy wiadomość użytkownika zawiera odpowiedź twierdzącą lub przeczącą.

        Args:
            message (str): Wiadomość użytkownika.

        Returns:
            bool or None: True/False w przypadku odpowiedzi, None jeśli brak rozpoznania.
        """
        for key, value in SpeechLibrary.response_yes_no_pettern.items():
            if key in message.lower():
                return value
        return None
