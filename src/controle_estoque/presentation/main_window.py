import tkinter as tk
from tkinter import ttk


class MainWindow(tk.Tk):
    """Janela raiz provisória da aplicação."""

    def __init__(self) -> None:
        super().__init__()
        self.title("Controle de Estoque")
        self.minsize(760, 480)
        self._build_layout()

    def _build_layout(self) -> None:
        container = ttk.Frame(self, padding=24)
        container.pack(fill=tk.BOTH, expand=True)

        ttk.Label(container, text="Controle de Estoque", style="Title.TLabel").pack(anchor=tk.W)
        ttk.Label(
            container,
            text="A fundação da aplicação está pronta. As funcionalidades serão adicionadas nos próximos incrementos.",
            wraplength=680,
        ).pack(anchor=tk.W, pady=(12, 0))

        style = ttk.Style(self)
        style.configure("Title.TLabel", font=("Segoe UI", 16, "bold"))
