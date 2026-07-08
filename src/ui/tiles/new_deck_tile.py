from tkinter import Button, Frame
from src.ui._theme import SUCCESS, SUCCESS_LIGHT, TEXT_PRIMARY, FONT_DEFAULT


class NewDeckTile(Frame):

    def __init__(self, master, command):
        super().__init__(master, width=80, height=80, bg=SUCCESS_LIGHT, relief="solid", bd=1)

        self.pack_propagate(False)

        btn = Button(
            self,
            text="+\nNuovo",
            command=command,
            bg=SUCCESS,
            fg="white",
            font=FONT_DEFAULT,
            relief="flat",
            bd=0,
            cursor="hand2"
        )
        btn.pack(fill="both", expand=True)