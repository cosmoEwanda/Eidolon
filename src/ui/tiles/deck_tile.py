from tkinter import Frame, Button


class DeckTile(Frame):

    def __init__(self, master, name, command):
        super().__init__(master, width=70, height=70, bg="#e0e0e0", relief="raised", bd=1)

        self.pack_propagate(False)

        btn = Button(
            self,
            text=name,
            wraplength=60,
            command=command
        )
        btn.pack(fill="both", expand=True)