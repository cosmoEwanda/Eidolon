from ..domain import DeckDefinition, DeckFactory


class DeckRepository:
    def __init__(self, storage):
        self.storage = storage

    def save_deck(self, deck: DeckDefinition):
        self.storage.save(deck.to_dict)

    def get_all_decks(self) -> list[DeckDefinition]:
        raw_list = self.storage.load_all()
        return [DeckFactory.from_dict(d) for d in raw_list]

    def get_deck_by_name(self, name: str) -> DeckDefinition | None:
        try:
            raw_data = self.storage.get_by_name(name)
            if raw_data is None:
                return None
            return DeckFactory.from_dict(raw_data)
        except AttributeError:
            return None

    def find_by_name(self, name: str) -> DeckDefinition | None:
        return self.get_deck_by_name(name)

    def delete_deck(self, deck_id: str):
        self.storage.delete(deck_id)

    def exists(self, name: str) -> bool:
        return self.get_deck_by_name(name) is not None
