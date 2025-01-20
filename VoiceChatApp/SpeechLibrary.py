import random


class SpeechLibrary:
    """
    Klasa SpeechLibrary obsługuje logikę rozmów w aplikacji medycznej.

    Funkcjonalności:

    - Przechowywanie tabeli chorób wraz z objawami i zaleceniami.

    - Obsługa odpowiedzi użytkownika na pytania dotyczące objawów.

    - Generowanie losowych pytań oraz odpowiedzi na podstawie danych wejściowych.
    """

    # Modele wzorców chorobowych
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
    ]

    # Lista zwrotów do zakończenia rozmowy
    end_speech_phrases = [
        "koniec", "dziękuję", "do widzenia"
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
        "restart",
        "rozpocznij ponownie"
    ]

    # Lista objawów do odpytania
    required_symptoms = [
        "Ból głowy", "Wymioty", "Gorączka", "Ból kości i stawów",
        "Nudności", "Ból brzucha", "Kaszel", "Duszności",
        "Zmęczenie", "Utrata wagi", "Problemy ze snem", "Ból mięśni", "Dreszcze"
    ]

    # Lista synonimów objawów
    synonyms = {
        "Ból głowy": [
            "boli mnie głowa",
            "głowa mnie boli",
            "ból głowy",
            "migrena",
            "pulsuje mi w głowie",
            "pulsujący ból głowy",
            "ścisk w skroniach",
            "napięciowy ból głowy",
            "ćmiący ból głowy",
            "rozpierający ból głowy"
        ],
        "Wymioty": [
            "rzyganie",
            "zwracam treść pokarmową",
            "chce mi się wymiotować",
            "wymiotuję",
            "wymiotuje",
            "nudności z wymiotami",
            "rzucam pawia",
            "zwymiotowałem",
            "odruch wymiotny",
            "wyrzucam z siebie jedzenie",
            "mdłości z torsjami"
        ],
        "Gorączka": [
            "temperatura 38",
            "wysoka temperatura",
            "mam ponad 37 stopni",
            "mam gorączkę",
            "jestem rozpalony",
            "czuję, że mam podwyższoną temperaturę",
            "gorączkuję",
            "mam stan podgorączkowy",
            "piecze mnie skóra",
            "czuję gorąco w ciele"
        ],
        "Ból kości i stawów": [
            "łamanie w kościach",
            "stawy mnie bolą",
            "przeskakiwanie w stawach",
            "bóle reumatyczne",
            "kłujący ból w stawach",
            "sztywność stawów",
            "trzeszczenie w stawach",
            "bóle kostne",
            "ciągnie mnie w kościach",
            "ból podczas ruchu"
        ],
        "Nudności": [
            "mdłości",
            "jest mi niedobrze",
            "zbiera mi się na wymioty",
            "czuję się słabo",
            "ścisnęło mnie w żołądku",
            "żołądek mi się przewraca",
            "mam zawroty głowy i mdłości",
            "odrzuca mnie od jedzenia",
            "brzydzi mnie zapach jedzenia",
            "mdli mnie"
        ],
        "Ból brzucha": [
            "boli mnie brzuch",
            "ból w okolicy żołądka",
            "kłuje mnie w brzuchu",
            "skurcze brzucha",
            "bóle żołądkowe",
            "ciągnie mnie w żołądku",
            "czuję ucisk w brzuchu",
            "rozpierający ból w brzuchu",
            "piekący ból w żołądku",
            "ból jelitowy"
        ],
        "Kaszel": [
            "kaszlę",
            "pokasłuję",
            "mam suchy kaszel",
            "kaszel mokry",
            "drażniący kaszel",
            "krztuszę się",
            "odchrząkuję",
            "napad kaszlu",
            "kaszel odrywający",
            "kaszel duszący"
        ],
        "Duszności": [
            "ciężko mi oddychać",
            "brakuje mi tchu",
            "łapię powietrze",
            "nie mogę złapać oddechu",
            "czuję ucisk w klatce piersiowej",
            "świszczący oddech",
            "czuję się przytłoczony",
            "mam zadyszkę",
            "krótkie oddechy",
            "duszę się"
        ],
        "Zmęczenie": [
            "jestem wyczerpany",
            "brak mi energii",
            "czuję się słabo",
            "mam totalny spadek energii",
            "jestem ospały",
            "nie mam sił",
            "padam z nóg",
            "czuję się wyczerpany psychicznie",
            "jestem przemęczony",
            "czuję się bez życia"
        ],
        "Utrata wagi": [
            "schudłem",
            "chudnę ostatnio",
            "straciłem na wadze",
            "ważę mniej",
            "ubytki masy ciała",
            "spadek wagi",
            "zmniejszyłem swoją wagę",
            "widać po mnie, że schudłem",
            "zaczynam być chudy",
            "zmalała mi waga"
        ],
        "Problemy ze snem": [
            "bezsenność",
            "ciężko mi zasnąć",
            "nie mogę spać",
            "budzę się w nocy",
            "śpię niespokojnie",
            "mam płytki sen",
            "przewracam się z boku na bok",
            "nie mogę się wyspać",
            "senność w ciągu dnia",
            "jestem niewyspany"
        ],
        "Ból mięśni": [
            "mięśnie mnie bolą",
            "zakwasy",
            "ciągnie mnie w mięśniach",
            "sztywność mięśni",
            "mam ból mięśniowy",
            "nadwyrężenie mięśni",
            "skurcze mięśni",
            "piekący ból mięśni",
            "uczucie zmęczenia mięśni",
            "mięśnie mi sztywnieją"
        ],
        "Dreszcze": [
            "mam dreszcze",
            "trzęsie mnie",
            "zimno mi",
            "mam gęsią skórkę",
            "drżę z zimna",
            "czuję wewnętrzne dreszcze",
            "jest mi lodowato",
            "czuję, jakby coś mnie mroziło",
            "ciągle mi zimno",
            "mam niekontrolowane drżenie ciała"
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

    # Słownik odpowiedzi systemu
    responses = {
        "reset": [
            "Rozumiem, tak więc opisz mi jeszcze raz, co Ci dolega.",
            "W porządku. Możesz jeszcze raz opisać, co Cię trapi?",
            "Jasne, zatem co Cię konkretnie boli?",
            "Rozpoczynamy od nowa. Jak się czujesz i co Cię boli?",
            "OK, opowiedz mi ponownie, co Ci dolega.",
            "Zaczynamy od początku. Co Cię niepokoi?",
            "Powiedz mi raz jeszcze, co Ci doskwiera.",
            "Spróbujmy ponownie. Co Ci dolega?",
            "Chcę dobrze zrozumieć. Opisz jeszcze raz swoje objawy.",
            "Przejdźmy przez to od nowa. Jak się dziś czujesz?"
        ],
        "start": [
            "Dzień dobry, co Ci dolega?",
            "Hej! Co się dzieje? Jak mogę pomóc?",
            "Hej! Czy mógłbyś powiedzieć co ci dolega?",
            "Witaj! Co jest nie tak?",
            "Dzień dobry! opowiedz mi o swoich dolegliwościach",
            "Cześć! Jakie masz dziś dolegliwości?"
        ],
        "end": [
            "Do widzenia, życzę zdrowia!",
            "Trzymaj się, mam nadzieję, że czujesz się lepiej.",
            "Zdrówka, do usłyszenia!",
            "Dbaj o siebie i wracaj do zdrowia!",
            "Życzę Ci szybkiego powrotu do zdrowia!",
            "Do usłyszenia! Wszystkiego dobrego!",
            "Powodzenia, życzę dużo zdrowia!",
            "Trzymaj się ciepło, zdrowiej!",
            "Miłego dnia, dbaj o siebie!",
            "Cześć i wracaj szybko do formy!"
        ],
        "ask_first": [
            "Czy występują u Ciebie objawy takie jak {symptom}?",
            "Zastanawiam się, czy dokucza Ci coś takiego jak {symptom}?",
            "Czy zauważyłeś ostatnio, że masz coś co mogłoby sie objawiać jak {symptom}?",
            "Mógłbyś powiedzieć, czy symptom taki jak {symptom} wystąpił u ciebie ostatnio?",
            "a {symptom}?",
            "Czy zdarza Ci się doświadczać czegoś jak {symptom}?",
            "Czy może jeden z twoich objawów to {symptom}?",
        ]
    }

    # Lista skrótów
    additional_yes_no_abbreviations = {
        "t": True,
        "n": False,
        "y": True,
    }

    # Lista wyrażeń mówiąca o braku innych objawów
    no_other_symptoms_phrases = [
        "żadne inne objawy",
        "nie mam więcej objawów",
        "nic więcej mnie nie boli",
        "to wszystkie objawy",
        "to koniec objawów",
        "nie występują inne objawy",
        "to wszystko",
        "nic innego mi nie dolega",
        "to już wszystkie objawy",
        "nie mam innych dolegliwości"
    ]

    # Integracja dodatkowych skrótów
    response_yes_no_pattern.update(additional_yes_no_abbreviations)

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
        Generuje pierwszą odpowiedź po wprowadzeniu objawów przez użytkownika.

        Args:
            user_symptoms (dict): Słownik z objawami użytkownika (objaw: True/False).
            message (str): Wiadomość bazowa do uzupełnienia.

        Returns:
            str: Sformatowana odpowiedź zawierająca listę objawów.
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
        Generuje losowe pytanie o określony objaw.

        Args:
            symptom (str): Nazwa objawu.

        Returns:
            str: Losowo wybrane pytanie o dany objaw.
        """
        question_template = random.choice(SpeechLibrary.responses["ask_first"])
        return question_template.format(symptom=symptom.lower())

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
        Generuje odpowiedź zawierającą diagnozę, specjalistę i zalecenia dla zidentyfikowanej choroby.

        Args:
            disease (dict): Dane choroby.

        Returns:
            str: Diagnoza, specjalista i zalecenia.
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
        Sprawdza, czy wiadomość użytkownika wskazuje na zakończenie rozmowy.

        Args:
            message (str): Wiadomość użytkownika.

        Returns:
            bool: True, jeśli rozmowa powinna zostać zakończona; w przeciwnym razie False.
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
        return any(phrase in message.lower() for phrase in SpeechLibrary.reset_speech_phrases)

    @staticmethod
    def reset_response() -> str:
        """
        Odpowiedź po zresetowaniu rozmowy.

        Returns:
            str: Komunikat o rozpoczęciu nowej rozmowy.
        """

        return random.choice(SpeechLibrary.responses["reset"])

    @staticmethod
    def start_response() -> str:
        """
        Zwraca losowo wybraną odpowiedź przy rozpoczęciu rozmowy.
        """
        return random.choice(SpeechLibrary.responses["start"])

    @staticmethod
    def end_response() -> str:
        """
        Zwraca losowo wybraną odpowiedź przy zakończeniu rozmowy.
        """
        return random.choice(SpeechLibrary.responses["end"])

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
