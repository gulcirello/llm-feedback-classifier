import pandas as pd


def print_summary(df: pd.DataFrame) -> None:
    if df.empty:
        print("No results to summarize.")
        return

    required_columns = [
        "primary_theme",
        "sentiment",
        "needs_review",
        "confidence",
    ]

    missing = [column for column in required_columns if column not in df.columns]

    if missing:
        print(f"Missing columns: {missing}")
        return

    print_section("Summary")

    review_count = int(df["needs_review"].sum())
    review_ratio = review_count / len(df)

    print(f"Rows processed: {len(df)}")
    print(f"Review queue: {review_count}/{len(df)} ({review_ratio:.1%})")

    print_section("Theme distribution")
    print_distribution(df["primary_theme"])

    print_section("Sentiment distribution")
    print_distribution(df["sentiment"])

    print_section("Lowest confidence")
    print_lowest_confidence(df)


def print_section(title: str) -> None:
    print(f"\n=== {title} ===")


def print_distribution(series: pd.Series) -> None:
    counts = series.value_counts()

    for label, count in counts.items():
        print(f"{str(label):<30} {count:>3}")


def print_lowest_confidence(df: pd.DataFrame, limit: int = 5) -> None:
    lowest_confidence = df.sort_values("confidence").head(limit)
    print("\nScore | Theme                    | Comment")
    print("-" * 70)

    for _, row in lowest_confidence.iterrows():
        confidence = float(row["confidence"])
        primary_theme = str(row["primary_theme"])
        comment = truncate(str(row["comment"]), 56)

        print(f"{confidence:.2f} | {primary_theme:<24} | {comment}")


def truncate(text: str, max_length: int) -> str:
    if len(text) <= max_length:
        return text

    return text[: max_length - 3] + "..."
