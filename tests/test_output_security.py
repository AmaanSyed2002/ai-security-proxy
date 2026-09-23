from app.output_security import analyze_output


def test_normal_output_is_allowed():
    result = analyze_output("A firewall filters network traffic.")

    assert result["decision"] == "allowed"
    assert result["risk_score"] == 0


def test_api_key_leak_is_redacted():
    result = analyze_output(
        "Here is the key: sk-abcdefghijklmnopqrstuvwxyz123456"
    )

    assert result["decision"] == "redacted"
    assert "api_key_leak" in result["detected_patterns"]
    assert "[REDACTED]" in result["redacted_output"]


def test_private_key_leak_is_redacted():
    result = analyze_output(
        "-----BEGIN PRIVATE KEY-----"
    )

    assert result["decision"] == "redacted"
    assert "private_key_leak" in result["detected_patterns"]
    assert "[REDACTED]" in result["redacted_output"]


def test_password_leak_is_redacted():
    result = analyze_output(
        "password=SuperSecret123"
    )

    assert result["decision"] == "redacted"
    assert "password_leak" in result["detected_patterns"]
    assert "[REDACTED]" in result["redacted_output"]