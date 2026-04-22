from src.basic_config._paths_composer import (
    select_drive_interactively,
    load_saved_drive,
    clear_config,
    resource_path,
    get_app_data_folder
)
import sys
from tkinter import messagebox

FONT_PATH = "C:/Windows/Fonts/Arial.ttf"


ASSETS_DIR = resource_path("assets")
CONSTRUCTS_DIR = ASSETS_DIR / "constructs"
ICONS_DIR = ASSETS_DIR / "icons"

APP_DATA = get_app_data_folder()
OUTPUT_DIR = APP_DATA / "output"
for d in ["images", "json", "deck"]:
    (OUTPUT_DIR / d).mkdir(parents=True, exist_ok=True)

selected_drive = load_saved_drive()
if not selected_drive:
    selected_drive = select_drive_interactively()

if not selected_drive:
    messagebox.showerror(
        title="Errore importazione dati",
        message="È necessario selezionare il Drive per continuare."
    )

    sys.exit()

POSSIBLE_DRIVE_NAMES = ["Il mio Drive", "My Drive", "Mon Drive", "Google Drive"]
DRIVE_ROOT_DIR = None

for name in POSSIBLE_DRIVE_NAMES:
    temp_path = selected_drive / name / "Eidolon"
    if temp_path.exists():
        DRIVE_ROOT_DIR = temp_path
        break

if not DRIVE_ROOT_DIR:
    # Se arriviamo qui, il drive (es. G:/) esiste, ma non contiene Eidolon.
    # Forse l'utente ha scelto il drive sbagliato o ha spostato i file.

    confirm = messagebox.askyesno(
        title="Cartella Eidolon non trovata",
        message=(f"Non ho trovato la cartella 'Eidolon' in {selected_drive}.\n\n"
                 "Vuoi cancellare questa configurazione e sceglierne una nuova?")
    )

    if confirm:
        clear_config()  # Elimina il JSON in LocalAppData

    sys.exit()  # Chiude l'app per permettere il riavvio pulito

IMAGES_DIR = OUTPUT_DIR / "images"
IMAGES_DIR.mkdir(exist_ok=True)

JSON_DIR = OUTPUT_DIR / "json"
JSON_DIR.mkdir(exist_ok=True)

DECK_DIR = OUTPUT_DIR / "deck"
DECK_DIR.mkdir(exist_ok=True)

ONLINE_IMAGES_DIR = DRIVE_ROOT_DIR / "Immagini carte"
ONLINE_IMAGES_DIR.mkdir(exist_ok=True)

ONLINE_DECK_DIR = DRIVE_ROOT_DIR / "PdfDecks"
ONLINE_DECK_DIR.mkdir(exist_ok=True)

CARD_SHEET = (
    "https://docs.google.com/spreadsheets/d/"
    "100c4Gp3yjAmLCyOeEHHjHPsrNtzn0xS--xkqfDNuBdQ/"
    "export?format=csv&gid=0"
)

ORDER_SHEET = (
    "https://docs.google.com/spreadsheets/d/"
    "100c4Gp3yjAmLCyOeEHHjHPsrNtzn0xS--xkqfDNuBdQ/"
    "export?format=csv&gid=436643684"
)