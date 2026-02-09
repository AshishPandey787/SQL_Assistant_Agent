import os
import tempfile
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel

from core.session_store import create_session, get_session, update_session
from pdf.reader import extract_text_from_pdf
from agent.orchestrator import SQLRAGAgent

agent = SQLRAGAgent()
app = FastAPI(title="SQL RAG Agent")

class FeedbackRequest(BaseModel):
    session_id: str
    feedback: str

class ConfirmRequest(BaseModel):
    session_id: str
    ok: bool
    feedback: str | None = None  # only if ok=False

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/session/create")
def session_create():
    sid = create_session()
    return {"session_id": sid}

# Step 1: upload pdf
@app.post("/pdf/upload")
async def upload_pdf(session_id: str, pdf: UploadFile = File(...)):
    try:
        _ = get_session(session_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Invalid session_id")

    suffix = os.path.splitext(pdf.filename)[-1].lower()
    if suffix != ".pdf":
        raise HTTPException(status_code=400, detail="Upload a PDF file.")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(await pdf.read())
        tmp_path = tmp.name

    text = extract_text_from_pdf(tmp_path)
    os.remove(tmp_path)

    if not text.strip():
        raise HTTPException(status_code=400, detail="No text found in PDF (may be scanned). Use OCR option.")

    extraction = agent.extract(text)

    update_session(session_id, pdf_text=text, extraction=extraction)
    return {
        "session_id": session_id,
        "extraction": extraction,
        "message": "Review extracted tables/columns/filters. Confirm or send corrections."
    }

# Step 3-4: confirm extraction or send correction feedback
@app.post("/extraction/confirm")
def confirm_extraction(req: ConfirmRequest):
    sess = get_session(req.session_id)
    if not sess.get("extraction"):
        raise HTTPException(status_code=400, detail="No extraction found. Upload a PDF first.")

    if req.ok:
        return {"message": "Extraction confirmed. You can now generate SQL."}

    if not req.feedback:
        raise HTTPException(status_code=400, detail="Provide feedback to correct extraction.")

    updated = agent.update_extraction(sess["extraction"], req.feedback)
    update_session(req.session_id, extraction=updated)
    return {"session_id": req.session_id, "extraction": updated}

# Step 5: generate SQL
@app.post("/sql/generate")
def generate_sql(session_id: str):
    sess = get_session(session_id)
    extraction = sess.get("extraction")
    if not extraction:
        raise HTTPException(status_code=400, detail="No extraction found. Upload a PDF first.")

    result = agent.generate_sql(extraction)
    update_session(session_id, sql=result["sql"], sql_notes=result.get("notes"))
    return {"session_id": session_id, **result}

# Step 6-8: refine SQL with user feedback
@app.post("/sql/refine")
def refine_sql(req: FeedbackRequest):
    sess = get_session(req.session_id)
    if not sess.get("sql"):
        raise HTTPException(status_code=400, detail="No SQL found. Generate SQL first.")

    result = agent.refine_sql(sess["sql"], req.feedback, sess.get("extraction"))
    update_session(req.session_id, sql=result["sql"], sql_notes=result.get("notes"))
    return {"session_id": req.session_id, **result}