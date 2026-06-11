import pprint

from src.cli import apply_cli_overrides, parse_cli_args
from src.config_loader import load_config
from src.pipeline import run_pipeline
from src.report import print_summary


def main() -> None:
    args = parse_cli_args()

    config = load_config()
    config = apply_cli_overrides(config, args)

    if config["runtime"]["show_config"]:
        pprint.pprint(config, sort_dicts=False)

    df = run_pipeline(config)
    print_summary(df)


if __name__ == "__main__":
    main()
