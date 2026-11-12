
from collections.abc import Iterable


def normalize_item(value: str) -> str:
    """Normalize values for comparison."""
    return " ".join(value.casefold().split())


def calculate_extraction_metrics(
    predicted: Iterable[str],
    expected: Iterable[str],
) -> dict:
    """Calculate set-based precision, recall, and F1."""

    predicted_set = {
        normalize_item(item) for item in predicted
    }
    expected_set = {
        normalize_item(item) for item in expected
    }

    true_positives = len(predicted_set & expected_set)
    false_positives = len(predicted_set - expected_set)
    false_negatives = len(expected_set - predicted_set)

    precision = (
        true_positives / (true_positives + false_positives)
        if predicted_set else 0.0
    )

    recall = (
        true_positives / (true_positives + false_negatives)
        if expected_set else 0.0
    )

    f1 = (
        2 * precision * recall / (precision + recall)
        if precision + recall else 0.0
    )

    return {
        "precision": round(precision, 3),
        "recall": round(recall, 3),
        "f1": round(f1, 3),
        "true_positives": true_positives,
        "false_positives": false_positives,
        "false_negatives": false_negatives,
        "unexpected": sorted(predicted_set - expected_set),
        "missed": sorted(expected_set - predicted_set),
    }
