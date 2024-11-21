from tkinter import scrolledtext
import tkinter as tk
from MedicalChat import MedicalChat

class VoiceChatApp:
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Czat Głosowy")
        self.create_widgets()
        self.medic = MedicalChat()
        self.user_input = ""

    def start(self):
        self.root.mainloop()


    def create_widgets(self):
        # Panel do wyświetlania czatu
        self.chat_display = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=50, height=20)
        self.chat_display.pack(padx=10, pady=10)

        # Panel do wyświetlania tekstu użytkownika
        # self.user_input = tk.Entry(self.root, width=50)
        # self.user_input.pack(padx=10, pady=10)
        

        # Panel do wyświetlania głosu użytkownika
        self.user_input_voice = tk.Label(self.root, width=50, text="pusto")
        self.user_input_voice.pack(padx=10, pady=10)
        self.user_input_voice

        # Przycisk do rozpoczęcia mówienia
        self.start_button = tk.Button(self.root, text="Rozpocznij Mówienie", command=self.start_speaking_button)
        self.start_button.pack(padx=10, pady=10)

        # Przycisk do potwierdzenia co powiedziane
        self.start_button = tk.Button(self.root, text="Potwierdź", command=self.process_text)
        self.start_button.pack(padx=10, pady=10)


    def start_speaking_button(self):
        # Logika do rozpoczęcia mówienia (do zaimplementowania)
        

        pass
        
        
    # Przetwarzanie tekstu i wyswietlanie
    def process_text(self):
        user_text = self.user_input
        if not user_text:  # Sprawdzenie, czy pole nie jest puste
            return
        self.chat_display.insert(tk.END, f"Ty: {user_text}\n")
        result, message = self.medic.analyze_symptoms(user_text)
        self.chat_display.insert(tk.END, f"MedykBot: {message}\n")
        self.user_input_voice.config(text="dziala")

