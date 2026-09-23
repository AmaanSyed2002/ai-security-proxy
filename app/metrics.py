import json
from pathlib import Path


LOG_FILE = Path("security_events.jsonl")


def get_security_metrics():
    metrics = {
        "total_events": 0,
        "allowed": 0,
        "review": 0,
        "blocked": 0,
    }

    if not LOG_FILE.exists():
        return metrics

    with LOG_FILE.open("r") as file:
        for line in file:
            if not line.strip():
                continue

            event = json.loads(line)
            decision = event.get("decision")

            metrics["total_events"] += 1

            if decision in metrics:
                metrics[decision] += 1

    return metrics


def get_detection_summary():
    metrics = get_security_metrics()

    total = metrics["total_events"]
    detected = metrics["review"] + metrics["blocked"]

    detection_rate = (
        detected / total
        if total
        else 0
    )

    return {
        **metrics,
        "detected": detected,
        "detection_rate": round(detection_rate, 4),
    }