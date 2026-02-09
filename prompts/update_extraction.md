You are updating an existing JSON extraction of columns/filters based on user feedback.

Given:
1) CURRENT_JSON (valid JSON)
2) USER_FEEDBACK (text)

Return ONLY the UPDATED valid JSON in the exact same schema.
- Apply corrections: rename columns, add/remove filters, change operators/values, add tables, etc.
- If user feedback is ambiguous, add a question to questions_for_user.
CURRENT_JSON:
{{CURRENT_JSON}}
USER_FEEDBACK:
{{USER_FEEDBACK}}