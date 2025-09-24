import tkinter as tk
from tkinter import ttk
from typing import Optional, Union


class Window:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Guibot")

        # tema più moderno
        style = ttk.Style(self.root)
        style.theme_use("clam")

        # sfondo finestra
        self.root.configure(bg="#f0f2f5")

        # stile entry
        style.configure(
            "Modern.TEntry",
            padding=6,
            relief="flat",
            borderwidth=0,
            foreground="#333",
            fieldbackground="white"
        )

        # stile button
        style.configure(
            "Modern.TButton",
            padding=(12, 6),
            relief="flat",
            background="#4a90e2",
            foreground="white",
            focusthickness=3,
            focuscolor="none"
        )
        style.map(
            "Modern.TButton",
            background=[("active", "#357ABD")]
        )

    def prompt(self, /, title: str, message: str, *, none_btn_name: str = 'Cancel', enter_btn_name: str = 'Enter') -> Union[str, None]:
        result: Optional[str] = None

        frm = ttk.Frame(self.root, padding=20)
        frm.grid(sticky="nsew")

        ttk.Label(frm, text=message, font=("Segoe UI", 11)).grid(
            row=0, column=0, sticky="w", pady=(0, 10)
        )

        entry = ttk.Entry(frm, width=40, style="Modern.TEntry", font=("Segoe UI", 11))
        entry.grid(row=1, column=0, sticky="ew", pady=(0, 15))
        entry.focus()

        def submit(event=None):
            nonlocal result
            result = entry.get()
            self.root.quit()

        def cancel():
            nonlocal result
            result = None
            self.root.quit()

        btn = ttk.Button(frm, text=none_btn_name, style="Modern.TButton", command=cancel)
        btn.grid(row=2, column=0, sticky="w")

        btn = ttk.Button(frm, text=enter_btn_name, style="Modern.TButton", command=submit)
        btn.grid(row=2, column=0, sticky="e")

        entry.bind("<Return>", submit)

        self.root.title(title)
        self.root.mainloop()

        return result


if __name__ == "__main__":
    w = Window()
    nome = w.prompt("Input", "Inserisci il tuo nome:")
    print(f"Ciao, {nome}!")
