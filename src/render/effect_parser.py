import re
from .types import Token

class EffectParser:

    ICON_PATTERN = re.compile(r"\[([^\]]+)\]")

    def parse(self, text: str):
        tokens = []
        last_index = 0

        for match in self.ICON_PATTERN.finditer(text):
            start, end = match.span()

            # testo prima dell'icona
            if start > last_index:
                tokens.append(
                    Token("text", text[last_index:start])
                )

            # icona
            tokens.append(
                Token("icon", match.group(1))
            )

            last_index = end

        # testo finale
        if last_index < len(text):
            tokens.append(
                Token("text", text[last_index:])
            )

        return tokens