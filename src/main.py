import tkinter as tk
from tkinter import scrolledtext
from lexer import Lexer


class CompilerGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Mini Compiler")

        self.editor = scrolledtext.ScrolledText(
            self.window,
            width=80,
            height=25,
            font=("Consolas", 12)
        )
        self.editor.pack(padx=10, pady=10)

        self.compile_button = tk.Button(
            self.window,
            text="Compile",
            font=("Arial", 12, "bold"),
            command=self.compile_code
        )
        self.compile_button.pack(pady=5)

        self.console = scrolledtext.ScrolledText(
            self.window,
            width=80,
            height=10,
            font=("Consolas", 11),
            foreground="white",
            background="black"
        )
        self.console.pack(padx=10, pady=10)

        self.window.mainloop()

    def compile_code(self):
        self.console.delete("1.0", tk.END)

        code = self.editor.get("1.0", tk.END)
        lexer = Lexer(code)

        try:
            tokens = lexer.scan_all()
            self.console.insert(tk.END, "Compilation success.\n\nTokens:\n")
            for t in tokens:
                self.console.insert(tk.END, str(t) + "\n")

        except Exception as e:
            self.console.insert(tk.END, "Error during compiling process\n\n")
            self.console.insert(tk.END, str(e) + "\n")

if __name__ == "__main__":
    CompilerGUI()