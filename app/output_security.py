import re


def analyze_output(output: str):
    rules = [
        {
            "name": "api_key_leak",
            "pattern": r"\bsk-[a-zA-Z0-9_-]{20,}\b",
            "score": 100,
        },
        {
            "name": "private_key_leak",
            "pattern": r"-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----",
            "score": 100,
        },
        {
            "name": "password_leak",
            "pattern": r"(password|passwd|pwd)\s*[:=]\s*\S+",
            "score": 70,
        },
    ]

    detected_patterns = []
    risk_score = 0
    redacted_output = output

    for rule in rules:
        if re.search(rule["pattern"], output, re.IGNORECASE):
            detected_patterns.append(rule["name"])
            risk_score += rule["score"]

            redacted_output = re.sub(
                rule["pattern"],
                "[REDACTED]",
                redacted_output,
                flags=re.IGNORECASE
            )

    if risk_score >= 70:
        decision = "redacted"
    elif risk_score >= 25:
        decision = "review"
    else:
        decision = "allowed"

    return {
        "decision": decision,
        "risk_score": risk_score,
        "detected_patterns": detected_patterns,
        "redacted_output": redacted_output,
    }