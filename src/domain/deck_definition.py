from . import _deck_config

class DeckDefinition:
    MAX_COMMON_CARDS = _deck_config.MAX_COMMON_CARDS
    MAX_RARE_CARDS = _deck_config.MAX_RARE_CARDS
    MAX_EPIC_CARDS = _deck_config.MAX_EPIC_CARDS
    MIN_DECK_CARDS = _deck_config.MIN_DECK_CARDS
    MAX_DECK_CARDS = _deck_config.MAX_DECK_CARDS

    def __init__(self, name : str, cards : dict [str, int] | None = None, description : str = None):
        self.name = name
        self.cards = cards or {}
        self.description = description
        self.avg_cost = {}
        self.avg_strenght = {}

    def add(self, card_id, qty = 1):
        self.cards[card_id] = self.cards.get(card_id, 0) + qty

    def remove(self, card_id, qty=1):
        if card_id in self.cards:
            self.cards[card_id] -= qty
            if self.cards[card_id] <= 0:
                del self.cards[card_id]

    def total_cards(self):
        return sum(self.cards.values())

    @property
    def to_dict(self):
        return {
            "name": self.name,
            "cards": self.cards,
            "description": self.description,
            "avg_cost": self.avg_cost,
            "avg_strenght": self.avg_strenght
        }

    def set_avg_cost(self, avg_cost, target_cost):
        self.avg_cost[target_cost] = avg_cost

    def set_avg_strenght(self, avg_strenght, target_strenght):
        self.avg_strenght[target_strenght] = avg_strenght

    def get_avg_cost(self):
        return self.avg_cost

    def get_avg_strenght(self):
        return self.avg_strenght