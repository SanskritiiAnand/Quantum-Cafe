#musical scales used by quantum cafe
from dataclasses import dataclass
from typing import List

@dataclass(frozen=True)
class Scale:
    name: str
    notes: tuple[int, ...]

#morning collection
MORNING_PENTATONIC = Scale(name="Morning Pentatonic",
                           notes=[48,   # C3
                                  50,   # D3
                                  52,   # E3
                                  55,   # G3
                                  57,   # A3
                                  60,   # C4
                                  62,
                                  64,
                                  67,
                                  69,
                                  72,   # C5
                                  74,
                                  76,
                                  79,
                                  81,]
                          )