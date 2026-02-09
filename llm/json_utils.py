import json
import re
from typing import Any

def extract_json(text: str) -> Any:
    """
    Tries to parse JSON even if the model accidentally wrapped it.
    """
    text = text.strip()

    # If it already parses, great
    try:
        return json.loads(text)
    except Exception:
        pass

    # Try to find a JSON object inside the text
    m = re.search(r"(\{.*\})", text, flags=re.DOTALL)
    if m:
        candidate = m.group(1)
        return json.loads(candidate)

    raise ValueError("Could not parse JSON from model output")
