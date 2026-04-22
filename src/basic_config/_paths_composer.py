import json
import os
import tkinter as tk
from tkinter import filedialog
from pathlib import Path


def get_app_data_folder() -> Path:
    """Restituisce la cartella in LocalAppData, creandola se manca."""
    path = Path(os.environ["LOCALAPPDATA"]) / "Eidolon"
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_config_path() -> Path:
    return get_app_data_folder() / "config.json"


def load_saved_drive() -> Path | None:
    """Legge il drive dal file JSON se esiste ed è valido."""
    config_file = get_config_path()
    if config_file.exists():
        try:
            with open(config_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                saved_path = Path(data.get("drive_letter", ""))
                if saved_path.exists():
                    return saved_path
        except:
            pass
    return None


def save_drive_letter(path: Path):
    """Salva la scelta dell'utente."""
    with open(get_config_path(), "w", encoding="utf-8") as f:
        json.dump({"drive_letter": str(path)}, f, indent=4)


def clear_config():
    """Rimuove il file di configurazione per forzare una nuova selezione al prossimo avvio."""
    config_path = get_config_path()
    if config_path.exists():
        config_path.unlink()


def select_drive_interactively() -> Path | None:
    """Apre la GUI per la selezione manuale."""
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    # Chiediamo all'utente di selezionare la lettera del drive (es. G:/)
    selected = filedialog.askdirectory(title="Seleziona l'unità di Google Drive (es. G:)")
    root.destroy()

    if selected:
        path = Path(selected)
        save_drive_letter(path)
        return path
    return None


def resource_path(rel: str) -> Path:
    """Gestisce i percorsi delle risorse sia in script che in eseguibile (PyInstaller)."""
    import sys
    if getattr(sys, "frozen", False):
        base_path = Path(sys._MEIPASS)
    else:
        # Risale di due livelli da src/basic_config/ alla root del progetto
        base_path = Path(__file__).resolve().parent.parent.parent
    return base_path / rel