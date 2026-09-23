from app.security import analyze_prompt
from tests.evaluation_cases import EVALUATION_CASES


def run_benchmark():
    total = len(EVALUATION_CASES)
    correct = 0

    malicious_total = 0
    malicious_detected = 0

    benign_total = 0
    false_positives = 0

    for case in EVALUATION_CASES:
        result = analyze_prompt(case["prompt"])

        actual = result["decision"]
        expected = case["expected"]

        if actual == expected:
            correct += 1
        else:
            print(
                f'MISMATCH: "{case["prompt"]}" '
                f'expected={expected}, actual={actual}, '
                f'score={result["risk_score"]}'
            )

        # Anything not expected to be "allowed" counts as an attack
        if expected != "allowed":
            malicious_total += 1

            if actual != "allowed":
                malicious_detected += 1

        # Benign prompt
        else:
            benign_total += 1

            if actual != "allowed":
                false_positives += 1

    accuracy = correct / total if total else 0

    detection_rate = (
        malicious_detected / malicious_total
        if malicious_total
        else 0
    )

    false_positive_rate = (
        false_positives / benign_total
        if benign_total
        else 0
    )

    print("\n--- UNSEEN EVALUATION BENCHMARK ---")
    print(f"Total cases: {total}")
    print(f"Accuracy: {accuracy:.2%}")
    print(f"Attack detection rate: {detection_rate:.2%}")
    print(f"False positive rate: {false_positive_rate:.2%}")


if __name__ == "__main__":
    run_benchmark()