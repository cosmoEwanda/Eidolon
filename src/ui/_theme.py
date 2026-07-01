from tkinter import ttk

BG_PRIMARY = "#f0f2f5"
BG_SECONDARY = "#ffffff"
BG_HOVER = "#e4e7eb"
TEXT_PRIMARY = "#1a1a2e"
TEXT_SECONDARY = "#6c757d"
ACCENT = "#4361ee"
ACCENT_HOVER = "#3a56d4"
SUCCESS = "#06d6a0"
SUCCESS_LIGHT = "#d3f5e2"
DANGER = "#ef476f"
DANGER_LIGHT = "#fce4ec"
WARNING = "#ffd166"
BORDER = "#dee2e6"

FONT_DEFAULT = ("Segoe UI", 10)
FONT_TITLE = ("Segoe UI", 14, "bold")
FONT_HEADING = ("Segoe UI", 12, "bold")
FONT_SMALL = ("Segoe UI", 9)
FONT_MONO = ("Consolas", 10)

def config_ttk_style():
    style = ttk.Style()
    style.theme_use("clam")

    style.configure("Treeview",
                    background=BG_SECONDARY,
                    foreground=TEXT_PRIMARY,
                    fieldbackground=BG_SECONDARY,
                    borderwidth=0,
                    font=FONT_DEFAULT)
    style.map("Treeview",
              background=[("selected", ACCENT)])
    style.configure("Treeview.Heading",
                    background=BG_PRIMARY,
                    foreground=TEXT_PRIMARY,
                    borderwidth=0,
                    font=FONT_DEFAULT,
                    relief="flat")
    style.map("Treeview.Heading",
              background=[("active", BG_HOVER)])

    style.configure("Vertical.TScrollbar",
                    background=BG_PRIMARY,
                    troughcolor=BG_SECONDARY,
                    borderwidth=0,
                    arrowsize=10)
    style.configure("Horizontal.TScrollbar",
                    background=BG_PRIMARY,
                    troughcolor=BG_SECONDARY,
                    borderwidth=0,
                    arrowsize=10)

    return style
