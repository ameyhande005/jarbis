from datetime import datetime, timezone
import json
from pathlib import Path

AUDIT_FILE = Path("data/audit.jsonl")
AUDIT_FILE.parent.mkdir(exist_ok=True)

def log_event(event_type: str, details: dict):
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event_type": event_type,
        "details": details,
    }
    with AUDIT_FILE.open("a", encoding="utf-8") as file:
        file.write(json.dumps(record) + "\n")
