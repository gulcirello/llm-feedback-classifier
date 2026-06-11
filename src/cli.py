import argparse

REPROCESS_OPTIONS = [
    "all",
    "other",
    "needs_review",
    "other_or_needs_review",
]

DEBUG_OPTIONS = [
    "none",
    "raw",
    "prompt",
    "cache",
    "all",
]


def parse_cli_args():
    parser = argparse.ArgumentParser(
        description="AI-assisted employee feedback classification pipeline."
    )

    parser.add_argument("--input", help="Input CSV path.")
    parser.add_argument("--output", help="Output CSV path.")
    parser.add_argument("--model", help="Ollama model name.")
    parser.add_argument("--limit", type=int, help="Limit number of rows to process.")

    parser.add_argument(
        "--prompt-version",
        help="Prompt version used for cache invalidation, e.g. v1, v2.",
    )

    parser.add_argument(
        "--reprocess",
        choices=REPROCESS_OPTIONS,
        default="all",
        help="Which rows to reprocess.",
    )

    parser.add_argument(
        "--debug",
        choices=DEBUG_OPTIONS,
        default="none",
        help="Debug output mode.",
    )

    parser.add_argument(
        "--skip-cache",
        action="store_true",
        help="Bypass cache and call the model.",
    )

    parser.add_argument(
        "--show-config",
        action="store_true",
        help="Print final config after CLI overrides.",
    )

    return parser.parse_args()


def apply_cli_overrides(config: dict, args) -> dict:
    if args.input:
        config["paths"]["input"] = args.input

    if args.output:
        config["paths"]["output"] = args.output

    if args.model:
        config["model"] = args.model

    if args.prompt_version:
        config["prompt_version"] = args.prompt_version

    if args.skip_cache:
        config["cache"]["read_enabled"] = False

    config["runtime"]["limit"] = args.limit
    config["runtime"]["reprocess"] = args.reprocess
    config["runtime"]["debug"] = args.debug
    config["runtime"]["show_config"] = args.show_config

    return config
