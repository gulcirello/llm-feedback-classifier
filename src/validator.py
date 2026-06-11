def validate_result(
    result: dict,
    comment: str,
    taxonomy: dict,
    confidence_threshold: float,
) -> dict:
    primary = result.get("primary_theme")
    secondary = result.get("secondary_theme")
    sentiment = result.get("sentiment")
    confidence = result.get("confidence")
    needs_review = result.get("needs_review", False)

    if primary not in taxonomy["themes"]:
        primary = "Other"
        needs_review = True

    if secondary in ("", "null", None):
        secondary = None

    if secondary is not None and secondary not in taxonomy["themes"]:
        secondary = None
        needs_review = True

    if secondary == primary:
        secondary = None
        needs_review = True

    if sentiment not in taxonomy["sentiments"]:
        sentiment = "mixed"
        needs_review = True

    try:
        confidence = float(confidence)

    except (TypeError, ValueError):
        confidence = 0.0
        needs_review = True

    confidence = max(0.0, min(1.0, confidence))

    if confidence < confidence_threshold:
        needs_review = True

    normalized_comment = comment.lower().strip()

    if not normalized_comment:
        needs_review = True

    if len(normalized_comment) < 5:
        needs_review = True

    if primary == "Compensation & Benefits":
        compensation_keywords = taxonomy["validation"]["compensation_keywords"]

        has_compensation_keyword = any(
            keyword in normalized_comment for keyword in compensation_keywords
        )

        if not has_compensation_keyword:
            needs_review = True

    return {
        "primary_theme": primary,
        "secondary_theme": secondary,
        "sentiment": sentiment,
        "confidence": confidence,
        "needs_review": needs_review,
    }
