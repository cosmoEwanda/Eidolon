from PIL import Image

class RenderCard:
    def __init__(self, card, template_path="DEFAULT"):
        self.card = card

        self.template = Image.open(template_path).convert("RGBA")

    def render_external_image(self, image_path, posx, posy, dim=None):
        """Metodo generico per incollare immagini esterne."""
        with Image.open(image_path) as img:
            img = img.convert("RGBA")
            if dim:
                img = img.resize(dim)
            self.template.paste(img, (posx, posy), img)

    def get_template(self):
        return self.template