from tkinter import Frame, Label, Button, StringVar, Entry, Canvas, Scrollbar

class DeckListFrame(Frame):
    def __init__(self, master, deck, on_save):
        super().__init__(master)

        self.deck = deck
        self.on_save = on_save

        Label(self, text="Nome mazzo").pack(fill="x")

        self.deck_name_var = StringVar(value=deck.name)
        Entry(self, textvariable=self.deck_name_var).pack(fill="x", padx=5, pady=5)

        # Header: titolo + contatore a destra
        header = Frame(self)
        header.pack(fill="x")

        Label(header, text="Mazzo Corrente, ").pack(side="left")
        self.card_count_var = StringVar()
        self.card_count_label = Label(header, textvariable=self.card_count_var)
        self.card_count_label.pack(side="left")



        # --- SCROLLABLE AREA ---
        self.scroll_container = Frame(self)
        self.scroll_container.pack(fill="both", expand=True)

        self.canvas = Canvas(self.scroll_container, highlightthickness=0)
        self.v_scroll = Scrollbar(self.scroll_container, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.v_scroll.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.v_scroll.pack(side="right", fill="y")

        # frame interno dentro il canvas
        self.list_container = Frame(self.canvas)
        self._window_id = self.canvas.create_window((0, 0), window=self.list_container, anchor="nw")

        # aggiorna scrollregion quando cambia contenuto
        self.list_container.bind("<Configure>", self._on_frame_configure)
        # mantiene la larghezza del frame interno uguale al canvas (righe full-width)
        self.canvas.bind("<Configure>", self._on_canvas_configure)

        # rotellina mouse (Windows/macOS; su Linux spesso Button-4/5)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Button-4>", lambda e: self.canvas.yview_scroll(-1, "units"))
        self.canvas.bind_all("<Button-5>", lambda e: self.canvas.yview_scroll(1, "units"))
        # --- END SCROLLABLE AREA ---

        Button(self, text="Salva", command=self._save_clicked).pack(fill="x")

        self.refresh()

    def _on_frame_configure(self, event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, event):
        # fa sì che l'inner frame abbia la stessa larghezza del canvas
        self.canvas.itemconfigure(self._window_id, width=event.width)

    def _on_mousewheel(self, event):
        # Su Windows: event.delta = +/-120; su macOS spesso +/-1
        delta = event.delta
        if delta == 0:
            return
        step = -1 if delta > 0 else 1
        # più fluido su Windows
        if abs(delta) >= 120:
            step = int(-delta / 120)
        self.canvas.yview_scroll(step, "units")

    def refresh(self):
        for w in self.list_container.winfo_children():
            w.destroy()

        for cid, qty in self.deck.cards.items():
            self._create_row(cid, qty)

        self.card_count_var.set(f"N Carte: {self.deck.total_cards()}")
        self._on_frame_configure()

    def _create_row(self, cid, qty):
        row = Frame(self.list_container)
        row.pack(fill="x", pady=2)

        Label(row, text=cid, width=20, anchor="w").pack(side="left")

        Button(row, text="-", width=3, command=lambda c=cid: self._dec(c)).pack(side="left")
        Label(row, text=str(qty), width=5).pack(side="left")
        Button(row, text="+", width=3, command=lambda c=cid: self._inc(c)).pack(side="left")

    def _inc(self, cid):
        self.deck.add(cid)
        self.refresh()

    def _dec(self, cid):
        self.deck.remove(cid)
        self.refresh()

    def _save_clicked(self):
        self.deck.name = self.deck_name_var.get()
        self.on_save()

    def selected_cards(self):
        return self.deck.cards

    def deck_name(self):
        return self.deck_name_var.get()