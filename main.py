import os
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from .models import QueryRequest, FeedbackRequest
from .local_retriever import LocalKeywordRetriever, DATA_DIR
from .moss_retriever import MossRetriever
from .policy import check_query_policy
from .audit import log_event

load_dotenv()

app = FastAPI(title="Sovereign AI Workbench - Moss Prototype")
local_retriever = LocalKeywordRetriever()
moss_retriever = MossRetriever()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/", response_class=HTMLResponse)
def home():
    return Path("app/static/index.html").read_text(encoding="utf-8")

@app.get("/health")
def health():
    return {
        "status": "ok",
        "retrieval_mode": "moss" if moss_retriever.enabled else "local-fallback"
    }

@app.post("/documents")
async def upload_document(file: UploadFile = File(...)):
    if not file.filename or not file.filename.lower().endswith(".txt"):
        return {"ok": False, "message": "Only .txt files are supported in this prototype."}

    content = await file.read()
    if len(content) > 1_000_000:
        return {"ok": False, "message": "File is too large for the prototype limit."}

    safe_name = Path(file.filename).name
    (DATA_DIR / safe_name).write_bytes(content)
    log_event("document_uploaded", {"filename": safe_name})
    return {
        "ok": True,
        "filename": safe_name,
        "message": "Saved locally. Run build_moss_index.py to index it in Moss."
    }

@app.post("/query")
async def query(request: QueryRequest):
    allowed, message = check_query_policy(request.question, request.user_role)
    log_event("query_policy_check", {
        "question": request.question,
        "role": request.user_role,
        "allowed": allowed
    })

    if not allowed:
        return {"ok": False, "answer": message, "sources": []}

    moss_result = None
    if moss_retriever.enabled:
        try:
            moss_result = await moss_retriever.query(request.question)
        except Exception as exc:
            log_event("moss_query_error", {"error": str(exc)})
            moss_result = None

    if moss_result is not None:
        results = moss_result["results"]
        retrieval_mode = "moss"
        latency_ms = moss_result["time_taken_ms"]
    else:
        results = local_retriever.retrieve(request.question)
        retrieval_mode = "local-fallback"
        latency_ms = None

    if not results:
        answer = "I could not find relevant content in the available local index."
    else:
        answer = "Based on the retrieved passages:\n\n" + "\n\n".join(
            f"- {item['text']}" for item in results
        )

    log_event("query_completed", {
        "question": request.question,
        "result_count": len(results),
        "retrieval_mode": retrieval_mode,
        "latency_ms": latency_ms
    })

    return {
        "ok": True,
        "answer": answer,
        "retrieval_mode": retrieval_mode,
        "retrieval_latency_ms": latency_ms,
        "sources": [
            {"source": item["source"], "score": item["score"]}
            for item in results
        ],
        "retrieved_context": results
    }

@app.post("/feedback")
def feedback(request: FeedbackRequest):
    log_event("user_feedback", request.model_dump())
    return {"ok": True, "message": "Feedback recorded locally."}

@app.get("/audit")
def audit():
    path = Path("data/audit.jsonl")
    if not path.exists():
        return {"events": []}
    return {"events": path.read_text(encoding="utf-8").splitlines()}
