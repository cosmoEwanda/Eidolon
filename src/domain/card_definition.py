from pathlib import Path
import src.domain._card_config as _card_config

class CardDefinition:
    VALID_CONSTRUCTS = _card_config.CONSTRUCTS
    VALID_COSTS = _card_config.COSTS
    VALID_ORDERS = _card_config.ORDERS
    VALID_STATS = _card_config.STATS
    VALID_RARITY = _card_config.RARITY
    VALID_MANA = _card_config.MANA

    CORE_FIELDS = _card_config.CORE_FIELDS

    # set condiviso solo per “loggare una volta”
    _WARNED_DYNAMIC_KEYS = set()

    def __init__(self, id: str, name: str, orders: list[str], construct: str,
                 rarity: str = "Comune", ability: str = "NULL", img: Path = None):
        self.id = id
        self.name = name
        self.orders = orders
        self.construct = construct
        self.rarity = rarity
        self.ability = ability
        self.img = img if img else None

        self.global_extra_fields = {}

    def set_attributes(self, key, value, warn_new: bool = True):
        known = (key in self.__dict__) or (key in self.CORE_FIELDS) or (key in self.global_extra_fields)

        if not known:
            self.global_extra_fields[key] = value
            if warn_new and key not in self._WARNED_DYNAMIC_KEYS:
                print(f"[WARN] Nuovo attributo dinamico: {key}")
                self._WARNED_DYNAMIC_KEYS.add(key)

        setattr(self, key, value)

    def get_attributes(self, key, default=None):
        return getattr(self, key, default)

    @property
    def to_dict(self):
        data = dict(self.__dict__)
        if isinstance(data.get("img"), Path):
            data["img"] = str(data["img"])
        return data

    def __str__(self):
        return str(self.__dict__)