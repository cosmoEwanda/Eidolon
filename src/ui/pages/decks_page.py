from tkinter import Frame

from src.ui.tiles import DeckTile, NewDeckTile


class DecksPage(Frame):

    TILE_SIZE = 70
    MAX_N_DECKS = 35

    def __init__(self, master, deck_service, open_callback, new_callback):
        super().__init__(master)

        self.deck_service = deck_service # Il Repository (non lo Storage!)
        self.open_callback = open_callback
        self.new_callback = new_callback

        # Container centrale per le tile
        self.container = Frame(self)
        self.container.pack(padx=20, pady=20)

        self.load_decks()

    def load_decks(self):
        """Recupera i mazzi e costruisce la griglia di Tile."""
        # Chiamata al metodo pulito del Repository
        decks = self.deck_service.get_all_decks_service()

        col = 0
        row = 0

        for i, deck in enumerate(decks):
            # Creiamo la tile per il mazzo esistente
            if i >= self.MAX_N_DECKS:
                break

            tile = DeckTile(
                self.container,
                deck.name,
                # Passiamo l'oggetto deck completo al callback
                lambda d=deck: self.open_callback(d)
            )
            tile.grid(row=row, column=col, padx=10, pady=10)

            col += 1
            if col == 6:
                col = 0
                row += 1

        # Tile per la creazione di un nuovo mazzo (sempre in ultima posizione)
        new_tile = NewDeckTile(self.container, self.new_callback)
        new_tile.grid(row=row, column=col, padx=10, pady=10)

    def reload(self):
        """Pulisce la UI e ricarica i dati dal Repository."""
        for widget in self.container.winfo_children():
            widget.destroy()

        self.load_decks()