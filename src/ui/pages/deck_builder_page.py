from tkinter import Frame, messagebox

from src.domain import CardDefinition, DeckDefinition
from src.ui.frames import CardCatalogFrame, DeckListFrame, CardImageWindow
from src.services import DeckStatistics


class DeckBuilderPage(Frame):

    def __init__(self, master, card_service, card_loader, on_save, deck_name="Nuovo Mazzo"):
        super().__init__(master)

        self.card_service = card_service  # CardRepository
        self.card_loader = card_loader  # CardLoader (Service)
        self.on_save = on_save

        # Inizializziamo un mazzo vuoto
        self.deck = DeckDefinition(deck_name)

        # USA IL METODO PULITO: .get_all()
        self.cards = self.card_service.get_all_cards_service()

        # ---------- UI SETUP ----------
        self._setup_ui()

    def _setup_ui(self):
        main = Frame(self)
        main.pack(fill="both", expand=True)

        self.right = Frame(main, width=250)
        self.right.pack(side="right", fill="y")
        self.right.pack_propagate(False)  # IMPORTANTISSIMO

        self.left = Frame(main)
        self.left.pack(side="left", fill="both", expand=True)

        # Catalogo: passa la lista di oggetti CardDefinition
        self.catalog = CardCatalogFrame(
            self.left,
            self.cards,
            on_card_double_click=self.add_card,
            on_view_card=self._open_card_view,
            on_reload_selected=self._reload_selected_art
        )
        self.catalog.pack(fill="both", expand=True)

        # Deck UI
        self.deck_ui = DeckListFrame(self.right, self.deck, self.save_deck)
        self.deck_ui.pack(fill="both", expand=True)

    def add_card(self, card_id):

        self.deck.add(card_id)
        self.deck_ui.refresh()

    def load_existing(self, deck):
        self.deck = deck
        self.deck_ui.deck = deck
        self.deck_ui.refresh()

    def save_deck(self):
        name = self.deck_ui.deck_name().strip()
        cards_map = self.deck_ui.selected_cards()

        if not name:
            messagebox.showerror("Errore", "Il mazzo deve avere un nome")
            return

        if not cards_map:
            messagebox.showerror("Errore", "Impossibile salvare un mazzo vuoto")
            return

        new_deck = DeckDefinition(name=name, cards=cards_map) #aggiungere descrizione

        stats_engine = DeckStatistics(new_deck, self.card_service)


        for cost in CardDefinition.VALID_COSTS:
            stats_engine.calculate_avg_cost(cost)
        for stat in CardDefinition.VALID_STATS:
            stats_engine.calculate_avg_strenght(stat)

        # Passiamo il mazzo al callback on_save (che nel container chiamerà repo.save)
        self.on_save(new_deck)

    def _open_card_view(self, card_id):
        # Il CardLoader gestisce già il path e l'eventuale rendering lazy
        img_path = self.card_loader.load_image_by_id(card_id)
        if img_path:
            CardImageWindow(self, img_path)
        else:
            messagebox.showwarning("Immagine mancante", f"Impossibile trovare l'immagine per {card_id}")

    def _reload_selected_art(self, ids: list[str]):
        # Recupera le card dal service e forza il render
        cards = []
        for cid in ids:
            c = self.card_service.get_card_by_id_service(cid)
            if c:
                cards.append(c)

        if not cards:
            messagebox.showwarning("Nessuna carta", "Nessuna carta valida selezionata per la ricarica.")
            return

        try:
            self.card_loader.renderer.sync(cards, force=True)
            messagebox.showinfo("Completato", f"Ricaricate {len(cards)} art.")
            # opzionale: pulisci le marcature
            if hasattr(self.catalog.sheet, "clear_reload_marks"):
                self.catalog.sheet.clear_reload_marks()
        except Exception as e:
            messagebox.showerror("Errore", f"Errore durante la ricarica art:\n{e}")