import json
from pathlib import Path


def load_cache(cache_path: str) -> dict:
    path = Path(cache_path)

    if not path.exists():
        return {}
    
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)
    

def save_cache(cache: dict, cache_path: str) -> None:
    path = Path(cache_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as file:
        json.dump(cache, file, ensure_ascii=False, indent=2)

def build_cache_key(prompt_version: str, topic: str, question: str, comment: str) -> str:
    return  "::".join(
        [
            prompt_version.strip().lower(),
            topic.strip().lower(),
            question.strip().lower(),
            comment.strip().lower(),
        ]
    )