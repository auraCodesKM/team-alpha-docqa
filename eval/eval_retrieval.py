"""Recall@k and MRR of the retriever on the held-out test split of eval/qa.jsonl."""

import json
from pathlib import Path

from app.rag import RETRIEVER


def recall_at_k(gold: str, ranked: list[str], k: int = 3) -> float:
    return 1.0 if gold in ranked[:k] else 0.0


def reciprocal_rank(gold: str, ranked: list[str]) -> float:
    return next((1.0 / i for i, s in enumerate(ranked, 1) if s == gold), 0.0)


def evaluate(split: str = "test", k: int = 3) -> dict[str, float]:
    rows = [json.loads(line) for line in (Path(__file__).parent / "qa.jsonl").read_text().splitlines()]
    rows = [r for r in rows if r["split"] == split]
    ranked = [[c.source for c in RETRIEVER.retrieve(r["q"], k=10)] for r in rows]
    return {"n": len(rows),
            f"recall@{k}": sum(recall_at_k(r["doc"], s, k) for r, s in zip(rows, ranked, strict=True)) / len(rows),
            "mrr": sum(reciprocal_rank(r["doc"], s) for r, s in zip(rows, ranked, strict=True)) / len(rows)}


if __name__ == "__main__":
    print(evaluate())
