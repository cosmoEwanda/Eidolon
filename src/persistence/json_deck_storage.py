import json
import uuid
from pathlib import Path
import os
import tempfile


class JsonDeckStorage:

    def __init__(self, folder):
        self.folder = Path(folder)
        self.folder.mkdir(parents=True, exist_ok=True)

    def save(self, data: dict):
        file_path = self.folder / f"{data['id']}.json"
        self._atomic_write(file_path, data)

    def delete(self, deck_id: str):
        file_path = self.folder / f"{deck_id}.json"
        if file_path.exists():
            file_path.unlink()
            return
        # Fallback: cerca per id nel contenuto (vecchi file con nome diverso)
        for file in self.folder.glob("*.json"):
            with open(file, encoding="utf8") as f:
                try:
                    if json.load(f).get("id") == deck_id:
                        file.unlink()
                        return
                except (json.JSONDecodeError, OSError):
                    pass

    def load_all(self) -> list[dict]:
        decks = []
        for file in self.folder.glob("*.json"):
            with open(file, encoding="utf8") as f:
                data = json.load(f)
            # Migrazione: assegna id ai vecchi mazzi salvati per nome
            if "id" not in data:
                data["id"] = str(uuid.uuid4())
                self._atomic_write(file, data)
                # Rinomina il file da {name}.json a {id}.json
                new_path = self.folder / f"{data['id']}.json"
                if file != new_path:
                    os.replace(file, new_path)
            decks.append(data)
        return decks

    def get_by_name(self, name: str) -> dict | None:
        for file in self.folder.glob("*.json"):
            with open(file, encoding="utf8") as f:
                data = json.load(f)
                if data.get("name") == name:
                    return data
        return None

    def get_by_id(self, deck_id: str) -> dict | None:
        file_path = self.folder / f"{deck_id}.json"
        if file_path.exists():
            with open(file_path, encoding="utf8") as f:
                return json.load(f)
        return None

    def _atomic_write(self, file_path: Path, data: dict):
        fd, tmp_name = tempfile.mkstemp(prefix=file_path.name + ".", suffix=".tmp", dir=str(self.folder))
        tmp_path = Path(tmp_name)
        try:
            with os.fdopen(fd, "w", encoding="utf8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                f.flush()
                os.fsync(f.fileno())
            os.replace(tmp_path, file_path)
        except Exception:
            try:
                if tmp_path.exists():
                    tmp_path.unlink()
            except Exception:
                pass
            raise
