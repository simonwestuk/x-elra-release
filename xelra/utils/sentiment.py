"""Lightweight lexicon-based sentiment heuristic used as a simple fallback."""

import re

# Minimal heuristic analyser with a pluggable hook
POS = set(
    """good great excellent amazing love helpful clear concise engaging brilliant awesome fantastic insightful easy comfortable supportive enjoyable recommend satisfied happy like well done""".split()
)
NEG = set(
    """bad poor terrible awful hate confusing unclear long boring frustrating difficult hard disappointed unhappy dislike not recommend rubbish useless dreadful horrible annoying worse worst struggle struggled struggling""".split()
)
NEGATORS = set("""not never no hardly barely scarcely seldom without""".split())


def _tokenise(text: str):
    return re.findall(r"[a-zA-Z']+", (text or "").lower())


def analyse(text: str) -> tuple[float, float]:
    """Return (polarity in [-1,1], confidence in [0,1])."""

    toks = _tokenise(text)
    if not toks:
        return 0.0, 0.0
    score = 0
    prev = None
    for t in toks:
        if prev in NEGATORS and t in POS:
            score -= 1
        elif prev in NEGATORS and t in NEG:
            score += 1
        else:
            if t in POS:
                score += 1
            if t in NEG:
                score -= 1
        prev = t
    # normalise by length
    raw = score / max(3.0, len(toks) / 5.0)
    # squash to [-1,1]
    polarity = max(-1.0, min(1.0, raw))
    conf = min(1.0, abs(polarity))
    return polarity, conf
