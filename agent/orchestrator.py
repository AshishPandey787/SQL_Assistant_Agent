import json
from pathlib import Path
from core.config import settings
from llm.azure_openai import chat_json
from llm.json_utils import extract_json
from rag.retriever import Retriever
from sql.validator import validate_sql

PROMPTS_DIR = Path("prompts")

def _load_prompt(name: str) -> str:
    return (PROMPTS_DIR / name).read_text(encoding="utf-8")

class SQLRAGAgent:
    def __init__(self):
        self.retriever = Retriever()
        self.p_extract = _load_prompt("extract_columns_filters.md")
        self.p_update = _load_prompt("update_extraction.md")
        self.p_gen = _load_prompt("generate_sql.md")
        self.p_refine = _load_prompt("refine_sql.md")

    # Step 2: extract columns & filters from PDF text
    def extract(self, pdf_text: str) -> dict:
        user = self.p_extract.replace("{{PDF_TEXT}}", pdf_text[:25000])
        out = chat_json(system="Return only valid JSON.", user=user, temperature=0.1)
        return extract_json(out)

    # Step 4: apply iterative corrections to extraction
    def update_extraction(self, current_json: dict, feedback: str) -> dict:
        user = self.p_update \
            .replace("{{CURRENT_JSON}}", json.dumps(current_json, ensure_ascii=False)) \
            .replace("{{USER_FEEDBACK}}", feedback)
        out = chat_json(system="Return only valid JSON.", user=user, temperature=0.1)
        return extract_json(out)

    # Step 5: generate SQL with RAG
    def generate_sql(self, extraction_json: dict) -> dict:
        query_for_rag = (
            "Schema and SQL patterns for: " +
            extraction_json.get("intent_summary", "") +
            " tables=" + ",".join([t["name"] for t in extraction_json.get("tables", [])])
        )
        context = self.retriever.retrieve(query_for_rag)

        user = self.p_gen \
            .replace("{{SQL_DIALECT}}", settings.SQL_DIALECT) \
            .replace("{{KNOWLEDGE_CONTEXT}}", context) \
            .replace("{{EXTRACTION_JSON}}", json.dumps(extraction_json, ensure_ascii=False))

        out = chat_json(system="Return only valid JSON.", user=user, temperature=0.1)
        result = extract_json(out)

        # Validate SQL
        validate_sql(result["sql"], settings.SQL_DIALECT)
        return result

    # Step 7-8: refine SQL with feedback and RAG again
    def refine_sql(self, previous_sql: str, feedback: str, extraction_json: dict | None = None) -> dict:
        # Use feedback + intent as RAG query
        rag_query = "Fix SQL based on feedback: " + feedback
        if extraction_json:
            rag_query += " intent=" + extraction_json.get("intent_summary", "")

        context = self.retriever.retrieve(rag_query)

        user = self.p_refine \
            .replace("{{KNOWLEDGE_CONTEXT}}", context) \
            .replace("{{PREVIOUS_SQL}}", previous_sql) \
            .replace("{{USER_FEEDBACK}}", feedback)

        out = chat_json(system="Return only valid JSON.", user=user, temperature=0.1)
        result = extract_json(out)

        validate_sql(result["sql"], settings.SQL_DIALECT)
        return result