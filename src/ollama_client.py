import json
import requests

from src.prompts import build_prompt
from src.validator import validate_result


def classify_comment(
    topic: str,
    question: str,
    comment: str,
    department: str,
    team: str,
    model: str,
    ollama_url: str,
    taxonomy: dict,
    thresholds: dict,
    debug: str = "none",
) -> dict:
    confidence_threshold = thresholds["confidence_review"]

    comment_data = {
        "topic": topic,
        "question": question,
        "comment": comment,
        "department": department,
        "team": team,
    }

    prompt = build_prompt(
        comment_data=comment_data,
        taxonomy=taxonomy,
        confidence_threshold=confidence_threshold,
    )
    
    if debug in ("prompt", "all"):
        print("\n=== PROMPT ===")
        print(prompt)

    response = requests.post(
        ollama_url,
        json={
            "model": model,
            "prompt": prompt,
            "stream": False,
        },
        timeout=120,
    )

    response.raise_for_status()

    raw_output = response.json()["response"]

    if debug in ("raw", "all"):
        print("\n=== RAW OUTPUT ===")
        print(raw_output)

    try:
        parsed = json.loads(raw_output)

    except json.JSONDecodeError:
        parsed = {
            "primary_theme": "Other",
            "secondary_theme": None,
            "sentiment": "mixed",
            "confidence": 0.0,
            "needs_review": True,
            "raw_output": raw_output,
        }

    return validate_result(
        parsed, comment, taxonomy=taxonomy, confidence_threshold=confidence_threshold
    )
