from dataclasses import dataclass, field

import numpy as np


@dataclass
class Frame:
    idx: int
    img: np.ndarray
    passed: bool = True
    reason: str = ""
    features: dict[str, float] = field(default_factory=dict)
    score: float = 0.0
