from . import CardDefinition


class CardFactory:

    @staticmethod
    def from_input(
        id,
        name,
        orders,
        construct,
        rarity="Comune",
        ability="NULL",
        img=None,
        extra_attributes=None
    ) -> CardDefinition:

        card = CardDefinition(id=id, name=name, orders=orders, construct=construct, rarity=rarity, ability=ability,
                              img=img if img else None)

        if extra_attributes:
            for k, v in extra_attributes.items():
                card.set_attributes(k, v)

        return card

    # -------------------------

    @staticmethod
    def from_dict(data: dict) -> CardDefinition:
        core = {k: data.get(k) for k in CardDefinition.CORE_FIELDS}
        card = CardDefinition(**core)

        for key, value in data.items():
            if key not in CardDefinition.CORE_FIELDS:
                card.set_attributes(key, value)

        return card

