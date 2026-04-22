import json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import tempfile
import time
import shutil


class ImageRenderSync:
    def __init__(self, image_dir: Path, renderer_service, max_workers: int = 4, use_local_tmp: bool = True):
        self.image_dir = Path(image_dir)          # G:
        self.renderer = renderer_service
        self.meta_file = self.image_dir / "_render_meta.json"
        self.image_dir.mkdir(parents=True, exist_ok=True)
        self.meta_file.parent.mkdir(parents=True, exist_ok=True)
        self.max_workers = max_workers
        self.use_local_tmp = use_local_tmp

    def sync(self, cards, force: bool = False):
        t0 = time.perf_counter()

        meta = self._load_meta()
        updated_meta = {}
        cards = list(cards)
        current_ids = {str(c.id) for c in cards}

        # Unica operazione "directory listing" su G:
        existing_png = {p.stem for p in self.image_dir.glob("*.png")}

        to_render = []
        meta_changed = force  # se force, di fatto può cambiare tutto

        for card in cards:
            cid = str(card.id)
            json_hash = card.get_attributes("_hash")  # SOLO JSON
            old_hash = meta.get(cid)

            has_png = (cid in existing_png)
            needs = force or (old_hash != json_hash) or (not has_png)

            if needs:
                to_render.append((card, self.image_dir / f"{cid}.png"))

            updated_meta[cid] = json_hash
            if old_hash != json_hash:
                meta_changed = True

        # Orfani: png che non corrispondono più a nessuna card
        orphan_stems = existing_png - current_ids

        # EARLY EXIT: niente da fare davvero
        if not to_render and not orphan_stems and not meta_changed:
            dt = time.perf_counter() - t0
            print(f"[IMG] Niente da fare | Total: {dt:.2f}s")
            return

        ok, fail = 0, 0
        errors = []

        def _render_one(card, out_path: Path):
            # tmp locale unico
            if self.use_local_tmp:
                tmp_dir = Path(tempfile.gettempdir()) / "img_render_sync"
                tmp_dir.mkdir(parents=True, exist_ok=True)
            else:
                tmp_dir = out_path.parent

            with tempfile.NamedTemporaryFile(dir=tmp_dir, suffix=".tmp.png", delete=False) as tf:
                tmp_path = Path(tf.name)

            try:
                self.renderer.render_and_save(card, tmp_path)
                # move su G: (copy+delete se FS diverso)
                shutil.move(str(tmp_path), str(out_path))
            finally:
                tmp_path.unlink(missing_ok=True)

        if to_render:
            # Su G: spesso 3-4 worker è meglio di 10
            with ThreadPoolExecutor(max_workers=self.max_workers) as ex:
                futures = [ex.submit(_render_one, c, p) for c, p in to_render]
                for fut in as_completed(futures):
                    try:
                        fut.result()
                        ok += 1
                    except Exception as e:
                        fail += 1
                        errors.append(str(e))

        removed = 0
        for stem in orphan_stems:
            (self.image_dir / f"{stem}.png").unlink(missing_ok=True)
            removed += 1

        self._save_meta(updated_meta)

        dt = time.perf_counter() - t0
        print(f"[IMG] Render: {ok} ok, {fail} fail | Removed: {removed} | Total: {dt:.2f}s")
        if errors:
            print("[IMG] Errori (prime 5):")
            for e in errors[:5]:
                print(" -", e)

    def _load_meta(self):
        if not self.meta_file.exists():
            return {}
        with open(self.meta_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save_meta(self, meta):
        tmp = self.meta_file.with_suffix(".tmp")
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=4)
        tmp.replace(self.meta_file)