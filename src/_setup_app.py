from dataclasses import replace
from src.domain import CardDefinition
from src.basic_config.paths import CONSTRUCTS_DIR, ICONS_DIR, FONT_PATH
from src.render.types import Padding
from src.render.style import TextBoxStyle


ORDER_ICONS_DEFAULT_DIM = (62, 62)
ORDER_ICONS_VARCO_DIM = (104, 104)
STATS_DEFAULT_DIM = (90, 60)
COST_DIM = (90, 60)

COMMON_STYLE = TextBoxStyle(
    font_path=FONT_PATH,
    font_size=45,
    text_color=(0, 0, 0, 255),
    bg_color=(0,0,0,0),
    align="right",
    padding=Padding(0, 0, 0, 0)
)

STYLES = {
    "name": replace(COMMON_STYLE, font_size=60),
    "construct": replace(COMMON_STYLE, font_size=50),
    "stats": replace(COMMON_STYLE, align="center"),
    "cost" : replace(COMMON_STYLE, align="center"),
    "ability": replace(COMMON_STYLE, align="left", padding=Padding(5, 0, 0, 5)),
    "rarity": replace(COMMON_STYLE, align="center", font_size=35),
    "energy" : replace(COMMON_STYLE, align="center", font_size=50),
    "RUNA" : replace(COMMON_STYLE, text_color=(0,0,0,0)) #trasparente
}


# --- 1. ASSETS LIBRARY (Dove sono i file) ---
# Gestisce la mappatura tra i nomi logici e i file fisici
ASSETS_LIBRARY = {
    "Icons": {
        **{order: ICONS_DIR / f"{order}.png" for order in CardDefinition.VALID_ORDERS},
        **{mana: ICONS_DIR / f"{mana}.png" for mana in CardDefinition.VALID_MANA}
    },
    "Templates": {
        **{construct : CONSTRUCTS_DIR / f"{construct}.png" for construct in CardDefinition.VALID_CONSTRUCTS},
        "DEFAULT": CONSTRUCTS_DIR / "carta generica gioco.png"
    }
}

# --- 2. LAYOUT TEMPLATES (Le coordinate) ---
# Definiamo uno scheletro comune per evitare ripetizioni
def get_base_layout():
    return {
        "name_config" : {
            "style" : STYLES["name"],
            "elems" : {
                "Name" : {
                    "pos": (280, 70),
                    "dim": (590, 70)}
                }
            },
        "rarity_config" : {
            "style" : STYLES["rarity"],
            "elems" : {
                "Rarity" : {
                    "pos": (60, 930),
                    "dim": (180, 90)}
                }
            },
        "ability_config" : {
            "style": STYLES["ability"],
            "elems" : {
                "Ability" : {
                    "pos": (65, 1000),
                    "dim": (805, 210)}
                }
            },
        "construct_config": {
            "style" : STYLES["construct"],
            "elems" : {
                "Construct" : {
                    "pos": (280, 180),
                    "dim": (590, 70)}
                }
            },
        "stats_config" : {
            "style": STYLES["stats"],
            "elems": {
                CardDefinition.VALID_STATS[0]: {  # Energia
                    "pos": (153, 34),
                    "dim": STATS_DEFAULT_DIM},
                CardDefinition.VALID_STATS[1]: {  # Forza
                    "pos": (355, 1235),
                    "dim": STATS_DEFAULT_DIM},
                CardDefinition.VALID_STATS[2]: {  # Tenacia
                    "pos": (560, 1235),
                    "dim": STATS_DEFAULT_DIM},
                CardDefinition.VALID_STATS[3]: {  # Astuzia
                    "pos": (755, 1235),
                    "dim": STATS_DEFAULT_DIM}
                },

        },
        "cost_config": {
            "style": STYLES["cost"],
            "elems": {
                CardDefinition.VALID_COSTS[0]: {
                    "pos": (140, 70),
                    "dim": COST_DIM},
                CardDefinition.VALID_COSTS[1]: {
                    "pos": (155, 175),
                    "dim": COST_DIM},
                CardDefinition.VALID_COSTS[2]: {
                    "pos": (150, 1235),
                    "dim": COST_DIM},
            }
        },
        "orders_config": {
            "style": None,
            "elems": {
                CardDefinition.VALID_ORDERS[0] : {
                    "pos": (60, 313),
                    "dim": ORDER_ICONS_DEFAULT_DIM},
                CardDefinition.VALID_ORDERS[1] : {
                    "pos": (60, 407),
                    "dim": ORDER_ICONS_DEFAULT_DIM},
                CardDefinition.VALID_ORDERS[2]: {
                    "pos": (60, 501),
                    "dim": ORDER_ICONS_DEFAULT_DIM},
                CardDefinition.VALID_ORDERS[3]: {
                    "pos": (60, 595),
                    "dim": ORDER_ICONS_DEFAULT_DIM},
                CardDefinition.VALID_ORDERS[4]: {
                    "pos": (60, 690),
                    "dim": ORDER_ICONS_DEFAULT_DIM},
                CardDefinition.VALID_ORDERS[5]: {
                    "pos": (60, 786),
                    "dim": ORDER_ICONS_DEFAULT_DIM}}
            },
        "art_config" : {
            "style": None,
            "elems": {
                "art" : {
                    "pos" : (239, 335),
                    "dim" : (600, 570)
                }
            }
        }

    }

RENDER_DICT = {}

# --- POPOLAMENTO RENDER_DICT ---
for i, construct in enumerate(CardDefinition.VALID_CONSTRUCTS):
        RENDER_DICT[construct] = get_base_layout()



#posizionamento specifico degli ordini in Varco
RENDER_DICT["Varco"]["orders_config"]["elems"] = {
            CardDefinition.VALID_ORDERS[0] : {
                "pos": (200, 330),
                "dim": ORDER_ICONS_VARCO_DIM},
            CardDefinition.VALID_ORDERS[1] : {
                "pos": (106, 472),
                "dim": ORDER_ICONS_VARCO_DIM},
            CardDefinition.VALID_ORDERS[2]: {
                "pos": (87, 629),
                "dim": ORDER_ICONS_VARCO_DIM},
            CardDefinition.VALID_ORDERS[3]: {
                "pos": (640, 330),
                "dim": ORDER_ICONS_VARCO_DIM},
            CardDefinition.VALID_ORDERS[4]: {
                "pos": (734, 472),
                "dim": ORDER_ICONS_VARCO_DIM},
            CardDefinition.VALID_ORDERS[5]: {
                "pos": (754, 629),
                "dim": ORDER_ICONS_VARCO_DIM}
            }
RENDER_DICT["Varco"]["name_config"]["elems"] = {
    "Name" : {
        "pos" : (110, 85),
        "dim" : (720, 80)
    }
}

RENDER_DICT["Varco"]["construct_config"]["elems"] = {
    "Construct" : {
        "pos" : (110, 200),
        "dim" : (720, 80)
    }
}

RENDER_DICT["Varco"]["rarity_config"]["elems"] = {
    "Rarity" : {
        "pos" : (115, 845),
        "dim" : (130, 80)
    }
}

RENDER_DICT["Varco"]["ability_config"]["elems"] = {
    "Ability" : {
        "pos" : (120, 930),
        "dim" : (720, 225)
    }
}

RENDER_DICT["Varco"]["stats_config"] = {
    "style" : STYLES["energy"],
    "elems": {
        CardDefinition.VALID_STATS[0] : {
            "pos" : (440, 1225),
            "dim" : STATS_DEFAULT_DIM
    }}
}

RENDER_DICT["Varco"]["art_config"]["elems"] = {
        "art" : {
            "pos" : (230, 352),
            "dim" : (480, 478)
        }
}

RENDER_DICT["Runa"] = get_base_layout()
RENDER_DICT["Runa"]["construct_config"]["style"] = STYLES["RUNA"]



if __name__ == "__main__":
    print(RENDER_DICT)