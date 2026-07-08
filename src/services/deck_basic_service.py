from src.utils.errors import DeckNameAlreadyExistsError


class DeckBasicService:
    def __init__(self, repository):
        self._repository = repository

    def create_deck_service(self, deck):
        if self._repository.exists(deck.name):
            raise DeckNameAlreadyExistsError(deck.name)
        self._repository.save_deck(deck)

    def update_deck_service(self, deck):
        self._repository.save_deck(deck)

    def delete_deck_service(self, deck_id):
        self._repository.delete_deck(deck_id)

    def find_by_name(self, name):
        return self._repository.find_by_name(name)

    def get_all_decks_service(self):
        return self._repository.get_all_decks()
