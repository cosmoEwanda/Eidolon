import json
from pathlib import Path
from typing import Optional

from src.domain import CardDefinition


def migrate_deck_costs(
    deck_dir: Path,
    card_dir: Path,
    costs: Optional[list[str]] = None,
    dry_run: bool = False,
) -> dict:
    """
    Ricalcola avg_cost per tutti i deck usando le carte correnti.
    Versatile: se COSTS cambia, basta eseguire questa funzione.

    Args:
        deck_dir: Directory con i deck JSON.
        card_dir: Directory con le carte JSON ({id}.json).
        costs: Lista chiavi costo. Default: CardDefinition.VALID_COSTS.
        dry_run: Se True, mostra cosa cambierebbe senza scrivere.

    Returns:
        stats: {"total": N, "updated": N, "skipped": N, "errors": N}
    """
    if costs is None:
        costs = CardDefinition.VALID_COSTS
    deck_dir, card_dir = Path(deck_dir), Path(card_dir)

    # 1. Carica tutte le carte in un lookup {id: data}
    cards = {}
    for card_file in card_dir.glob("*.json"):
        try:
            with open(card_file, encoding="utf-8") as f:
                data = json.load(f)
            cid = data.get("id")
            if cid:
                cards[cid] = data
        except Exception as e:
            print(f"[WARN] Lettura carta {card_file.name}: {e}")

    if not cards:
        print("[ERRORE] Nessuna carta caricata.")
        return {"total": 0, "updated": 0, "skipped": 0, "errors": 0}

    print(f"[INFO] Caricate {len(cards)} carte")

    stats = {"total": 0, "updated": 0, "skipped": 0, "errors": 0}

    # 2. Processa ogni deck
    for deck_file in sorted(deck_dir.glob("*.json")):
        stats["total"] += 1
        try:
            with open(deck_file, encoding="utf-8") as f:
                deck = json.load(f)

            deck_cards = deck.get("cards", {})
            if not deck_cards:
                stats["skipped"] += 1
                continue

            total_cards = sum(deck_cards.values())
            if total_cards == 0:
                stats["skipped"] += 1
                continue

            # 3. Ricalcola avg_cost per ogni tipo di costo
            new_avg_cost = {}
            for cost_key in costs:
                total = 0.0
                n = 0
                for cid, qty in deck_cards.items():
                    card = cards.get(cid)
                    if not card:
                        continue
                    val = card.get("cost", {}).get(cost_key)
                    if val is not None:
                        try:
                            total += float(val) * qty
                            n += qty
                        except (ValueError, TypeError):
                            pass
                new_avg_cost[cost_key] = round(total / n, 2) if n > 0 else 0.0

            # 4. Confronta e aggiorna
            old = deck.get("avg_cost", {})
            if old == new_avg_cost:
                stats["skipped"] += 1
                continue

            deck["avg_cost"] = new_avg_cost
            if not dry_run:
                with open(deck_file, "w", encoding="utf-8") as f:
                    json.dump(deck, f, indent=2, ensure_ascii=False)

            print(f"[OK] {deck_file.stem}: {dict(old)} -> {new_avg_cost}")
            stats["updated"] += 1

        except Exception as e:
            print(f"[ERRORE] {deck_file.stem}: {e}")
            stats["errors"] += 1

    print(
        f"\n[Riepilogo] totali={stats['total']}, "
        f"aggiornati={stats['updated']}, "
        f"saltati={stats['skipped']}, errori={stats['errors']}"
    )
    return stats


if __name__ == "__main__":
    import sys

    from src.basic_config._paths_composer import get_app_data_folder

    output_dir = get_app_data_folder() / "output"
    deck_dir = output_dir / "deck"
    card_dir = output_dir / "json"
    dry = "--dry-run" in sys.argv

    if not deck_dir.exists():
        print(f"[ERRORE] Deck dir non trovata: {deck_dir}")
        sys.exit(1)
    if not card_dir.exists():
        print(f"[ERRORE] Card dir non trovata: {card_dir}")
        sys.exit(1)

    migrate_deck_costs(deck_dir, card_dir, dry_run=dry)
