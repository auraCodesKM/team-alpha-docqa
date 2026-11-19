# Orbit DocQA (Team Alpha)

**Problem.** Router support teams answer the same questions all day ("how do I factory reset?", "which ports are open?"), and the answers are buried in a 40-page manual.

**Solution.** Ask a question, get the exact manual passage that answers it, with the section it came from, so the answer can be checked.

## Architecture
```
POST /ask {"q"}  ->  app/main.py  ->  app/rag.py: answer()
                                     |-- load_chunks(): manual (docs/*.md) split into paragraphs
                                     |-- BM25 index (app/bm25.py, no external services)
                                     '-- top passage + its source section -> {"answer", "sources"}
```
Retrieval is lexical BM25, written from scratch; answers are extractive (no text generation), so they cannot hallucinate.

## Claims
- Every answer includes the manual sections it came from (`sources`).
- Retrieval quality: **Recall@3 = 1.0, MRR = 1.0 on 8 held-out questions** (`python -m eval.eval_retrieval`, test split of `eval/qa.jsonl`). A small, easy set.
- 5 unit tests, run by GitHub Actions on every push.
- Live at **https://team-alpha-docqa.vercel.app** (`GET /health`, `POST /ask`).

## Try it
```bash
curl -s -X POST https://team-alpha-docqa.vercel.app/ask -H 'Content-Type: application/json' -d '{"q": "how do I factory reset"}'
```

## Run locally
```bash
pip install -r requirements.txt
uvicorn app.main:app
pytest -q
python -m eval.eval_retrieval
```

---
*Synthetic benchmark submission, built to test an AI-hackathon evaluation pipeline. Not a real team's project.*
