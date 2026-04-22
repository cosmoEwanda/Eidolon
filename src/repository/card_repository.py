from ..domain import CardFactory, CardDefinition

class CardRepository:
    def __init__(self, storage):
        self.storage = storage

    def save_card(self, card: CardDefinition):
        """Trasforma l'oggetto in dict e lo passa allo storage."""
        # Nota: usiamo .to_dict (proprietà) o .to_dict() (metodo) in base a come lo hai definito
        self.storage.save(card.id, card.to_dict)

    def delete_card(self, cid: str):
        """Delega la rimozione fisica allo storage."""
        self.storage.delete(cid)

    def get_all_cards(self) -> list[CardDefinition]:
        """Recupera tutti i dati grezzi e li trasforma in oggetti di Dominio."""
        raw_cards = self.storage.load_all()
        return [CardFactory.from_dict(data) for data in raw_cards]

    def get_card_by_id(self, cid: str) -> CardDefinition | None:
        """Tenta il recupero di una singola carta."""
        try:
            raw_data = self.storage.get_by_id(cid)
            return CardFactory.from_dict(raw_data)
        except FileNotFoundError:
            return None

    def exists(self, cid: str) -> bool:
        """Controllo rapido di esistenza."""
        try:
            # Chiamata leggera allo storage
            self.storage.get_by_id(cid)
            return True
        except FileNotFoundError:
            return False