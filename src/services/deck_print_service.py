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
    Genera un PDF impaginato con le immagini delle carte del deck.
    - Anteprima: apri il PDF col viewer default
    - Stampa (Windows): os.startfile(pdf, "print")
    """

    def __init__(self, image_provider):
        """
        image_provider deve esporre:
            load_image_by_id(card_id) -> Path | None
        """
        self.image_provider = image_provider


    # -------------------------------------------------------------

    def build_pdf_for_deck(
        self,
        deck,
        output_path: Optional[Path] = None,
        cards_per_row: int = 3,
        rows_per_page: int = 3,
        margin_mm: float = 10.0,
        gap_mm: float = 2.0
    ) -> Path:
        """
        deck.cards: dict[str, int]  (id -> quantity)
        """
        card_ids = self._expand_deck_ids(deck)

        if output_path is None:
            output_path = Path(tempfile.gettempdir()) / f"deck_{self._safe_filename(deck.name)}.pdf"

        # Fail fast se il PDF è aperto / non scrivibile
        self._ensure_writable(output_path)

        page_w, page_h = A4

        mm = 72.0 / 25.4
        margin = margin_mm * mm
        gap = gap_mm * mm

        cols = cards_per_row
        rows = rows_per_page

        usable_w = page_w - 2 * margin - (cols - 1) * gap
        usable_h = page_h - 2 * margin - (rows - 1) * gap

        cell_w = usable_w / cols
        cell_h = usable_h / rows

        c = canvas.Canvas(str(output_path), pagesize=A4)

        index = 0
        per_page = cols * rows

        # Cache ImageReader per path: evita decode ripetuti (molto importante con PNG 940x1410)
        img_cache: Dict[str, Tuple[ImageReader, int, int]] = {}
        while index < len(card_ids):
            for slot in range(per_page):
                if index >= len(card_ids):
                    break

                cid = card_ids[index]
                index += 1

                r = slot // cols
                col = slot % cols

                x = margin + col * (cell_w + gap)
                y = page_h - margin - (r + 1) * cell_h - r * gap

                img_path = self.image_provider.load_image_by_id(cid)
                if img_path and Path(img_path).exists():
                    self._draw_image_fit_cached(c, Path(img_path), x, y, cell_w, cell_h, img_cache)
                else:
                    c.rect(x, y, cell_w, cell_h, stroke=1, fill=0)
                    c.drawString(x + 6, y + cell_h - 14, "Missing image:")
                    c.drawString(x + 6, y + cell_h - 30, str(cid))

            c.showPage()

        c.save()
        return output_path

    # -------------------------------------------------------------

    def preview(self, pdf_path: Path):
        self._open_file(pdf_path)

    def print_pdf(self, pdf_path: Path):
        """
        Windows: startfile(print).
        Altrove: apri il PDF e l'utente stampa dal viewer.
        """
        try:
            if os.name == "nt":
                os.startfile(str(pdf_path), "print")
            else:
                self._open_file(pdf_path)
        except Exception:
            self._open_file(pdf_path)

    # -------------------- helpers --------------------

    def _ensure_writable(self, path: Path):
        """
        Su Windows un PDF aperto spesso non è rinominabile/sovrascrivibile.
        Questo check fallisce subito e permette alla UI di mostrare messagebox.
        """
        path.parent.mkdir(parents=True, exist_ok=True)

        if not path.exists():
            # Prova a creare e cancellare un file vuoto per verificare permessi
            try:
                path.touch(exist_ok=False)
                path.unlink(missing_ok=True)
            except PermissionError as e:
                raise PdfInUseError(f"Impossibile creare il PDF in: {path}") from e
            return

        # Se esiste già: prova un "rename roundtrip"
        tmp = path.with_suffix(path.suffix + ".locktest")
        try:
            # Se è aperto, spesso qui esplode con PermissionError
            path.replace(tmp)
            tmp.replace(path)
        except PermissionError as e:
            # Ripristino best-effort se qualcosa è rimasto in mezzo
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
        """
        Disegna l'immagine adattandola al riquadro senza distorcerla.
        Usa cache per evitare decode ripetuti.
        """
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

        scale = min(w / iw, h / ih)
        dw = iw * scale
        dh = ih * scale

        dx = x + (w - dw) / 2
        dy = y + (h - dh) / 2

        c.drawImage(img, dx, dy, dw, dh, preserveAspectRatio=True, anchor="c")

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