from typing import List
from PIL import Image, ImageDraw

from .types import Token, LayoutResult


class TextLayout:
    def __init__(self, width: int, font, padding):
        self.width = width
        self.font = font
        self.padding = padding
        self.draw = ImageDraw.Draw(Image.new("RGBA", (1, 1)))

    def compute(self, tokens: List[Token], icon_size: tuple, interline: int, align: str) -> LayoutResult:
        lines = self._wrap_tokens(tokens, icon_size)

        ascent, descent = self.font.getmetrics()
        text_height = ascent + descent

        current_y = self.padding.top

        for idx, line in enumerate(lines):
            has_icon = any(t.kind == "icon" for t in line)
            line_h = max(text_height, icon_size[1]) if has_icon else text_height

            line_w = self._measure_line(line, icon_size)
            start_x = self._get_start_x(line_w, align)
            current_x = start_x

            for t in line:
                t.x = current_x

                if t.kind == "icon":
                    t.y = current_y + (line_h - icon_size[1]) // 2
                    current_x += icon_size[0] + 4
                else:
                    t.y = current_y + (line_h - text_height) // 2
                    t.font = self.font
                    bbox = self.draw.textbbox((0, 0), t.value, font=self.font)
                    current_x += (bbox[2] - bbox[0])

            current_y += line_h
            if idx < len(lines) - 1:
                current_y += interline

        return LayoutResult(lines, int(current_y + self.padding.bottom))

    def _wrap_tokens(self, tokens: List[Token], icon_size: tuple) -> List[List[Token]]:
        lines = []
        current_line = []
        current_line_w = 0
        max_w = self.width - self.padding.left - self.padding.right

        for t in tokens:
            if t.kind == "text":
                paragraphs = t.value.split("\n")

                for i, p in enumerate(paragraphs):
                    if i > 0:
                        lines.append(current_line)
                        current_line = []
                        current_line_w = 0

                    words = p.split(" ")
                    for j, word in enumerate(words):
                        word_to_draw = word if j == 0 else " " + word
                        bbox = self.draw.textbbox((0, 0), word_to_draw, font=self.font)
                        word_w = bbox[2] - bbox[0]

                        if current_line_w + word_w > max_w and current_line:
                            lines.append(current_line)
                            current_line = [Token(kind="text", value=word.lstrip())]
                            bbox = self.draw.textbbox((0, 0), word.lstrip(), font=self.font)
                            current_line_w = bbox[2] - bbox[0]
                        else:
                            if current_line and current_line[-1].kind == "text":
                                current_line[-1].value += word_to_draw
                            else:
                                current_line.append(Token(kind="text", value=word_to_draw))
                            current_line_w += word_w
            else:
                t_w = icon_size[0] + 4
                if current_line_w + t_w > max_w and current_line:
                    lines.append(current_line)
                    current_line = [t]
                    current_line_w = t_w
                else:
                    current_line.append(t)
                    current_line_w += t_w

        if current_line:
            lines.append(current_line)

        return lines

    def _measure_line(self, line, icon_size: tuple):
        w = 0
        for t in line:
            if t.kind == "text":
                bbox = self.draw.textbbox((0, 0), t.value, font=self.font)
                w += (bbox[2] - bbox[0])
            else:
                w += icon_size[0] + 4
        return w

    def _get_start_x(self, line_w, align):
        if align == "right":
            return self.width - self.padding.right - line_w
        if align == "center":
            return (self.width - line_w) // 2
        return self.padding.left