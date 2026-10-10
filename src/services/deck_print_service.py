from __future__ import annotations

import os
import tempfile
from pathlib import Path
from typing import List, Optional, Dict, Tuple

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader


class PdfInUseError(RuntimeError):
    """Raised when the target PDF cannot be overwritten (likely open in a viewer)."""
    pass


class DeckPrintService:
    """
    Genera un PDF impaginato con le immagini delle carte del deck a dimensioni fisiche fisse.
    """

    def __init__(self, image_provider):
        self.image_provider = image_provider

    def build_pdf_for_deck(
        self,
        deck,
        output_path: Optional[Path] = None,
        cards_per_row: int = 3,
        rows_per_page: int = 3,
        card_w_mm: float = 59.0,  # 63x88 per Standard (Magic/Pokemon), 59x86 per Yu-Gi-Oh!
        card_h_mm: float = 86.0,
        gap_mm: float = 2.0,
    ) -> Path:
        card_ids = self._expand_deck_ids(deck)

        if output_path is None:
            output_path = Path(tempfile.gettempdir()) / f"deck_{self._safe_filename(deck.name)}.pdf"

        self._ensure_writable(output_path)

        page_w, page_h = A4
        mm = 72.0 / 25.4

        cols = cards_per_row
        rows = rows_per_page

        card_w = card_w_mm * mm
        card_h = card_h_mm * mm
        gap = gap_mm * mm

        # Calcola l'ingombro totale della griglia di carte
        total_grid_w = (cols * card_w) + ((cols - 1) * gap)
        total_grid_h = (rows * card_h) + ((rows - 1) * gap)

        if total_grid_w > page_w or total_grid_h > page_h:
            raise ValueError(
                f"La griglia richiesta ({total_grid_w / mm:.1f}x{total_grid_h / mm:.1f} mm) "
                f"eccede il formato A4 ({page_w / mm:.1f}x{page_h / mm:.1f} mm). "
                f"Riduci gap_mm o verifica le dimensioni delle carte."
            )

        # Centra la griglia nella pagina A4
        margin_x = (page_w - total_grid_w) / 2.0
        margin_y = (page_h - total_grid_h) / 2.0

        c = canvas.Canvas(str(output_path), pagesize=A4)

        index = 0
        per_page = cols * rows
        img_cache: Dict[str, Tuple[ImageReader, int, int]] = {}

        while index < len(card_ids):
            for slot in range(per_page):
                if index >= len(card_ids):
                    break

                cid = card_ids[index]
                index += 1

                r = slot // cols
                col = slot % cols

                # Coordinata X e Y (ReportLab ha l'origine in basso a sinistra)
                x = margin_x + col * (card_w + gap)
                y = page_h - margin_y - (r + 1) * card_h - r * gap

                img_path = self.image_provider.load_image_by_id(cid)
                if img_path and Path(img_path).exists():
                    self._draw_image_fit_cached(c, Path(img_path), x, y, card_w, card_h, img_cache)
                else:
                    c.rect(x, y, card_w, card_h, stroke=1, fill=0)
                    c.drawString(x + 6, y + card_h - 14, "Missing image:")
                    c.drawString(x + 6, y + card_h - 30, str(cid))

            c.showPage()

        c.save()
        return output_path

    def preview(self, pdf_path: Path):
        self._open_file(pdf_path)

    def print_pdf(self, pdf_path: Path):
        try:
            if os.name == "nt":
                os.startfile(str(pdf_path), "print")
            else:
                self._open_file(pdf_path)
        except Exception:
            self._open_file(pdf_path)

    def _ensure_writable(self, path: Path):
        path.parent.mkdir(parents=True, exist_ok=True)

        if not path.exists():
            try:
                path.touch(exist_ok=False)
                path.unlink(missing_ok=True)
            except PermissionError as e:
                raise PdfInUseError(f"Impossibile creare il PDF in: {path}") from e
            return

        tmp = path.with_suffix(path.suffix + ".locktest")
        try:
            path.replace(tmp)
            tmp.replace(path)
        except PermissionError as e:
            try:
                if tmp.exists() and not path.exists():
                    tmp.replace(path)
            except Exception:
                pass
            raise PdfInUseError(f"PDF già aperto: {path}") from e
        except OSError as e:
            try:
                if tmp.exists() and not path.exists():
                    tmp.replace(path)
            except Exception:
                pass
            raise PdfInUseError(f"Impossibile scrivere il PDF (forse aperto): {path}") from e

    def _expand_deck_ids(self, deck) -> List[str]:
        ids = []
        for cid, qty in deck.cards.items():
            try:
                q = int(qty)
            except Exception:
                q = 1
            if q <= 0:
                continue
            ids.extend([cid] * q)
        return ids

    def _draw_image_fit_cached(
        self,
        c,
        img_path: Path,
        x: float,
        y: float,
        w: float,
        h: float,
        cache: Dict[str, Tuple[ImageReader, int, int]],
    ):
        key = str(img_path)
        entry = cache.get(key)
        if entry is None:
            img = ImageReader(key)
            iw, ih = img.getSize()
            cache[key] = (img, iw, ih)
        else:
            img, iw, ih = entry

        if iw <= 0 or ih <= 0:
            return

        # Disegna l'immagine forzata al rettangolo esatto della carta
        # Se preferisci ritagliare l'eventuale bleed invece di forzare le proporzioni,
        # qui puoi mantenere preserveAspectRatio=True
        c.drawImage(img, x, y, width=w, height=h, preserveAspectRatio=False)

    def _open_file(self, path: Path):
        try:
            if os.name == "nt":
                os.startfile(str(path))
            elif os.name == "posix":
                opener = "open" if "darwin" in os.sys.platform else "xdg-open"
                os.system(f'{opener} "{path}"')
            else:
                os.system(f'"{path}"')
        except Exception:
            pass

    def _safe_filename(self, name: str) -> str:
        s = "".join(ch if ch.isalnum() or ch in (" ", "-", "_") else "_" for ch in (name or "deck"))
        return "_".join(s.strip().split()) or "deck"