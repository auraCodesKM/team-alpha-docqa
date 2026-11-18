from fastapi.testclient import TestClient

from app.main import app
from app.rag import RETRIEVER, answer
from eval.eval_retrieval import evaluate

client = TestClient(app)


def test_retrieves_the_reset_page() -> None:
    assert RETRIEVER.retrieve("how do I factory reset", k=1)[0].source == "05-reset.md"


def test_answer_has_sources() -> None:
    out = answer("when do firmware updates install")
    assert out["sources"] and "04-firmware.md" in out["sources"]


def test_unknown_question_says_so() -> None:
    assert answer("zzz qqq")["sources"] == []


def test_api_health_and_ask() -> None:
    assert client.get("/health").json() == {"status": "ok"}
    r = client.post("/ask", json={"q": "can guests see my printer"}).json()
    assert "06-ports.md" in r["sources"]


def test_held_out_retrieval_quality() -> None:
    m = evaluate("test")
    assert m["recall@3"] >= 0.8 and m["mrr"] >= 0.6
