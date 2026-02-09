import sqlglot
from sql.safety import is_safe_sql

class SQLValidationError(Exception):
    pass

def validate_sql(sql: str, dialect: str):
    if not is_safe_sql(sql):
        raise SQLValidationError("SQL contains potentially destructive statements.")

    try:
        sqlglot.parse_one(sql, read=dialect)
    except Exception as e:
        raise SQLValidationError(f"SQL parse failed for dialect={dialect}: {e}")