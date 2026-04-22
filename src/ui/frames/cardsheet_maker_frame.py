import pandas as pd
from tkinter import Frame, Toplevel, Label
from tkinter.ttk import Treeview, Scrollbar
from ._cardsheet_config import COLUMNS_MAP


class CardSheetMakerFrame(Frame):
    TOOLTIP_WRAP = 300
    SHORT_LEN = 35

    RELOAD_COL_ID = "__reload__"
    RELOAD_COL_TEXT = "Ricarica art"

    def __init__(self, master, item_list, on_reload_selected=None):
        """
        on_reload_selected: callback(ids: list[str]) -> None
        (la UI lo chiama quando premi il pulsante che aggiungerai nel parent, oppure lo chiami tu)
        """
        super().__init__(master)
        self.pack(fill="both", expand=True)

        self.on_reload_selected = on_reload_selected
        self.reload_ids: set[str] = set()

        # ------------------------------
        # DATAFRAME + quantity
        # ------------------------------
        df = pd.DataFrame([
            {
                'id': item.id,
                **{field: item.to_dict.get(field, None) for field in COLUMNS_MAP.keys()}
            }
            for item in item_list
        ])

        quantity = df['id'].value_counts().to_dict()
        df_counted = df.groupby('id', as_index=False).first()
        df_counted['quantity'] = df_counted['id'].map(quantity)

        self.item_list = df_counted
        self.tooltip = None
        self.tooltip_label = None
        self._full_text_cache = {}

        # ------------------------------
        # TREEVIEW
        # ------------------------------
        container = Frame(self, bg="white")
        container.pack(fill="both", expand=True)

        scroll_y = Scrollbar(container, orient="vertical")
        scroll_y.pack(side="right", fill="y")

        scroll_x = Scrollbar(container, orient="horizontal")
        scroll_x.pack(side="bottom", fill="x")

        # Colonna extra per “checkbox”
        columns = [self.RELOAD_COL_TEXT] + [COLUMNS_MAP[col]["text"] for col in COLUMNS_MAP.keys()]

        self.tree = Treeview(
            container,
            columns=columns,
            show="headings",
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set,
            selectmode="extended"
        )

        # Heading colonna reload
        self.tree.heading(self.RELOAD_COL_TEXT, text=self.RELOAD_COL_TEXT)
        self.tree.column(self.RELOAD_COL_TEXT, width=80, stretch=False, anchor="center")

        # Headings normali
        for key, value in COLUMNS_MAP.items():
            col = value["text"]
            self.tree.heading(col, text=col)
            w = value.get("width", value.get("min", 80))
            self.tree.column(col, width=w, stretch=True)

        self.tree.pack(fill="both", expand=True)

        scroll_y.config(command=self.tree.yview)
        scroll_x.config(command=self.tree.xview)

        # ------------------------------
        # POPOLA
        # ------------------------------
        self._populate(items=df_counted.to_dict(orient='records'))

        # ------------------------------
        # BIND
        # ------------------------------
        self.tree.bind("<Motion>", self._on_hover)
        self.tree.bind("<Leave>", lambda e: self._hide_tooltip())
        self.tree.bind("<Configure>", lambda e: self._apply_weighted_widths())

        # Toggle “checkbox” con click
        self.tree.bind("<Button-1>", self._on_click, add=True)

    def get_reload_ids(self) -> list[str]:
        """IDs marcati ☑ per ricaricare art."""
        return sorted(self.reload_ids)

    def clear_reload_marks(self):
        self.reload_ids.clear()
        # aggiorna la colonna visiva
        for iid in self.tree.get_children(""):
            values = list(self.tree.item(iid, "values"))
            if values:
                values[0] = "☐"
                self.tree.item(iid, values=values)

    # ------------------------------
    # LAYOUT COLONNE
    # ------------------------------
    def _apply_weighted_widths(self):
        total_w = self.tree.winfo_width()
        if total_w <= 1:
            return

        # spazio lasciato alla colonna reload
        reload_w = 80
        remaining = max(0, total_w - reload_w)

        cols = list(COLUMNS_MAP.keys())
        weights = [COLUMNS_MAP[c].get("weight", 1) for c in cols]
        mins = [COLUMNS_MAP[c].get("min", 40) for c in cols]

        w_sum = sum(weights)
        base = sum(mins)
        extra = max(0, remaining - base)

        for c, w, mn in zip(cols, weights, mins):
            px = mn + int(extra * (w / w_sum))
            self.tree.column(COLUMNS_MAP[c]["text"], width=px, stretch=True)

    # ------------------------------
    # POPOLA
    # ------------------------------
    def _populate(self, items):
        for item in items:
            qty = item["quantity"]
            cid = str(item["id"])     # <-- IID STABILE = ID CARTA

            display_values = ["☐"]    # colonna reload
            col_offset = 1            # shift per cache tooltip

            for col_index, field in enumerate(COLUMNS_MAP.keys()):
                full = self._format_full_value(item[field])
                if qty > 1 and field == "name":
                    full = f"{qty}x {full}"

                short = self._shorten(full)

                display_values.append(short)
                self._full_text_cache[(cid, col_index + col_offset)] = full

            self.tree.insert("", "end", iid=cid, values=display_values)

    # ------------------------------
    # CLICK: toggle checkbox
    # ------------------------------
    def _on_click(self, event):
        row_id = self.tree.identify_row(event.y)
        col = self.tree.identify_column(event.x)  # "#1" è la prima colonna (Reload)
        if not row_id or col != "#1":
            return

        # toggle
        if row_id in self.reload_ids:
            self.reload_ids.remove(row_id)
            mark = "☐"
        else:
            self.reload_ids.add(row_id)
            mark = "☑"

        values = list(self.tree.item(row_id, "values"))
        values[0] = mark
        self.tree.item(row_id, values=values)

        # evita che il click cambi selezione in modo fastidioso
        # (opzionale) self.tree.selection_set(row_id)

    # ------------------------------
    # FORMAT / TOOLTIP (quasi uguali)
    # ------------------------------
    def _format_full_value(self, value):
        if value == "NULL" or value is None:
            return ""
        if isinstance(value, dict):
            return ", ".join(f"{k}:{v}" for k, v in value.items())
        if isinstance(value, list):
            return ", ".join(map(str, value))
        return str(value)

    def _shorten(self, text):
        row = text.split("\n")[0]
        if len(row) <= self.SHORT_LEN:
            return row
        return row[:self.SHORT_LEN] + "..."

    def _on_hover(self, event):
        row_id = self.tree.identify_row(event.y)
        column = self.tree.identify_column(event.x)

        if not row_id or not column:
            self._hide_tooltip()
            return

        try:
            col_index = int(column[1:]) - 1
            # col_index 0 è la colonna Reload: niente tooltip
            if col_index == 0:
                self._hide_tooltip()
                return

            full_text = self._full_text_cache.get((row_id, col_index), "")
            if len(full_text) <= self.SHORT_LEN:
                self._hide_tooltip()
                return
        except Exception:
            self._hide_tooltip()
            return

        self._show_tooltip(event.x_root, event.y_root, full_text)

    def _show_tooltip(self, x, y, text):
        if self.tooltip is None:
            self.tooltip = Toplevel(self)
            self.tooltip.wm_overrideredirect(True)
            self.tooltip_label = Label(
                self.tooltip,
                background="#ffffe0",
                relief="solid",
                borderwidth=1,
                justify="left",
                wraplength=self.TOOLTIP_WRAP
            )
            self.tooltip_label.pack(ipadx=6, ipady=4)

        self.tooltip_label.config(text=text)
        self.tooltip.geometry(f"+{x+15}+{y+10}")

    def _hide_tooltip(self):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None
            self.tooltip_label = None