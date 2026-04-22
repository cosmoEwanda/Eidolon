from PIL import Image, ImageDraw, ImageFont


class TextBoxRenderer:
    def __init__(self, icon_cache):
        self.icon_cache = icon_cache

    def render(self, layout, width: int, style) -> Image.Image:
        # 'layout' deve essere un oggetto LayoutResult, non una stringa
        img = Image.new("RGBA", (width, layout.content_height), style.bg_color)
        draw = ImageDraw.Draw(img)

        for line in layout.lines:
            for t in line:
                if t.kind == "text":
                    draw.text((t.x, t.y), t.value, font=t.font, fill=style.text_color)
                elif t.kind == "icon" and t.value in self.icon_cache:
                    icon = self.icon_cache[t.value]  # Se è un path
                    with Image.open(icon).convert("RGBA") as icon_img:
                        icon_img = icon_img.resize(style.icon_size)
                        img.paste(icon_img, (int(t.x), int(t.y)), mask=icon_img)
        return img

    def render_simple(self, text: str, width: int, style) -> Image.Image:
        """Metodo mancante per renderizzare testi brevi senza layout complesso."""

        font = ImageFont.truetype(style.font_path, style.font_size)
        # Calcolo altezza singola riga
        bbox = draw = ImageDraw.Draw(Image.new("RGBA", (1, 1))).textbbox((0, 0), text, font=font)
        h = bbox[3] - bbox[1] + style.padding.top + style.padding.bottom

        img = Image.new("RGBA", (width, int(h)), style.bg_color)
        ImageDraw.Draw(img).text((style.padding.left, style.padding.top), text, font=font, fill=style.text_color)
        return img