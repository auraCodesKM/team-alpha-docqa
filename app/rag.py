"""Retrieve paragraphs from the product docs and answer extractively, with sources."""

from dataclasses import dataclass
from pathlib import Path

from app.bm25 import BM25, tokens

DOCS = Path(__file__).resolve().parent.parent / "docs"


@dataclass(frozen=True)
class Chunk:
    source: str
    text: str


def load_chunks(root: Path = DOCS) -> list[Chunk]:
    chunks = []
    for p in sorted(root.glob("*.md")):
        for para in p.read_text().split("\n\n"):
            body = " ".join(line for line in para.splitlines() if not line.startswith("#")).strip()
            if body:
                chunks.append(Chunk(p.name, body))
    return chunks


class Retriever:
    def __init__(self, chunks: list[Chunk]) -> None:
        self.chunks = chunks
        self.index = BM25([tokens(c.text) for c in chunks])

    def retrieve(self, question: str, k: int = 3) -> list[Chunk]:
        scores = self.index.scores(tokens(question))
        ranked = sorted(range(len(scores)), key=lambda i: -scores[i])
        return [self.chunks[i] for i in ranked[:k] if scores[i] > 0]


RETRIEVER = Retriever(load_chunks())


def answer(question: str) -> dict[str, object]:
    hits = RETRIEVER.retrieve(question, k=3)
    if not hits:
        return {"answer": "I could not find that in the manual.", "sources": []}
    return {"answer": hits[0].text, "sources": sorted({h.source for h in hits})}
