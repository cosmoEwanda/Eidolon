from tkinter import Frame, Button
from src.ui._theme import BG_SECONDARY, TEXT_PRIMARY, FONT_DEFAULT, BORDER


class DeckTile(Frame):

    def __init__(self, master, name, command):
        super().__init__(master, width=80, height=80, bg=BG_SECONDARY, relief="solid", bd=1, highlightbackground=BORDER)

        self.pack_propagate(False)

        btn = Button(
            self,
            text=name,
            wraplength=60,
            command=command,
            bg=BG_SECONDARY,
            fg=TEXT_PRIMARY,
            font=FONT_DEFAULT,
            relief="flat",
            bd=0,
            cursor="hand2"
        )
        btn.pack(fill="both", expand=True)