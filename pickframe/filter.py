import numpy as np

from .types import Frame


def sharpness(img: np.ndarray) -> float:
    raise NotImplementedError


def clip_pct(img: np.ndarray) -> float:
    raise NotImplementedError


def gate(frames: list[Frame], cfg: dict) -> list[Frame]:
    raise NotImplementedError
