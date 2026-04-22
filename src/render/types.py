from dataclasses import dataclass
from typing import List, Any

@dataclass(frozen=True)
class Padding:
    top: int = 0
    right: int = 0
    bottom: int = 0
    left: int = 0


@dataclass
class Token:
    kind: str   # "text" | "icon"
    value: str
    x: float = 0
    y: float = 0
    font: Any = None

@dataclass(frozen=True)
class LayoutResult:
    lines: List[List[Token]]
    content_height: int