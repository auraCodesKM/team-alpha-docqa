"""Okapi BM25 over tokenised chunks. Pure Python so tests run anywhere."""

import math
import re
from collections import Counter

_WORD = re.compile(r"[a-z0-9]+")
STOP = {"the", "a", "an", "and", "or", "to", "of", "is", "it", "do", "does", "i", "my", "can", "how", "what", "on",
        "for", "in", "at", "be", "this", "when", "which", "where", "your", "you", "are", "with", "from", "not", "but"}


def tokens(text: str) -> list[str]:
    return [w for w in _WORD.findall(text.lower()) if w not in STOP]


class BM25:
    def __init__(self, docs: list[list[str]], k1: float = 1.5, b: float = 0.75) -> None:
        self.docs, self.k1, self.b = docs, k1, b
        self.avgdl = sum(map(len, docs)) / max(len(docs), 1)
        df = Counter(t for d in docs for t in set(d))
        n = len(docs)
        self.idf = {t: math.log(1 + (n - f + 0.5) / (f + 0.5)) for t, f in df.items()}
        self.tf = [Counter(d) for d in docs]

    def scores(self, query: list[str]) -> list[float]:
        out = []
        for d, tf in zip(self.docs, self.tf, strict=True):
            s = 0.0
            for t in query:
                if t in tf:
                    f = tf[t]
                    s += self.idf[t] * f * (self.k1 + 1) / (f + self.k1 * (1 - self.b + self.b * len(d) / self.avgdl))
            out.append(s)
        return out
