from pathlib import Path
from src.render import RenderCard


class CardRendererService:
    def __init__(
            self,
            assets_library,
            render_dict,
            text_builder,
            text_renderer,
            images_dir,
            default_style = None
    ):
        self.assets = assets_library
        self.render_dict = render_dict
        self.text_builder = text_builder
        self.text_renderer = text_renderer
        self.images_dir = images_dir
        self.default_style = default_style


    def render_and_save(self, card, out_path: Path):
        """
        Punto di ingresso usato da ImageRenderSync.
        Seleziona il layout corretto in base al costrutto della carta.
        """
        # Recupera il layout specifico (es. Incarnato, Varco, o Default)
        layout_config = self.render_dict.get(card.construct, self.render_dict.get("DEFAULT"))

        if not layout_config:
            raise ValueError(f"Nessun layout configurato per il costrutto: {card.construct}")

        # Esegue il rendering effettivo
        return self._execute_render(card, layout_config, out_path)

    def _execute_render(self, card, layout, out_path):
        # 1. Template (già corretto nei messaggi precedenti)
        template_key = card.construct if card.construct in self.assets["Templates"] else "DEFAULT"
        template_path = self.assets["Templates"][template_key]
        composer = RenderCard(card, template_path=template_path)


        # 2. Ciclo Dinamico sulle sezioni
        for section_key, section_data in layout.items():
            # Evitiamo di processare chiavi di configurazione che non sono "testi"
            if section_key in ["orders_config", "art_config"] or not isinstance(section_data, dict): #da aggiungere art
                continue

            # Recuperiamo lo stile specifico della sezione (es. lo stile 'name' per la sezione 'name_config')
            style = section_data.get("style", self.default_style)
            elems = section_data.get("elems", {})


            for elem_key, rect in elems.items():
                content = self._resolve_card_value(card, elem_key)
                if content is not None:
                    # Passiamo tutto il necessario: non serve più cercare nel dizionario globale
                    self._draw_element(composer, content, rect, style)

        # 3. Altri elementi (Ordini e Art)
        self._draw_orders(composer, card, layout.get("orders_config").get("elems"))
        self._draw_art(composer, layout.get("art_config").get("elems").get("art"), card)

        # 4. Salvataggio
        out_path.parent.mkdir(parents=True, exist_ok=True)
        composer.get_template().save(out_path)
        return out_path

    def _resolve_card_value(self, card, key):
        """Mappa le chiavi del layout ai dati della carta in modo sicuro."""
        # 1. Campi base
        mapping = {
            "Name": card.name,
            "Construct": card.construct,
            "Rarity": card.rarity,
            "Ability": card.ability
        }
        if key in mapping:
            return mapping[key]

        # 2. Controllo Stats (Sicuro)
        stats = card.get_attributes("stats")
        if stats is not None and key in stats:
            return str(stats[key])

        # 3. Controllo Costs (Sicuro)
        costs = card.get_attributes("cost")
        if costs is not None and key in costs:
            return str(costs[key])

        return None

    def _draw_element(self, composer, text, rect, style):
        """Metodo puro: riceve dati e disegna, senza cercare chiavi esterne."""
        if not text or text == "NULL":
            return

        pos = rect["pos"]
        w, h = rect["dim"]
        # Se c'è uno stile (TextBoxStyle), usiamo il builder (auto-fit)
        # Se style è None, il renderer semplice userà i suoi parametri interni di base
        if style:
            img = self.text_builder.build(text, w, h, style)
        else:
            # Fallback se proprio non abbiamo stili
            img = self.text_renderer.render_simple(text, h, None)

        composer.template.paste(img, pos, img)

    def _draw_orders(self, composer, card, orders_config):
        """
        Renderizza le icone degli ordini presenti sulla carta.
        """

        # Verifica che esista la configurazione e che la carta abbia ordini
        if not orders_config or not card.get_attributes("orders"):
            return

        # Iteriamo sugli ordini effettivamente presenti sulla carta
        for i, ord_name in enumerate(card.get_attributes("orders")):
            # Recuperiamo il file dall'Asset Library passata al costruttore
            icon_path = self.assets["Icons"].get(ord_name)

            if icon_path and Path(icon_path).exists():
                # Calcoliamo l'offset orizzontale dinamico

                composer.render_external_image(
                    str(icon_path),
                    *orders_config[ord_name]["pos"],
                    orders_config[ord_name]["dim"]
                )

    def _draw_art(self, composer, config, card):
        """Disegna l'illustrazione della carta."""
        # Nota: recuperiamo il percorso dal sistema di file locale o asset
        art_path = self.images_dir / f"{card.img}"
        if art_path.exists():
            # Coordinate standard per l'art box (possono essere rese dinamiche nel layout)
            composer.render_external_image(art_path, *config.get("pos"), config.get("dim"))