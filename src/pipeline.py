from pathlib import Path

import pandas as pd

from src.cache import load_cache, save_cache, build_cache_key
from src.ollama_client import classify_comment


def run_pipeline(config: dict) -> pd.DataFrame:
    runtime = config["runtime"]
    paths = config["paths"]
    columns = config["columns"]
    taxonomy = config["taxonomy"]
    thresholds = config["thresholds"]

    debug = runtime["debug"]
    limit = runtime["limit"]
    checkpoint_interval = runtime["checkpoint_interval"]

    cache_config = config["cache"]
    cache_read_enabled = cache_config["read_enabled"]
    cache_write_enabled = cache_config["write_enabled"]

    if debug in ("cache", "all"):
        print(f"Cache settings: read={cache_read_enabled} write={cache_write_enabled}")

    if not cache_read_enabled:
        print("Cache reads disabled.")

    if not cache_write_enabled:
        print("Cache writes disabled.")

    df = pd.read_csv(paths["input"])

    if limit is not None:
        df = df.head(limit)

    print(f"Processing {len(df)} comments...")

    cache = load_cache(paths["cache"])
    cache_hits = 0
    cache_misses = 0
    results = []

    for index, row in df.iterrows():
        topic = safe_get(row, columns["topic"])
        question = safe_get(row, columns["question"])
        comment = safe_get(row, columns["comment"])
        department = safe_get(row, columns["department"])
        team = safe_get(row, columns["team"])

        if not comment or comment.lower() == "nan":
            continue

        cache_key = build_cache_key(
            prompt_version=config["prompt_version"],
            topic=topic,
            question=question,
            comment=comment,
        )

        if cache_read_enabled and cache_key in cache:
            result = cache[cache_key]
            cache_hits += 1

            if debug in ("cache", "all"):
                print(f"CACHE HIT: {index} - {comment[:80]}")
        else:
            cache_misses += 1

            if debug in ("cache", "all"):
                print(f"CACHE MISS: {index} - {comment[:80]}")
            else:
                print(f"Processing comment {index}: {comment[:80]}...")

            result = classify_comment(
                topic=topic,
                question=question,
                comment=comment,
                department=department,
                team=team,
                model=config["model"],
                ollama_url=config["ollama_url"],
                taxonomy=taxonomy,
                thresholds=thresholds,
                debug=debug,
            )
            if cache_write_enabled:
                cache[cache_key] = result

        results.append(
            {
                "index": index,
                "topic": topic,
                "question": question,
                "comment": comment,
                "department": department,
                "team": team,
                **result,
            }
        )

        if checkpoint_interval and len(results) % checkpoint_interval == 0:
            save_results(results, paths, thresholds, quiet=True)
            if cache_write_enabled:
                save_cache(cache, paths["cache"])

    if cache_write_enabled:
        save_cache(cache, paths["cache"])

    total_requests = cache_hits + cache_misses

    if total_requests > 0:
        hit_rate = cache_hits / total_requests
    else:
        hit_rate = 0

    print(
        f"\nCache: {cache_hits} hits, {cache_misses} misses ({hit_rate:.0%} hit rate)"
    )

    return save_results(results, paths, thresholds)


def safe_get(row: pd.Series, column_name: str | None) -> str:
    if not column_name:
        return ""

    if column_name not in row.index:
        return ""

    value = row[column_name]

    if pd.isna(value):
        return ""

    return str(value).strip()


def save_results(
    results: list[dict], paths: dict, thresholds: dict, quiet: bool = False
) -> pd.DataFrame:
    output_df = pd.DataFrame(results)

    output_path = Path(paths["output"])
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_df.to_csv(output_path, index=False)

    export_review_files(output_df, paths, thresholds)

    if not quiet:
        print(f"\nSaved results to {output_path}.")

        print(
            f"Other comments exported: "
            f"{len(output_df[output_df['primary_theme'] == 'Other'])}"
        )

        print(
            f"Low confidence comments exported: "
            f"{len(output_df[output_df['confidence'] < thresholds['low_confidence_export']])}"
        )

    return output_df


def export_review_files(
    output_df: pd.DataFrame,
    paths: dict,
    thresholds: dict,
) -> None:

    other_df = output_df[output_df["primary_theme"] == "Other"]

    other_df.to_csv(paths["other_review"], index=False)

    low_confidence_df = output_df[
        output_df["confidence"] < thresholds["low_confidence_export"]
    ]

    low_confidence_df.to_csv(paths["low_confidence_review"], index=False)
