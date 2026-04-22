from dataclasses import dataclass

from .types import Padding

@dataclass(frozen=True)
class TextBoxStyle:
    font_path: str
    font_size: int = 16
    text_color: tuple = (0, 0, 0, 255)
    bg_color: tuple = (255, 255, 255, 0)

    icon_size: tuple = (45, 45)
    interline: int = 4
    padding: Padding = Padding(6, 6, 6, 6)

    align: str = "left"  # left | right | center



