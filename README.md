---
title: team-alpha-docqa
emoji: 🧪
colorFrom: blue
colorTo: gray
sdk: docker
app_port: 8080
pinned: false
---

# Orbit DocQA (Team Alpha)

Answers questions about the Orbit Home Router manual, with the source pages it used.

- Retrieval: BM25 over paragraph chunks of `docs/` (`app/bm25.py`, `app/rag.py`)
- API: `POST /ask {"q": "..."}` returns `{"answer", "sources"}`, and `GET /health` (`app/main.py`)
- Evaluation: `python -m eval.eval_retrieval` computes Recall@3 and MRR on the held-out `test` split of `eval/qa.jsonl`.
  Current result: **Recall@3 = 1.0, MRR = 1.0 on 8 held-out questions**. This is a small and easy set; answers are extractive, not generated.
- Tests: `pytest -q` (5 tests, run in CI on every push)

```bash
pip install -r requirements.txt && uvicorn app.main:app
curl -X POST localhost:8000/ask -H 'Content-Type: application/json' -d '{"q": "how do I factory reset"}'
```


---
*Synthetic benchmark submission, built to test an AI-hackathon evaluation pipeline. Not a real team's project.*
