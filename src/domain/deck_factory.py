from . import DeckDefinition

class DeckFactory:
    @staticmethod
    def from_dict(data: dict) -> DeckDefinition:
        deck = DeckDefinition(
            name=data.get("name"),
            cards=data.get("cards", {}),
            description=data.get("description","")
        )
        deck.avg_cost = data.get("avg_cost", {})
        deck.avg_strenght = data.get("avg_strenght", {})
        return deck