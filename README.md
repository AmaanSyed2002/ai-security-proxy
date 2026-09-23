# AI Security Gateway & LLM Threat Detection

## Project Summary

This project is a security layer built in front of an LLM application to inspect prompts before they reach the model and inspect responses before they are returned to the user.

The gateway uses rule based detection and risk scoring to identify common prompt injection and jailbreak patterns, including attempts to override prior instructions, extract hidden system or developer instructions, disable safety controls, force a specific output, or push the model into an unrestricted mode.

Incoming prompts are classified as allowed, review, or blocked. Requests that pass the input checks can be sent to the LLM, while model responses are checked for sensitive data such as API keys, private keys, and passwords before being returned.

The project also includes security event logging, detection metrics, red team test cases, holdout tests, unseen evaluation cases, and Garak integration for external prompt injection testing.

## Features

- **Prompt injection detection:** Detects instruction override attempts, hidden instruction extraction, forced output hijacking, safety disablement, authority replacement, and jailbreak-style prompts.
- **Risk scoring:** Assigns scores to detected patterns and uses thresholds to classify prompts as allowed, review, or blocked.
- **Benign context handling:** Includes rules for common educational and defensive security prompts so normal security questions are less likely to be flagged.
- **Output security:** Scans LLM responses for API keys, private key material, and password-like values, then redacts sensitive matches before returning the response.
- **FastAPI gateway:** Exposes proxy, generation, health, and metrics endpoints for testing and integration.
- **Security event logging:** Records prompt decisions, risk scores, detected patterns, and timestamps in JSONL format for local analysis.
- **Detection metrics:** Tracks total events, allowed requests, review decisions, blocked requests, and overall detection rate.
- **Mock LLM mode:** Supports local testing without sending requests to a live model or consuming API credits.
- **Red team testing:** Includes malicious prompt cases and benign false-positive cases to measure how the detection logic behaves.
- **Holdout testing:** Uses a separate set of prompts that are not part of the main tuning set.
- **Unseen evaluation set:** Tests the detector against additional attack wording and benign prompts to check whether the rules generalize beyond the original examples.
- **Garak integration:** Includes a REST configuration for running Garak against the local gateway through the `/generate` endpoint.

## Garak PromptInject Benchmark

Tested the gateway against Garak PromptInject cases.

- Baseline: 0% detection
- After tuning: 79.56%
- Final run: 100% detection
- 768/768 PromptInject requests blocked
