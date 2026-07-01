from tkinter import Toplevel, Label
from PIL import Image, ImageTk
from src.ui._theme import BG_PRIMARY, TEXT_SECONDARY, FONT_SMALL


class CardImageWindow(Toplevel):
    def __init__(self, master, cid):
        super().__init__(master, bg=BG_PRIMARY)

        self.title(f"Visualizzatore: {cid}")
        self.geometry("400x650")

        # Caricamento e resize immagine
        img = Image.open(cid)
        original_dims = img.size
        img = img.resize((350, 500))
        new_dims = img.size
        self.ratio_x = original_dims[0] / new_dims[0]
        self.ratio_y = original_dims[1] / new_dims[1]

        self.photo = ImageTk.PhotoImage(img)

        # Creazione della Label per l'immagine
        self.image_label = Label(self, image=self.photo, bg=BG_PRIMARY)
        self.image_label.pack(padx=10, pady=10)

        # Label di stato per visualizzare le coordinate
        self.coords_label = Label(self, text="Muovi il mouse sull'immagine", bg=BG_PRIMARY, fg=TEXT_SECONDARY, font=FONT_SMALL)
        self.coords_label.pack(pady=5)

        # --- BINDING DELL'EVENTO ---
        # Colleghiamo il movimento del mouse sulla Label dell'immagine
        self.image_label.bind("<Motion>", self._on_mouse_move)

    def _on_mouse_move(self, event):
        """
        Gestore dell'evento movimento mouse con proiezione sulle coordinate reali.
        """
        # 1. Coordinate locali (sulla Label 350x500)
        view_x, view_y = event.x, event.y

        # 2. Proiezione sulle coordinate originali (es. 1500x2100)
        # Usiamo int() perché le coordinate del layout sono pixel interi
        real_x = int(view_x * self.ratio_x)
        real_y = int(view_y * self.ratio_y)

        # 3. Aggiorna la label visualizzando entrambi i valori per debug
        self.coords_label.config(
            text=f"Mouse: ({view_x}, {view_y}) | Layout: ({real_x}, {real_y})"
        )

        # Se vuoi testare il posizionamento degli oggetti:
        # self._debug_check_layout(real_x, real_y)