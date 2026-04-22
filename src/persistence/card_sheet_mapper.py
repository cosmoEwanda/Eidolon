import pandas as pd
import hashlib
from pathlib import Path
from ..domain import CardFactory, CardDefinition


class CardSheetMapper:

    def map(self, raw, art_dir):
        df_cards = raw["cards"]
        df_orders = raw["orders"]

        cards = []

        for _, r in df_cards.iterrows():
            sinergy = self._extract_sinergy(r)
            orders = self._extract_orders(r, df_orders)
            cost = self._extract_cost(r)
            stats = self._extract_stats(r)


            # --- LOGICA HASH IBRIDO ---
            # 1. Recuperiamo il timestamp dell'immagine su Drive Desktop
            img_name = f"{r['Nome']}.png"
            art_path = Path(art_dir) / img_name

            mtime = 0
            if art_path.exists():
                # Leggiamo l'epoca di ultima modifica (velocissimo)
                mtime = art_path.stat().st_mtime

            # 2. Creiamo una stringa che rappresenti lo stato attuale della riga + immagine
            # Includiamo i dati critici e il timestamp dell'immagine
            ##data_string = f"{r.to_json()}_{mtime}"
            #card_hash = hashlib.md5(data_string.encode()).hexdigest()

            extra = {
                #"_hash": card_hash  # Salviamo l'hash nei metadati della carta
            }

            if cost:
                # noinspection PyTypeChecker
                extra["cost"] = cost
            if stats:
                # noinspection PyTypeChecker
                extra["stats"] = stats
            if sinergy:
                # noispection PyTypeChecker
                extra["sinergy"] = sinergy

            card = CardFactory.from_input(
                id=r["Id_Carta"],
                name=r["Nome"],
                orders=orders,
                construct=r["Costrutto"],
                rarity=r["Rarità"],
                ability=r["Abilità"],
                img=img_name,
                extra_attributes=extra
            )

            cards.append(card)

        return cards

        # -------------------------

    def _extract_sinergy(self, r):
        if pd.notna(r["Sinergia"]):
            try:
                val = r["Sinergia"]
            except (ValueError, TypeError):
                pass

        return val

    # -------------------------

    def _extract_orders(self, r, df_orders):
        orders_raw = (
            df_orders[df_orders["Id_CO"] == r["Ordini"]]
            [["Ordine1", "Ordine2", "Ordine3", "Ordine4", "Ordine5", "Ordine6"]]
            .values.flatten()
        )

        return [
            str(o)
            for o in orders_raw
            if o != "NULL" and pd.notna(o)
        ]

    # -------------------------

    def _extract_cost(self, r):
        cost = {}
        for col in CardDefinition.VALID_COSTS:
            val = r.get(col)  # Usiamo get per sicurezza
            if pd.notna(val) and val != "NULL":
                try:
                    cost[col] = int(float(val))
                except (ValueError, TypeError):
                    pass
        return cost

    # -------------------------

    def _extract_stats(self, r):
        stats = {}
        for col in CardDefinition.VALID_STATS:
            val = r.get(col)
            if pd.notna(val) and val != "NULL":
                try:
                    stats[col] = int(float(val))
                except (ValueError, TypeError):
                    pass
        return stats

