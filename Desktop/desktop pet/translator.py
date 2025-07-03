# translator_app.py

import tkinter as tk
from tkinter import ttk, messagebox
from googletrans import Translator

class TranslatorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Translator")
        self.master.geometry("600x600")

        self.translator = Translator()

        self.pronunciation = tk.StringVar()
        self.word_details = tk.StringVar()

        self.create_widgets()
        
    def create_widgets(self):
        ttk.Label(self.master, text="Enter text to translate:").pack(pady=5)

        self.text_input = tk.Text(self.master, height=5, width=50)
        self.text_input.pack(pady=5)

        ttk.Label(self.master, text="Source Language (e.g., 'en'):").pack(pady=5)
        self.src_lang_combobox = ttk.Combobox(self.master)
        self.src_lang_combobox.pack(pady=5)

        ttk.Label(self.master, text="Destination Language (e.g., 'zh-CN'):").pack(pady=5)
        self.dest_lang_combobox = ttk.Combobox(self.master)
        self.dest_lang_combobox.pack(pady=5)

        translate_button = ttk.Button(self.master, text="Translate", command=self.translate_text)
        translate_button.pack(pady=20)

        ttk.Label(self.master, text="Translated text:").pack(pady=5)

        self.translated_text = tk.Text(self.master, height=5, width=50, wrap=tk.WORD)
        self.translated_text.pack(pady=5)

        self.translated_text.bind("<<Selection>>", self.show_word_details)

        ttk.Label(self.master, text="Pronunciation:").pack(pady=5)

        pronunciation_label = ttk.Label(self.master, textvariable=self.pronunciation, wraplength=500, relief="solid", padding=5)
        pronunciation_label.pack(pady=5)

        ttk.Label(self.master, text="Word Details:").pack(pady=5)

        word_details_label = ttk.Label(self.master, textvariable=self.word_details, wraplength=500, relief="solid", padding=5)
        word_details_label.pack(pady=5)

        languages = ['english', 'japanese', 'chinese (simplified)', 'chinese (traditional)', 'korean', 'indonesian']
        self.src_lang_combobox['values'] = languages
        self.dest_lang_combobox['values'] = languages

        self.src_lang_combobox.set('en')
        self.dest_lang_combobox.set('zh-CN')

    def translate_text(self):
        text = self.text_input.get("1.0", tk.END).strip()
        src_language = self.src_lang_combobox.get()
        dest_language = self.dest_lang_combobox.get()

        if not text:
            messagebox.showwarning("Input Error", "Please enter text to translate.")
            return

        try:
            translation = self.translator.translate(text, src=src_language, dest=dest_language)
            self.translated_text.delete("1.0", tk.END)
            self.translated_text.insert(tk.END, translation.text)
            self.pronunciation.set(translation.pronunciation or "N/A")
        except Exception as e:
            messagebox.showerror("Translation Error", str(e))

    def show_word_details(self, event):
        try:
            selected_word = self.translated_text.get(tk.SEL_FIRST, tk.SEL_LAST).strip()
            if selected_word:
                src_language = self.src_lang_combobox.get()
                dest_language = self.dest_lang_combobox.get()
                translation = self.translator.translate(selected_word, src=dest_language, dest=src_language)
                self.word_details.set(f"Meaning: {translation.text}")
        except tk.TclError:
            pass

def main():
    root = tk.Tk()
    app = TranslatorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
