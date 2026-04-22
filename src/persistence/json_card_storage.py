import json
from pathlib import Path


class JsonCardStorage:
    def __init__(self, folder_path):
        self.folder = Path(folder_path)
        self.folder.mkdir(parents=True, exist_ok=True)

    def save(self, card_id: str, data: dict):
        """Si occupa solo della persistenza fisica."""
        file_path = self.folder / f"{card_id}.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def delete(self, card_id: str):
        """Rimuove fisicamente il file."""
        file_path = self.folder / f"{card_id}.json"
        if file_path.exists():
            file_path.unlink()

    def get_by_id(self, card_id: str) -> dict:
        """Restituisce solo il dizionario. Se manca, solleva FileNotFoundError."""
        file_path = self.folder / f"{card_id}.json"
        if not file_path.exists():
            raise FileNotFoundError(f"File non trovato: {card_id}")

        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def load_all(self) -> list[dict]:
        """Scansiona la cartella e restituisce una lista di dizionari."""
        cards_data = []
        for file in self.folder.glob("*.json"):
            with open(file, "r", encoding="utf-8") as f:
                cards_data.append(json.load(f))
        return cards_data

