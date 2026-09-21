CORE_FIELDS = {
        "id",
        "name",
        "orders",
        "construct",
        "rarity",
        "ability",
        "img",
    }

CONSTRUCTS = [
    "Incarnato - Frammento di Guardiano",
    "Incarnato - Frammento di Sentinella",
    "Incarnato - Guardiano",
    "Incarnato - Sentinella",
    "Mistica - Alchemisi",
    "Mistica - Alchemisi Rapida",
    "Mistica - Alchemisi Rituale",
    "Mistica - Aura",
    "Mistica - Sempiterna",
    "Mistica - Sigillo",
    "Varco",
    "Runa"
]

ORDERS = [
    "Generazione",
    "Morte",
    "Forza",
    "Tenacia",
    "Incantamento",
    "Rinascita"
]

STATS = [
    "E",
    "F",
    "T",
    "A"
]

RARITY = ["Comune", "Raro", "Epico"]

PAYABLE_RESOURCES = ["Gemme", "Rune"]
SPECIAL_MANA = ["Attivazione"]

MANA = PAYABLE_RESOURCES + SPECIAL_MANA

COST_GROUPS = {
    "G": "top",
    "R": "bottom",
}

COST_DEFINITIONS = {
    f"{res}{suffix}": {"mana": res, "group": group}
    for group, suffix in [("top", "G"), ("bottom", "R")]
    for res in PAYABLE_RESOURCES
}

# Se nel resto del codice (validatori, parser, ecc.) serve ancora una lista di stringhe:
COSTS = list(COST_DEFINITIONS.keys())
TOP_COST_KEYS = [k for k, v in COST_DEFINITIONS.items() if v["group"] == "top"]
BOTTOM_COST_KEYS = [k for k, v in COST_DEFINITIONS.items() if v["group"] == "bottom"]