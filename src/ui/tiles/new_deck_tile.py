from tkinter import Button, Frame


class NewDeckTile(Frame):

    def __init__(self, master, command):
        super().__init__(master, width=70, height=70, bg="#c8f7c5", relief="ridge", bd=2)

        self.pack_propagate(False)

        btn = Button(
            self,
            text="+\nNuovo",
            command=command,
            bg="#a8e6a1"
        )
        btn.pack(fill="both", expand=True)