from tkinter import Frame, Button, messagebox
from src.services import DeckPrintService, PdfInUseError
from src.ui.pages import DeckBuilderPage, DeckDetailPage, DecksPage
from src.utils.errors import DeckNameAlreadyExistsError


class DeckWindowContainer(Frame):

    def __init__(self, master, card_service, deck_service, card_loader):
        super().__init__(master)
        self.pack(fill="both", expand=True)

        self.card_service = card_service
        self.deck_service = deck_service
        self.card_loader = card_loader

        self.pages = {}
        self.current_page = None

        self.print_service = DeckPrintService(image_provider=self.card_loader)

        # Solo pagina base subito
        self.pages["decks"] = DecksPage(self, self.deck_service, self.open_deck, self.new_deck)


        self.show("decks")

        self.bottom_frame = Frame(self)
        self.bottom_frame.pack(side="bottom", fill="both")
        Button(self.bottom_frame, text="Home", command= lambda : self.show("decks")).pack(side="left")

    # -------------------------------------------------

    def show(self, name):
        if self.current_page:
            self.current_page.pack_forget()

        self.current_page = self.pages[name]
        self.current_page.pack(fill="both", expand=True)


    # -------------------------------------------------

    def open_deck(self, deck):

        if "deck_detail" not in self.pages:
            self.pages["deck_detail"] = DeckDetailPage(self, self.deck_service, self.card_service,
                                                       on_delete=self._after_delete_deck, on_edit=self._edit_deck,
                                                       on_print_preview=self._print_preview_deck)

        self.pages["deck_detail"].load(deck)
        self.show("deck_detail")

    # -------------------------------------------------

    def new_deck(self):

        self.pages["deck_builder"] = DeckBuilderPage(
            self, card_service=self.card_service,
            card_loader=self.card_loader,
            on_save=self._save_new_deck
        )

        self.show("deck_builder")

    # ---------------------

    def _save_new_deck(self, deck):
        """Logica per la CREAZIONE di un nuovo mazzo."""

        try:
            self.deck_service.create_deck_service(deck)
            self.pages["decks"].reload()
            self.show("decks")

        except DeckNameAlreadyExistsError:
            messagebox.showerror(
                "Nome già usato",
                f"Esiste già un deck con nome '{deck.name}'. Scegli un nome diverso."
            )
            return

    def _after_delete_deck(self, deck):
        """Cancellazione basata solo sul nome (ID)."""
        # Il repository ora accetta il nome, non l'oggetto intero
        self.deck_service.delete_deck_service(deck.name)
        self.pages["decks"].reload()
        self.show("decks")

    def _edit_deck(self, deck):

        self.pages["deck_builder"] = DeckBuilderPage(
            self,
            card_service=self.card_service,
            card_loader=self.card_loader,
            on_save=self._save_edited_deck,
            deck_name=deck.name
        )

        self.pages["deck_builder"].load_existing(deck)
        self.show("deck_builder")

    def _save_edited_deck(self, deck):
        """Logica per l'AGGIORNAMENTO di un mazzo esistente."""
        # Qui sovrascriviamo senza controllare l'esistenza perché è un edit
        self.deck_service.update_deck_service(deck)
        self.pages["decks"].reload()
        self.show("decks")

    def _print_preview_deck(self, deck, out_path = None):
        try:
            pdf = self.print_service.build_pdf_for_deck(deck, output_path=out_path)
            self.print_service.preview(pdf)
        except PdfInUseError:
            messagebox.showwarning(
                "PDF già aperto",
                "Chiudi il PDF aperto nel visualizzatore e riprova."
            )
        except Exception as e:
            messagebox.showerror("Errore", f"Impossibile creare il PDF:\n{e}")