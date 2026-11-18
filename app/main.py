from fastapi import FastAPI
from pydantic import BaseModel

from app.rag import answer

app = FastAPI(title="Orbit DocQA")


class Ask(BaseModel):
    q: str


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/ask")
def ask(body: Ask) -> dict[str, object]:
    return answer(body.q)
