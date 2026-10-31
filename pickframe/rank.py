import numpy as np

from .types import Frame


def _minmax(v: np.ndarray) -> np.ndarray:
    lo, hi = np.nanmin(v), np.nanmax(v)
    return np.zeros_like(v) if hi == lo else (v - lo) / (hi - lo)


def rank(frames: list[Frame], weights: dict[str, float], fallback: list[str]) -> list[Frame]:
    live = [f for f in frames if f.passed]
    if not live:
        return []
    keys = list(weights)
    norm = {
        k: _minmax(np.array([f.features.get(k, np.nan) for f in live], dtype=float))
        for k in keys
    }
    for i, f in enumerate(live):
        has_face = all(k in f.features for k in keys)
        use = keys if has_face else [k for k in fallback if k in f.features]
        w = np.array([weights[k] for k in use])
        x = np.array([norm[k][i] for k in use])
        f.score = float(w @ x / w.sum()) if w.sum() else 0.0
    return sorted(live, key=lambda f: f.score, reverse=True)
