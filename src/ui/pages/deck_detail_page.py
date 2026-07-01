from tkinter import Frame, Button, Label, messagebox
from src.ui.frames import CardSheetMakerFrame
from src.basic_config.paths import ONLINE_DECK_DIR
from src.ui._theme import BG_PRIMARY, BG_SECONDARY, ACCENT, DANGER, SUCCESS, TEXT_PRIMARY, TEXT_SECONDARY, FONT_DEFAULT, FONT_TITLE, FONT_HEADING, FONT_SMALL, BORDER

class DeckDetailPage(Frame):

    def __init__(self, master, deck_service, card_service,
                 on_delete=None, on_edit=None,
                 on_print_preview=None):
        super().__init__(master, bg=BG_PRIMARY)

        self.deck_service = deck_service
        self.card_service = card_service

        self.on_delete = on_delete
        self.on_edit = on_edit
        self.on_print_preview = on_print_preview

        self.current_deck = None
        self.cardsheet = None
        self.description_frame = None

        self._setup_ui()

    def load(self, deck):
        """Carica i dati del mazzo e costruisce la visualizzazione delle carte."""
        self.current_deck = deck
        self.label.config(text=deck.name)
        self.description_label.config(text=deck.description)


        # Pulizia widget precedenti
        if self.cardsheet: self.cardsheet.destroy()
        if self.description_frame: self.description_frame.destroy()

        # Ricostruzione della lista carte per il CardSheetMaker
        cards_to_display = []
        for cid, qty in deck.cards.items():
            # USA IL METODO PULITO: .get_by_id()
            card = self.card_service.get_card_by_id_service(cid)
            if card:
                cards_to_display.extend([card] * qty)

        # Visualizzazione grafica (Catalogo delle carte nel mazzo)
        self.cardsheet = CardSheetMakerFrame(self, cards_to_display)
        self.cardsheet.pack(fill="both", expand=True)

        # Pannello statistiche
        self._render_stats()

    def _setup_ui(self):
        self.label = Label(self, text="Dettaglio Mazzo", bg=BG_PRIMARY, fg=TEXT_PRIMARY, font=FONT_TITLE)
        self.label.pack(pady=(12, 4))
        self.description_label = Label(self, wraplength=self.master.winfo_width()-10, justify="left", bg=BG_PRIMARY, fg=TEXT_SECONDARY, font=FONT_DEFAULT)
        self.description_label.pack(pady=(0, 10), padx=10)


        self.top_frame = Frame(self, bg=BG_PRIMARY)
        self.top_frame.pack(fill="x", padx=6)

        Button(self.top_frame, text="Anteprima stampa", command=self._preview, bg=SUCCESS, fg="white", font=FONT_DEFAULT, relief="flat", bd=0, cursor="hand2", padx=10, pady=4).pack(side="left", padx=4, pady=4)
        Button(self.top_frame, text="Elimina mazzo", command=self._delete_deck, bg=DANGER, fg="white", font=FONT_DEFAULT, relief="flat", bd=0, cursor="hand2", padx=10, pady=4).pack(side="left", padx=4, pady=4)
        Button(self.top_frame, text="Modifica mazzo", command=self._edit_deck, bg=ACCENT, fg="white", font=FONT_DEFAULT, relief="flat", bd=0, cursor="hand2", padx=10, pady=4).pack(side="left", padx=4, pady=4)
        Button(self.top_frame, text="Pubblica PDF sul drive", command=self._post_deck, bg="#6c757d", fg="white", font=FONT_DEFAULT, relief="flat", bd=0, cursor="hand2", padx=10, pady=4).pack(side="left", padx=4, pady=4)

    def _delete_deck(self):
        if not self.current_deck:
            return

        confirm = messagebox.askyesno(
            title="Conferma eliminazione",
            message=f"Eliminare definitivamente il mazzo '{self.current_deck.name}'?"
        )

        if confirm and self.on_delete:
            # NOTA: Non cancelliamo qui! 
            # Passiamo l'oggetto al container, che gestirà la cancellazione fisica 
            # tramite repo.delete() e aggiornerà la UI.
            self.on_delete(self.current_deck)

    def _preview(self):
        """
        Invia il mazzo corrente al callback di stampa definito nel container.
        """
        if self.current_deck and self.on_print_preview:
            self.on_print_preview(self.current_deck)

    def _edit_deck(self):
        """
        Notifica il container che l'utente vuole modificare il mazzo corrente.
        """
        if self.current_deck and self.on_edit:
            # Chiamiamo il callback 'on_edit' passato dal DeckWindowContainer
            self.on_edit(self.current_deck)

    def _post_deck(self):
        if self.current_deck and self.on_print_preview:
            self.on_print_preview(self.current_deck, out_path = ONLINE_DECK_DIR / f"{self.current_deck.name}.pdf")



    def _render_stats(self):
        self.description_frame = Frame(self, bg=BG_SECONDARY, relief="solid", bd=1, highlightbackground=BORDER)
        self.description_frame.pack(fill="x", pady=8, padx=6)

        stats = [
            f"Numero carte: {self.current_deck.total_cards()}",
            f"Costo mana medio: {self.current_deck.get_avg_cost()}",
            f"Potenza media: {self.current_deck.get_avg_strenght()}"
        ]

        for text in stats:
            Label(self.description_frame, text=text, bg=BG_SECONDARY, fg=TEXT_PRIMARY, font=FONT_DEFAULT).pack(side="top", padx=8, pady=2)