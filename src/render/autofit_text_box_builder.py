from PIL import ImageFont
from .text_layout import TextLayout
from .effect_parser import EffectParser


class AutoFitTextBoxBuilder:
    def __init__(self, renderer, font_path, min_font_size=15):
        self.renderer = renderer
        self.font_path = font_path
        self.min_font_size = min_font_size
        self.parser = EffectParser()

    def build(self, text, width, height, style):
        tokens = self.parser.parse(text)

        best_result = None

        for current_size in range(style.font_size, self.min_font_size - 1, -1):
            font = ImageFont.truetype(self.font_path, current_size)
            layout_engine = TextLayout(width, font, style.padding)

            layout_result = layout_engine.compute(
                tokens=tokens,
                icon_size=style.icon_size,
                interline=style.interline,
                align=style.align,
            )

            if layout_result.content_height <= height:
                best_result = layout_result
                break

        if best_result is None:
            font = ImageFont.truetype(self.font_path, self.min_font_size)
            layout_engine = TextLayout(width, font, style.padding)

            best_result = layout_engine.compute(
                tokens=tokens,
                icon_size=style.icon_size,
                interline=style.interline,
                align=style.align,
            )

        return self.renderer.render(best_result, width, style)