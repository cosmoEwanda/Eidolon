import json
from pathlib import Path
import os
import tempfile


class JsonDeckStorage:

    def __init__(self, folder):
        self.folder = Path(folder)
        self.folder.mkdir(parents=True, exist_ok=True)

    def save(self, name: str, data: dict):
        """Riceve nome e dict. Non sa cos'è un Deck."""
        file_path = self.folder / f"{name}.json"
        self._atomic_write(file_path, data)

    def delete(self, name: str):
        """Cancella basandosi sul nome del file."""
        file_path = self.folder / f"{name}.json"
        if file_path.exists():
            file_path.unlink()

    def load_all(self) -> list[dict]:
        """Restituisce una lista di dizionari."""
        decks = []
        for file in self.folder.glob("*.json"):
            with open(file, encoding="utf8") as f:
                decks.append(json.load(f))
        return decks

    def get_by_name(self, name: str):
        file_path = self.folder / f"{name}.json"
        if file_path.exists():
            with open(file_path, encoding="utf8") as f:
                return json.load(f)
        else:
            return None

    def _atomic_write(self, file_path: Path, data: dict):
        fd, tmp_name = tempfile.mkstemp(prefix=file_path.name + ".", suffix=".tmp", dir=str(self.folder))
        tmp_path = Path(tmp_name)
        try:
            with os.fdopen(fd, "w", encoding="utf8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                f.flush()
                os.fsync(f.fileno())
            os.replace(tmp_path, file_path)  # sovrascrive atomico
        except Exception:
            try:
                if tmp_path.exists():
                    tmp_path.unlink()
            except Exception:
                pass
            raise