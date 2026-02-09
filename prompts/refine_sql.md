You are refining an existing SQL query based on user feedback.

Use KNOWLEDGE_CONTEXT to ensure correctness.

Return ONLY valid JSON:
{
  "sql": "string",
  "notes": ["string", ...],
  "assumptions": ["string", ...]
}

KNOWLEDGE_CONTEXT:
{{KNOWLEDGE_CONTEXT}}

PREVIOUS_SQL:
{{PREVIOUS_SQL}}

USER_FEEDBACK:
{{USER_FEEDBACK}}