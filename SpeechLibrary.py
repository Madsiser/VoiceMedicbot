class SpeechLibrary:    

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
        "Specjalista": "Chirurg ogólny",
        "Zalecenia": "Natychmiastowa pomoc medyczna, operacja"
    },
        #Dodajcie pozostałe choroby z tabelki
    ]

    # Lista zwrotów do zakończenia rozmowy
    end_speech_phrases = [
        "koniec"
    ]

    # Listra objawów do odpytania
    required_symptoms = [
        "Ból głowy", "Wymioty", "Gorączka", "Ból kości i stawów",
        "Nudności", "Ból brzucha", "Kaszel", "Duszności",
        "Zmęczenie", "Utrata wagi", "Problemy ze snem"
    ]

    # Jakie słowa kluczowę będą rozpatrywane przy odbiorze odpowiedzi na pytanie (kolejność jest ważna, na samej górze powinny znajdowac sie najbardziej złożone kontrukcje)
    response_yes_no_pettern= {
        "tak": True,
        "występują": True,
        "mają miejsce": True,
        "nie": False,
        "nie występuje": False,
        "brak": False,
        "t": True,
        "n": False
        }
    
    # Pierwsza odpowiedź po monologu klienta
    def first_response(user_symptoms, message):
        active_symptoms = [symptom for symptom, has_symptom in user_symptoms.items() if has_symptom]
        if active_symptoms:
            symptoms_str = ", ".join(active_symptoms)
            message = f"Rozumiem. Czyli twoje objawy to: {symptoms_str}. {message}"
        else:
            message = f"Rozumiem. {message}"
        return message

    # Pierwsze pytanie o konkretny syndrom.
    def ask_first(symptom):
        return f"Czy występują u Ciebie {symptom.lower()}?"

    # Powtórne pytanie o konkretny syndrom.
    def ask_error(symptom):
        return f"Czy możesz powtórzyć bo nie zrozumiałem, występują u Ciebie {symptom.lower()}?"

    # Komunikat gdy coś sie zepsuje.
    def error():
        return "Cos poszło nie tak :("
    
    # Odpowiedź gdy namierzy chorobę
    def find_disease(disease):
        return (f"Zalecany specjalista: {disease['Specjalista']}\n"
                        f"Zalecenia: {disease['Zalecenia']}")
    
    # Odpowiedź gdy nie namierzy choroby
    def not_find_disease():
        return "Nie mogę jednoznacznie stwierdzić, co to."