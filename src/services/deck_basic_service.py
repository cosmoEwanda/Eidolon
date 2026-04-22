from src.utils.errors import DeckNameAlreadyExistsError

class DeckBasicService:
    def __init__(self, repository):
        self._repository = repository

    def create_deck_service(self, deck):
        """Logica per la creazione di un nuovo mazzo."""
        # Regola di business: il nome deve essere unico
        if self._repository.exists(deck.name):
            raise DeckNameAlreadyExistsError(deck.name)

        # Altre potenziali regole: numero minimo di carte, ecc.
        self._repository.save_deck(deck)

    def update_deck_service(self, deck):
        """Logica per l'aggiornamento di un mazzo esistente."""
        # Qui non controlliamo l'esistenza perché vogliamo sovrascrivere
        self._repository.save_deck(deck)

    def delete_deck_service(self, deck_name):
        """Coordina la cancellazione."""
        self._repository.delete_deck(deck_name)

    def get_all_decks_service(self):
        return self._repository.get_all_decks()
