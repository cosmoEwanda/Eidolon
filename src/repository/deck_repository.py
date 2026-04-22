from ..domain import DeckDefinition, DeckFactory

class DeckRepository:
    def __init__(self, storage):
        self.storage = storage

    def save_deck(self, deck: DeckDefinition):
        """Passa allo storage solo l'ID (nome) e il dizionario dei dati."""
        self.storage.save(deck.name, deck.to_dict)

    def get_all_decks(self) -> list[DeckDefinition]:
        """Carica tutti i mazzi e li trasforma in oggetti di dominio."""
        raw_list = self.storage.load_all()
        return [DeckFactory.from_dict(d) for d in raw_list]

    def get_deck_by_name(self, name: str) -> DeckDefinition | None:
        """Tenta il recupero. Gestisce il caso in cui il mazzo non esista."""
        try:
            raw_data = self.storage.get_by_name(name)
            deck = DeckFactory.from_dict(raw_data)
            print(deck.to_dict)
            return deck
        except AttributeError:
            # Gestiamo l'assenza del file o del dato
            return None

    def delete_deck(self, name: str):
        """Cancella il mazzo basandosi sull'identificativo (nome)."""
        self.storage.delete(name)

    def exists(self, name: str) -> bool:
        """Metodo rapido per il Service (es. per evitare duplicati in creazione)."""
        # Se get_by_name restituisce un oggetto, allora esiste
        return self.get_deck_by_name(name) is not None