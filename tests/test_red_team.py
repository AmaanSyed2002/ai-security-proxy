from app.security import analyze_prompt
from tests.red_team_cases import RED_TEAM_CASES


def test_red_team_cases():
    for case in RED_TEAM_CASES:
        result = analyze_prompt(case["prompt"])

        assert result["decision"] == case["expected"], (
            f'Prompt failed: "{case["prompt"]}" '
            f'Expected: {case["expected"]}, '
            f'Got: {result["decision"]}'
        )