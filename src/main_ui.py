from tkinter import Tk, Button, messagebox
from src.basic_config.paths import JSON_DIR, DECK_DIR, IMAGES_DIR, CARD_SHEET, ORDER_SHEET, FONT_PATH, ONLINE_IMAGES_DIR
from src.render import  TextBoxRenderer, AutoFitTextBoxBuilder
from src.persistence import JsonCardStorage, JsonDeckStorage, CardSheetMapper, GoogleDriveCardStorage
from src.services import CardLoader, ImageRenderSync, CardBasicService, DeckBasicService, CardRendererService
from src.repository import CardRepository, DeckRepository
from src._setup_app import ASSETS_LIBRARY, RENDER_DICT, STYLES
from src.ui import DeckWindowContainer

from src.domain import CardDefinition, DeckDefinition

###############
rune_deck_description = "Attenzione: questo mazzo viene resettato ogni volta che chiudi e riapri l'applicazione. Il suo utilizzo è necessario al solo fine di stampare le Rune del gioco. Volendo, è possibile modificare il numero di elementi da stampare, ricordando che a ogni riavvio dell'applicazione, tale valore sarà reimpostato a 15 di default!"
###############
class MainUI(Tk):

    ICONS_LIBRARY = ASSETS_LIBRARY["Icons"]

    def __init__(self):
        super().__init__()
        self.title("Eidolon Card Maker")
        self.configure(bg="white")
        self.setup_window()
        self.state("zoomed")

        # In MainUI.__init__
        # 1. Infrastruttura
        json_card_storage = JsonCardStorage(JSON_DIR)
        json_deck_storage = JsonDeckStorage(DECK_DIR)
        self.database = GoogleDriveCardStorage(CARD_SHEET, ORDER_SHEET)

        # 2. Repository
        card_repo = CardRepository(json_card_storage)
        deck_repo = DeckRepository(json_deck_storage)


        # 3. SERVICE (Qui è dove "vivono" i tuoi nuovi file)
        self.card_service = CardBasicService(card_repo)
        self.deck_service = DeckBasicService(deck_repo)

        self.renderer = TextBoxRenderer(self.ICONS_LIBRARY)
        builder = AutoFitTextBoxBuilder(self.renderer, font_path=FONT_PATH)



        self.renderer_service = CardRendererService(
            assets_library=ASSETS_LIBRARY,
            render_dict=RENDER_DICT,  # Passiamo tutto il dizionario dei layout
            text_builder=builder,
            text_renderer=self.renderer,
            images_dir=ONLINE_IMAGES_DIR,
            default_style=STYLES
        )

        self._create_deck_runes()
        # 4. COORDINATORE (CardLoader)
        # Assicurati che l'ordine delle dipendenze sia quello giusto!
        self.loader = CardLoader(
            card_service=self.card_service,
            remote_storage=self.database,
            mapper=CardSheetMapper(),
            renderer=ImageRenderSync(IMAGES_DIR, self.renderer_service)
        )



        # 5. UI SETUP
        # Nota: command chiama sync_remote_to_local, non load_cards (che abbiamo rinominato)
        Button(self, text="Aggiorna catalogo", command=self._on_sync_click).pack(fill="x")
        Button(self, text="Cancella catalogo", command=self.loader.clean_catalog).pack(fill="x")


        # =========================
        # PAGINE DINAMICHE
        # =========================

        self.page_container = DeckWindowContainer(
            master=self,
            card_service=self.card_service,
            deck_service=self.deck_service,
            card_loader=self.loader
        )
        self.page_container.pack(fill="both", expand=True)


    def setup_window(self):

        width = 1024
        height = 512

        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()

        x = (screen_w // 2) - (width // 2)
        y = (screen_h // 2) - (height // 2)

        self.geometry(f"{width}x{height}+{x}+{y}")

    def _on_sync_click(self):
        """Metodo helper per gestire gli errori di rete nella UI."""
        try:
            self.loader.sync_remote_to_local(art_dir=ONLINE_IMAGES_DIR)
            self._create_deck_runes()
            messagebox.showinfo("Successo", "Catalogo sincronizzato con successo!")
        except ConnectionError:
            messagebox.showerror("Errore di rete", "Impossibile raggiungere Google Drive. Verifica la connessione.")
        #except Exception as e:
            #messagebox.showerror("Errore", f"Si è verificato un errore imprevisto: {e}")

    def _create_deck_runes(self):
        rune = CardDefinition(
            id="__R__",
            name="",
            construct="Runa",
            orders=[],
            rarity="",
        )
        rune.set_attributes("sinergy", "NULL")
        deck_rune = DeckDefinition(
        name="!deck_rune!",
        cards={"__R__": 15},
        description=rune_deck_description
    )

        self.card_service.save_card_service(rune)
        self.deck_service.update_deck_service(deck_rune)
        self.renderer_service.render_and_save(rune, IMAGES_DIR / "_Runa_.png")





# =========================================================
# ENTRY POINT
# =========================================================

if __name__ == "__main__":
    app = MainUI()
    app.mainloop()

