from pydantic import BaseModel
from typing import Optional, List, Literal

class TableRef(BaseModel):
    name: str
    reason: str
    confidence: float

class ColumnRef(BaseModel):
    table: Optional[str] = None
    name: str
    alias: Optional[str] = None
    aggregation: Optional[str] = None
    reason: str
    confidence: float

class FilterRef(BaseModel):
    table: Optional[str] = None
    column: str
    operator: str
    value: str
    value_type: Literal["string", "number", "date", "boolean", "list", "unknown"]
    notes: Optional[str] = None

class OrderByRef(BaseModel):
    table: Optional[str] = None
    column: str
    direction: Literal["asc", "desc"]

class JoinOn(BaseModel):
    left_column: str
    right_column: str

class JoinRef(BaseModel):
    left_table: str
    right_table: str
    on: List[JoinOn]
    type: Literal["inner", "left", "right", "full", "unknown"]

class TimeRange(BaseModel):
    column: Optional[str] = None
    start: Optional[str] = None
    end: Optional[str] = None
    notes: Optional[str] = None

class Extraction(BaseModel):
    intent_summary: str
    tables: List[TableRef]
    columns: List[ColumnRef]
    filters: List[FilterRef]
    group_by: List[dict]
    order_by: List[OrderByRef]
    limit: Optional[int] = None
    joins: List[JoinRef]
    time_range: TimeRange
    assumptions: List[str]
    questions_for_user: List[str]