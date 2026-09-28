from dataclasses import replace
from src.domain import CardDefinition
from src.basic_config.paths import CONSTRUCTS_DIR, ICONS_DIR, FONT_PATH
from src.render.types import Padding
from src.render.style import TextBoxStyle


ORDER_ICONS_DEFAULT_DIM = (80, 80)
STATS_DEFAULT_DIM = (90, 60)
COST_DIM = (90, 60)

COMMON_STYLE = TextBoxStyle(
    font_path=FONT_PATH,
    font_size=45,
    text_color=(0, 0, 0, 255),
    bg_color=(125,125,125,0),
    align="right",
    padding=Padding(0, 0, 0, 0)
)

STYLES = {
    "name": replace(COMMON_STYLE, font_size=55),
    "construct": replace(COMMON_STYLE, font_size=50),
    "sinergy": replace(COMMON_STYLE, font_size=50, align="center"),
    "stats": replace(COMMON_STYLE, align="center"),
    "cost" : replace(COMMON_STYLE, align="left", font_size=53),
    "ability": replace(COMMON_STYLE, align="left", padding=Padding(5, 0, 0, 5)),
    "rarity": replace(COMMON_STYLE, align="center", font_size=35),
    "energy" : replace(COMMON_STYLE, align="center", font_size=120),
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
                    "pos": (300, 30),
                    "dim": (530, 95)}
                }
            },
        "rarity_config" : {
            "style" : STYLES["rarity"],
            "elems" : {
                "Rarity" : {
                    "pos": (120, 145),
                    "dim": (150, 90)}
                }
            },
        "ability_config" : {
            "style": STYLES["ability"],
            "elems" : {
                "Ability" : {
                    "pos": (40, 1000),
                    "dim": (850, 270)}
                }
            },
        "construct_config": {
            "style" : STYLES["construct"],
            "elems" : {
                "Construct" : {
                    "pos": (300, 140),
                    "dim": (500, 70)}
                }
            },
        "sinergy_config": {
            "style" : STYLES["sinergy"],
            "elems" : {
                "Sinergy" : {
                    "pos": (130, 920),
                    "dim": (675, 90)
                }
            }
        },
        "stats_config" : {
            "style": STYLES["stats"],
            "elems": {
                CardDefinition.VALID_STATS[0]: {  # Energia
                    "pos": (153, 34),
                    "dim": STATS_DEFAULT_DIM},
                CardDefinition.VALID_STATS[1]: {  # Forza
                    "pos": (675, 1310),
                    "dim": STATS_DEFAULT_DIM},
                CardDefinition.VALID_STATS[2]: {  # Tenacia
                    "pos": (750, 1310),
                    "dim": STATS_DEFAULT_DIM},
                CardDefinition.VALID_STATS[3]: {  # Astuzia
                    "pos": (480, 1310),
                    "dim": STATS_DEFAULT_DIM}
                },

        },
        "cost_config": {
            "style": STYLES["cost"],
            "elems": {
                "top_cost": {
                    "pos": (90, 35),
                    "dim": (210, 80)},
                "bottom_cost": {
                    "pos": (40, 1315),
                    "dim": (200, 60)},
            }
        },
        "orders_config1": {
            "style": None,
            "elems": {
                CardDefinition.VALID_ORDERS[0] : {
                    "pos": (17, 295),
                    "dim": ORDER_ICONS_DEFAULT_DIM},
                CardDefinition.VALID_ORDERS[1] : {
                    "pos": (19, 395),
                    "dim": ORDER_ICONS_DEFAULT_DIM},
                CardDefinition.VALID_ORDERS[2]: {
                    "pos": (19, 495),
                    "dim": ORDER_ICONS_DEFAULT_DIM},
                CardDefinition.VALID_ORDERS[3]: {
                    "pos": (19, 595),
                    "dim": ORDER_ICONS_DEFAULT_DIM},
                CardDefinition.VALID_ORDERS[4]: {
                    "pos": (19, 693),
                    "dim": ORDER_ICONS_DEFAULT_DIM},
                CardDefinition.VALID_ORDERS[5]: {
                    "pos": (19, 791),
                    "dim": ORDER_ICONS_DEFAULT_DIM}}
            },
        "orders_config2": {
            "style": None,
            "elems": {
                CardDefinition.VALID_ORDERS[0] : {
                    "pos": (833, 300),
                    "dim": ORDER_ICONS_DEFAULT_DIM},
                CardDefinition.VALID_ORDERS[1] : {
                    "pos": (835, 400),
                    "dim": ORDER_ICONS_DEFAULT_DIM},
                CardDefinition.VALID_ORDERS[2]: {
                    "pos": (835, 500),
                    "dim": ORDER_ICONS_DEFAULT_DIM},
                CardDefinition.VALID_ORDERS[3]: {
                    "pos": (835, 600),
                    "dim": ORDER_ICONS_DEFAULT_DIM},
                CardDefinition.VALID_ORDERS[4]: {
                    "pos": (835, 700),
                    "dim": ORDER_ICONS_DEFAULT_DIM},
                CardDefinition.VALID_ORDERS[5]: {
                    "pos": (835, 798),
                    "dim": ORDER_ICONS_DEFAULT_DIM}}
            },
        "art_config" : {
            "style": None,
            "elems": {
                "art" : {
                    "pos" : (140, 235),
                    "dim" : (650, 650)
                }
            }
        }

    }

RENDER_DICT = {}

# --- POPOLAMENTO RENDER_DICT ---
for i, construct in enumerate(CardDefinition.VALID_CONSTRUCTS):
        RENDER_DICT[construct] = get_base_layout()

RENDER_DICT["Varco"]["ability_config"]["elems"] = {
    "Ability" : {
        "pos" : (40, 950),
        "dim" : (850, 325)
    }
}

RENDER_DICT["Varco"]["stats_config"] = {
    "style" : STYLES["energy"],
    "elems": {
        CardDefinition.VALID_STATS[0] : {
            "pos" : (410, 1290),
            "dim" : (120, 100)
    }}
}

RENDER_DICT["Runa"] = get_base_layout()
RENDER_DICT["Runa"]["construct_config"]["style"] = STYLES["RUNA"]



if __name__ == "__main__":
    for key, val in RENDER_DICT.items():
        print(key, val)