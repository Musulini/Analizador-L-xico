import tkinter as tk
from tkinter import scrolledtext
from lexer import Lexer


class CompilerGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Mini Compiler")
        self.window.geometry("900x600")
        self.window.configure(bg="#1e1e1e")

        # ======= TOP BAR =======
        top_frame = tk.Frame(self.window, bg="#1e1e1e")
        top_frame.pack(fill="x", padx=10, pady=5)

        self.compile_button = tk.Button(
            top_frame,
            text="▶",
            font=("Arial", 14, "bold"),
            bg="#0e639c",
            fg="white",
            activebackground="#1177bb",
            activeforeground="white",
            bd=0,
            padx=15,
            pady=5,
            command=self.compile_code
        )
        self.compile_button.pack(side="right")

        # ======= PANED WINDOW (Editor + Console) =======
        self.paned = tk.PanedWindow(
            self.window,
            orient=tk.VERTICAL,
            sashwidth=6,
            bg="#1e1e1e"
        )
        self.paned.pack(fill="both", expand=True, padx=10, pady=5)

        # ======= EDITOR FRAME =======
        editor_frame = tk.Frame(self.paned, bg="#1e1e1e")

        # Line numbers
        self.line_numbers = tk.Text(
            editor_frame,
            width=4,
            padx=5,
            takefocus=0,
            border=0,
            background="#252526",
            foreground="#858585",
            state="disabled",
            font=("Consolas", 12)
        )
        self.line_numbers.pack(side="left", fill="y")

        # Code editor
        self.editor = tk.Text(
            editor_frame,
            wrap="none",
            font=("Consolas", 12),
            background="#1e1e1e",
            foreground="#d4d4d4",
            insertbackground="white",
            border=0
        )
        self.editor.pack(side="left", fill="both", expand=True)

        # Scrollbar
        scroll = tk.Scrollbar(editor_frame, command=self._on_scroll)
        scroll.pack(side="right", fill="y")
        self.editor.config(yscrollcommand=scroll.set)

        self.editor.bind("<KeyRelease>", self._update_line_numbers)
        self.editor.bind("<MouseWheel>", self._update_line_numbers)

        self.paned.add(editor_frame)

        # ======= CONSOLE FRAME =======
        console_frame = tk.Frame(self.paned, bg="#111111")

        self.console = scrolledtext.ScrolledText(
            console_frame,
            font=("Consolas", 11),
            foreground="#d4d4d4",
            background="#111111",
            insertbackground="white",
            border=0
        )
        self.console.pack(fill="both", expand=True)

        self.paned.add(console_frame)

        self._update_line_numbers()
        self.window.mainloop()

    # ===============================
    # Line numbers
    # ===============================
    def _update_line_numbers(self, event=None):
        self.line_numbers.config(state="normal")
        self.line_numbers.delete("1.0", tk.END)

        line_count = int(self.editor.index("end-1c").split(".")[0])
        for i in range(1, line_count + 1):
            self.line_numbers.insert(tk.END, f"{i}\n")

        self.line_numbers.config(state="disabled")

    def _on_scroll(self, *args):
        self.editor.yview(*args)
        self.line_numbers.yview(*args)

    # ===============================
    # Compile
    # ===============================
    def compile_code(self):
        self.console.config(state="normal")
        self.console.delete("1.0", tk.END)

        code = self.editor.get("1.0", tk.END)
        lexer = Lexer(code)

        self.console.tag_config('warning', foreground="red")
        self.console.tag_config('success', foreground="green")

        tokens, symbols, errors = lexer.scan_all()
        self.console.insert(tk.END, "Compilation success.\n\nResult:\n", 'success')


        self.console.insert(tk.END, "-"*7)
        self.console.insert(tk.END, "TABLA DE TOKENS")
        self.console.insert(tk.END, "-"*8+"\n")
        for t in tokens:
            self.console.insert(tk.END, "-"*30)
            self.console.insert(tk.END, f'\n{t}\n')
        self.console.insert(tk.END, "-"*30+"\n")

        self.console.insert(tk.END, "-"*6)
        self.console.insert(tk.END, "TABLA DE SIMBOLOS")
        self.console.insert(tk.END, "-"*7+"\n")
        for e in symbols:
            self.console.insert(tk.END, "-"*30)
            self.console.insert(tk.END, f'\n{e}\n')
        self.console.insert(tk.END, "-"*30+"\n")

        self.console.insert(tk.END, "-"*11)
        self.console.insert(tk.END, "Errores")
        self.console.insert(tk.END, "-"*12+"\n")
        for e in errors:
            self.console.insert(tk.END, "-"*30)
            self.console.insert(tk.END, f'\n{e}\n')
        self.console.insert(tk.END, "-"*30)

        self.console.config(state="disabled")


if __name__ == "__main__":
    CompilerGUI()
