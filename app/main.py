from fastapi import FastAPI
from pydantic import BaseModel

from app.security import analyze_prompt
from app.logger import log_security_event
from app.llm import send_to_llm
from app.output_security import analyze_output
from app.metrics import get_security_metrics, get_detection_summary


app = FastAPI(
    title="AI Security Reverse Proxy",
    description="Security layer for protecting LLM applications",
    version="0.1.0",
)


class PromptRequest(BaseModel):
    prompt: str


@app.get("/")
def home():
    return {
        "status": "running",
        "service": "AI Security Reverse Proxy"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/proxy")
def proxy_prompt(request: PromptRequest):
    input_analysis = analyze_prompt(request.prompt)

    log_security_event(
        prompt=request.prompt,
        analysis=input_analysis
    )

    if input_analysis["decision"] == "blocked":
        return {
            "input_analysis": input_analysis,
            "response": None,
            "message": "Prompt blocked by security policy."
        }

    if input_analysis["decision"] == "review":
        return {
            "input_analysis": input_analysis,
            "response": None,
            "message": "Prompt requires review before being sent to the LLM."
        }

    llm_response = send_to_llm(request.prompt)

    output_analysis = analyze_output(llm_response)

    if output_analysis["decision"] == "redacted":
        return {
            "input_analysis": input_analysis,
            "output_analysis": output_analysis,
            "response": output_analysis["redacted_output"],
            "message": "Sensitive data was detected and redacted."
        }

    return {
        "input_analysis": input_analysis,
        "output_analysis": output_analysis,
        "response": llm_response
    }


@app.get("/metrics")
def security_metrics():
    return get_security_metrics()


@app.post("/generate")
def generate(request: PromptRequest):
    input_analysis = analyze_prompt(request.prompt)

    log_security_event(
        prompt=request.prompt,
        analysis=input_analysis
    )

    if input_analysis["decision"] != "allowed":
        return {
            "text": "",
            "decision": input_analysis["decision"],
            "risk_score": input_analysis["risk_score"],
        }

    llm_response = send_to_llm(request.prompt)

    output_analysis = analyze_output(llm_response)

    if output_analysis["decision"] == "redacted":
        safe_response = output_analysis["redacted_output"]
    else:
        safe_response = llm_response

    return {
        "text": safe_response,
        "decision": input_analysis["decision"],
        "risk_score": input_analysis["risk_score"],
    }


@app.get("/metrics/detection")
def detection_metrics():
    return get_detection_summary()
    