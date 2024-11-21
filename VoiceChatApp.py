from tkinter import scrolledtext
import tkinter as tk
from MedicalChat import MedicalChat

class VoiceChatApp:
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Czat Głosowy")
        self.create_widgets()
        self.medic = MedicalChat()

    def start(self):
        self.root.mainloop()


    def create_widgets(self):
        # Panel do wyświetlania czatu
        self.chat_display = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=50, height=20)
        self.chat_display.pack(padx=10, pady=10)

        # Panel do wyświetlania tekstu użytkownika
        self.user_input = tk.Entry(self.root, width=50)
        self.user_input.pack(padx=10, pady=10)

        # Przycisk do rozpoczęcia mówienia
        self.start_button = tk.Button(self.root, text="Rozpocznij Mówienie", command=self.start_speaking)
        self.start_button.pack(padx=10, pady=10)

    def start_speaking(self):
        # Logika do rozpoczęcia mówienia (do zaimplementowania)
        user_text = self.user_input.get()
        if not user_text:  # Sprawdzenie, czy pole nie jest puste
            return
        self.chat_display.insert(tk.END, f"Ty: {user_text}\n")
        self.user_input.delete(0, tk.END)
        result, message = self.medic.analyze_symptoms(user_text)
        self.chat_display.insert(tk.END, f"MedykBot: {message}\n")

