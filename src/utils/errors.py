class DeckNameAlreadyExistsError(Exception):
    def __init__(self, name: str):
        super().__init__(f"Deck name already exists: {name}")
        self.name = name