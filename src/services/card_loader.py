class CardLoader:
    def __init__(self, card_service, remote_storage, mapper, renderer):

        self.card_service = card_service
        self.source = remote_storage  # GoogleDriveCardStorage
        self.mapper = mapper  # CardSheetMapper
        self.renderer = renderer  # ImageRenderSync

    def sync_remote_to_local(self, art_dir):
        print("[LOADER] Inizio sincronizzazione...")

        # 1. Scarica dati grezzi dallo Sheet
        raw_data = self.source.load_raw()

        # 2. Mappa e calcola Hash (inclusi i timestamp dei file su G:)
        remote_cards = self.mapper.map(raw_data, art_dir=art_dir)

        # 3. Aggiorna il database JSON locale (veloce)
        self.card_service.sync_cards(remote_cards)

        # 4. Sincronizza le immagini (veloce, perché force=False)
        # Verranno ridisegnate SOLO le carte con hash diverso
        local_cards = self.card_service.get_all_cards_service()
        self.renderer.sync(local_cards, force=False)

        print("[LOADER] Catalogo e immagini aggiornati con successo.")

    def clean_catalog(self):
        """Svuota il catalogo locale tramite il Service."""
        cards = self.card_service.get_all_cards_service()
        for card in cards:
            self.card_service.delete_card_service(card.id)

        # Pulizia immagini
        self.renderer.sync([])
        print("Catalog removed.")

    def load_image_by_id(self, card_id):
        """Metodo di supporto per la UI (Lazy Loading)."""
        # Il renderer sa dove sono le immagini
        image_path = self.renderer.image_dir / f"{card_id}.png"

        if image_path.exists():
            return image_path

        # Se non esiste, cerchiamo la carta e renderizziamo al volo
        card = self.card_service.get_card_by_id_service(card_id)
        if card:
            self.renderer.sync([card])
            return image_path if image_path.exists() else None

        return None

    def update_image_catalog(self):
        cards = self.card_service.get_all_cards_service()
        self.renderer.sync(cards, force=True)