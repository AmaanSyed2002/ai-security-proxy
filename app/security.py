import re


def contains_any(text: str, patterns: list[str]) -> bool:
    return any(re.search(pattern, text, re.IGNORECASE) for pattern in patterns)


def analyze_prompt(prompt: str):
    text = prompt.lower()

    # Benign educational / defensive context
    benign_context = [
        r"what does .* mean",
        r"explain .* from a defensive perspective",
        r"security class",
        r"security research",
        r"how .* detection works",
        r"describe .* techniques",
        r"what is .* in ai security",
    ]

    if contains_any(text, benign_context):
        return {
            "decision": "allowed",
            "risk_score": 0,
            "detected_patterns": [],
        }

    detected_patterns = []
    risk_score = 0

    # Concept 1: references to earlier/system instructions
    prior_instruction_terms = [
        r"previous instructions",
        r"prior instructions",
        r"earlier instructions",
        r"existing instructions",
        r"instructions above",
        r"earlier guidance",
        r"previous rules",
        r"prior rules",
        r"earlier rules",
        r"rules you started with",
        r"previous policy",
        r"prior policy",
        r"earlier policy",
        r"policy .* earlier",
        r"what you were told before",
        r"previous and following instructions",
        r"previous .* instructions",
        r"following instructions",
    ]

    # Concept 2: tries to negate / replace them
    override_terms = [
        r"ignore",
        r"disregard",
        r"forget",
        r"discard",
        r"override",
        r"optional",
        r"obsolete",
        r"do not apply",
        r"don't apply",
        r"never existed",
        r"follow this message instead",
        r"follow only my",
        r"obey me",
        r"obey the commands below",
        r"with mine",
        r"just say",
        r"just print",
    ]

    # Concept 2b: explicitly replaces authority
    authority_override_terms = [
        r"follow only my",
        r"only my directions",
        r"obey me",
        r"obey my",
        r"follow my instructions instead",
        r"use only my instructions",
    ]

    # Concept 2c: direct forced-output hijacking
    forced_override_terms = [
        r"stop everything",
        r"stop all",
        r"drop everything",
        r"forget everything",
    ]

    forced_output_terms = [
        r"just print",
        r"just say",
        r"respond only with",
        r"output only",
        r"print exactly",
        r"say exactly",
    ]

    if contains_any(text, authority_override_terms):
        detected_patterns.append("authority_override")
        risk_score += 30

    if (
        contains_any(text, prior_instruction_terms)
        and contains_any(text, override_terms)
    ):
        detected_patterns.append("instruction_override")
        risk_score += 40

    if (
        contains_any(text, forced_override_terms)
        and contains_any(text, forced_output_terms)
    ):
        detected_patterns.append("forced_output_hijack")
        risk_score += 60

    if (
        contains_any(text, prior_instruction_terms)
        and contains_any(text, override_terms)
        and contains_any(text, forced_output_terms)
    ):
        detected_patterns.append("forced_output_command")
        risk_score += 20

    # Concept 3: attempts to extract hidden/internal instructions
    hidden_instruction_terms = [
        r"system prompt",
        r"developer message",
        r"developer instructions",
        r"hidden instructions",
        r"internal instructions",
        r"hidden rules",
        r"confidential rules",
        r"private developer configuration",
        r"hidden configuration",
    ]

    extraction_terms = [
        r"reveal",
        r"show",
        r"display",
        r"print",
        r"provide",
        r"tell me",
        r"what .* were supplied",
    ]

    if (
        contains_any(text, hidden_instruction_terms)
        and contains_any(text, extraction_terms)
    ):
        detected_patterns.append("hidden_instruction_extraction")
        risk_score += 60

    # Concept 4: attempts to disable safety protections
    safety_terms = [
        r"safety",
        r"safeguard",
        r"safeguards",
        r"guardrail",
        r"guardrails",
        r"restriction",
        r"restrictions",
        r"protection",
        r"protections",
        r"filter",
        r"filters",
    ]

    disable_terms = [
        r"bypass",
        r"disable",
        r"remove",
        r"without",
        r"no ",
        r"switched off",
        r"turn off",
        r"ignore",
        r"circumvent",
    ]

    if (
        contains_any(text, safety_terms)
        and contains_any(text, disable_terms)
    ):
        detected_patterns.append("safety_disablement")
        risk_score += 45

    # Concept 5: unrestricted persona / jailbreak behavior
    unrestricted_terms = [
        r"unrestricted",
        r"uncensored",
        r"no guardrails",
        r"without safeguards",
        r"jailbreak",
        r"j\s*a\s*i\s*l\s*b\s*r\s*e\s*a\s*k",
    ]

    if contains_any(text, unrestricted_terms):
        detected_patterns.append("unrestricted_behavior")
        risk_score += 35

    # Final decision
    if risk_score >= 50:
        decision = "blocked"
    elif risk_score >= 25:
        decision = "review"
    else:
        decision = "allowed"

    return {
        "decision": decision,
        "risk_score": risk_score,
        "detected_patterns": detected_patterns,
    }