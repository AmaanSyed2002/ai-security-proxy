import json
from datetime import datetime
from pathlib import Path


LOG_FILE = Path("security_events.jsonl")


def log_security_event(prompt: str, analysis: dict):
    event = {
        "timestamp": datetime.utcnow().isoformat(),
        "prompt": prompt,
        "decision": analysis["decision"],
        "risk_score": analysis["risk_score"],
        "detected_patterns": analysis["detected_patterns"],
    }

    with LOG_FILE.open("a") as file:
        file.write(json.dumps(event) + "\n")