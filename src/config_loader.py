from pathlib import Path
import yaml


def load_yaml(path: str) -> dict:
    with Path(path).open("r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def load_config(
    app_config_path: str = "config/app.yaml",
    taxonomy_config_path: str = "config/taxonomy.yaml",
) -> dict:
    app_config = load_yaml(app_config_path)
    taxonomy_config = load_yaml(taxonomy_config_path)

    return {
        **app_config,
        "taxonomy": taxonomy_config,
    }
