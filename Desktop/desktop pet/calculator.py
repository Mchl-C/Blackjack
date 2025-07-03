import tkinter as tk
import math

class Calculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculator")
        self.geometry("300x400")
        
        self.expression = ""
        self.result_var = tk.StringVar()
        self.history = []

        self.create_widgets()
        self.bind_keys()

    def create_widgets(self):
        result_frame = tk.Frame(self)
        result_frame.pack(expand=True, fill="both")

        result_label = tk.Label(result_frame, textvariable=self.result_var, anchor="e", bg="white", font=("Arial", 24))
        result_label.pack(expand=True, fill="both")

        button_frame = tk.Frame(self)
        button_frame.pack(expand=True, fill="both")

        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', '.', '=', '+',
            'sqrt', 'log', 'x^y', 'C',
        ]

        row = 0
        col = 0
        for button in buttons:
            button_action = lambda x=button: self.on_button_click(x)
            tk.Button(button_frame, text=button, command=button_action, font=("Arial", 18)).grid(row=row, column=col, sticky="nsew")
            col += 1
            if col > 3:
                col = 0
                row += 1

        for i in range(4):
            button_frame.grid_columnconfigure(i, weight=1)
            button_frame.grid_rowconfigure(i, weight=1)

        history_frame = tk.Frame(self)
        history_frame.pack(expand=True, fill="both")

        self.history_text = tk.Text(history_frame, state='disabled', height=5, font=("Arial", 12))  # Smaller height
        self.history_text.pack(expand=True, fill="both")

        # Exit button
        exit_button = tk.Button(button_frame, text='Exit', command=self.on_exit, font=("Arial", 18))
        exit_button.grid(row=row+1, column=0, columnspan=4, sticky="nsew")

    def bind_keys(self):
        for key in '0123456789+-*/.':
            self.bind(f'<Key-{key}>', self.on_key_press)
        self.bind('<Return>', self.on_key_press)
        self.bind('<BackSpace>', self.on_backspace_press)
        self.bind('<Key-c>', self.clear_expression)
        self.bind('<Key-p>', lambda event: self.on_exit())

    def on_key_press(self, event):
        if event.keysym == 'Return':
            self.on_button_click('=')
        elif event.char in '0123456789+-*/.':
            self.on_button_click(event.char)

    def on_backspace_press(self, event):
        self.expression = self.expression[:-1]
        self.result_var.set(self.expression)

    def on_button_click(self, char):
        if char == "=":
            try:
                self.expression = self.expression.replace('^', '**')
                result = str(eval(self.expression))
                self.history.append(self.expression + " = " + result)
                self.update_history()
                self.expression = result
            except Exception as e:
                self.expression = "Error"
        elif char == 'sqrt':
            try:
                result = str(math.sqrt(eval(self.expression)))
                self.history.append(f"sqrt({self.expression}) = {result}")
                self.update_history()
                self.expression = result
            except Exception as e:
                self.expression = "Error"
        elif char == 'log':
            try:
                result = str(math.log10(eval(self.expression)))
                self.history.append(f"log({self.expression}) = {result}")
                self.update_history()
                self.expression = result
            except Exception as e:
                self.expression = "Error"
        elif char == 'x^y':
            self.expression += '^'
        elif char == 'C':
            self.expression = ""
        else:
            self.expression += str(char)
        self.result_var.set(self.expression)

    def update_history(self):
        self.history_text.config(state='normal')
        self.history_text.delete(1.0, tk.END)
        for item in self.history[-4:]:  # Show last 4 history items
            self.history_text.insert(tk.END, item + "\n")
        self.history_text.config(state='disabled')

    def clear_expression(self, event=None):
        self.expression = ""
        self.result_var.set(self.expression)

    def on_exit(self):
        self.destroy()

if __name__ == "__main__":
    app = Calculator()
    app.mainloop()
