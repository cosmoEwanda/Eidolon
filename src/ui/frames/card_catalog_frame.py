from tkinter import Frame, Menu
from .cardsheet_maker_frame import CardSheetMakerFrame


class CardCatalogFrame(Frame):
    def __init__(self, master, cards, on_card_double_click, on_view_card, on_reload_selected):
        super().__init__(master)

        self.on_card_double_click = on_card_double_click
        self.on_view_card = on_view_card
        self.on_reload_selected = on_reload_selected

        self._right_clicked_card_id = None

        self.context_menu = Menu(self, tearoff=0)
        self.context_menu.add_command(label="Vedi carta", command=self._view_card)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Marca/Demarca ricarica art", command=self._toggle_reload_mark)
        self.context_menu.add_command(label="Ricarica art marcate", command=self._reload_marked)
        self.context_menu.add_command(label="Svuota marcature", command=self._clear_marks)

        self.sheet = CardSheetMakerFrame(self, cards)
        self.sheet.pack(fill="both", expand=True)

        self.sheet.tree.bind("<Double-1>", self._double_click)
        self.sheet.tree.bind("<Button-3>", self._right_click)
        self.sheet.tree.bind("<Button-2>", self._right_click)  # macOS

    def _double_click(self, event):
        row_id = self.sheet.tree.identify_row(event.y)
        if not row_id:
            return

        # se iid == card_id:
        card_id = row_id
        self.on_card_double_click(card_id)

    def _right_click(self, event):
        row_id = self.sheet.tree.identify_row(event.y)
        if not row_id:
            return

        self._right_clicked_card_id = row_id
        self.context_menu.tk_popup(event.x_root, event.y_root)

    def _view_card(self):
        if self._right_clicked_card_id:
            self.on_view_card(self._right_clicked_card_id)

    def _toggle_reload_mark(self):
        """Toggle della marcatura sulla carta right-clicked."""
        cid = self._right_clicked_card_id
        if not cid:
            return

        # Usa gli helper che abbiamo aggiunto in CardSheetMakerFrame
        if cid in self.sheet.reload_ids:
            self.sheet.reload_ids.remove(cid)
            mark = "☐"
        else:
            self.sheet.reload_ids.add(cid)
            mark = "☑"

        values = list(self.sheet.tree.item(cid, "values"))
        values[0] = mark  # prima colonna = Reload
        self.sheet.tree.item(cid, values=values)

    def _reload_marked(self):
        ids = self.sheet.get_reload_ids()
        if ids:
            self.on_reload_selected(ids)

    def _clear_marks(self):
        self.sheet.clear_reload_marks()