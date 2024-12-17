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

        # Możliwość rozszerzenia o kolejne choroby
    ]

    # Lista zwrotów do zakończenia rozmowy
    end_speech_phrases = [
        "koniec", "dziękuję", "do widzenia"
    ]

    # Lista objawów do odpytania
    required_symptoms = [
        "Ból głowy", "Wymioty", "Gorączka", "Ból kości i stawów",
        "Nudności", "Ból brzucha", "Kaszel", "Duszności",
        "Zmęczenie", "Utrata wagi", "Problemy ze snem", "Ból mięśni", "Dreszcze"
    ]

    synonyms = {
        "ból głowy": [
            "głowa mnie boli",
            "bol glowy",
            "migrena",
            "pulsuje mi w głowie",
            "pulsujący ból głowy"
        ],
        "wymioty": [
            "rzyganie",
            "zwracam treść pokarmową",
            "chce mi się wymiotować"
        ],
        "gorączka": [
            "temperatura 38",
            "wysoka temperatura",
            "mam ponad 37 stopni"
        ],
        "ból kości i stawów": [
            "łamanie w kościach",
            "stawy mnie bolą"
        ],
        "nudności": [
            "mdłości",
            "jest mi niedobrze",
            "zbiera mi się na wymioty"
        ],
        "ból brzucha": [
            "boli mnie brzuch",
            "ból w okolicy żołądka"
        ],
        "kaszel": [
            "kaszlę",
            "pokasłuję"
        ],
        "duszności": [
            "ciężko mi oddychać",
            "brakuje mi tchu"
        ],
        "zmęczenie": [
            "jestem wyczerpany",
            "brak mi energii"
        ],
        "utrata wagi": [
            "schudłem",
            "chudnę ostatnio"
        ],
        "problemy ze snem": [
            "bezsenność",
            "ciężko mi zasnąć",
            "nie mogę spać"
        ],
        "ból mięśni": [
            "mięśnie mnie bolą",
            "zakwasy",
            "ciągnie mnie w mięśniach"
        ],
        "dreszcze": [
            "mam dreszcze",
            "trzęsie mnie"
        ]
    }
    # Wzorce odpowiedzi użytkownika (tak/nie) kolejnośc od najbardziej zaawansowanej
    response_yes_no_pettern = {
        "tak": True,
        "występują": True,
        "mają miejsce": True,
        "nie": False,
        "nie występuje": False,
        "brak": False,
        "t": True,
        "n": False
    }

    # Zwrot witający
    hello_phrase = "Cześć! Opisz mi co Ci dolega."

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
        return (f"Zalecany specjalista: {disease['Specjalista']}\n"
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