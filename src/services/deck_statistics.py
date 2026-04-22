class DeckStatistics:
    def __init__(self, deck, card_service):
        self.deck = deck
        self.card_service = card_service

        self.cards = {
            self.card_service.get_card_by_id_service(card): qty
            for card, qty in self.deck.cards.items()
        }
        self.total_cards = self.deck.total_cards()

    def calculate_avg_cost(self, target_cost: str):
        total_cost = 0.0
        n_cards = 0

        for card, qty in self.cards.items():
            cost = card.to_dict.get("cost")
            if not cost:
                continue

            target = cost.get(target_cost)
            if target is None:
                continue

            try:
                total_cost += float(target) * qty
                n_cards += qty
            except (ValueError, TypeError):
                continue

        avg_cost = total_cost / n_cards if n_cards != 0 else 0

        self.deck.set_avg_cost(avg_cost, target_cost)

    def calculate_avg_strenght(self, target_strenght: str):
        total_strenght = 0.0
        n_cards = 0

        for card, qty in self.cards.items():
            strenght = card.to_dict.get("stats")
            if not strenght:
                continue

            target = strenght.get(target_strenght)
            if target is None:
                continue

            try:
                total_strenght += float(target) * qty
                n_cards += qty
            except (ValueError, TypeError):
                continue

        avg_strenght = total_strenght / n_cards if n_cards != 0 else 0
        self.deck.set_avg_strenght(avg_strenght, target_strenght)

    def get_Ncards(self):
        return self.total_cards

