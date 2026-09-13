"""Compare predefined thresholds on simulated validation data only.

Fit one logistic model on training data, then reuse its validation scores.
Teacher-provided scaffolding; no test access, file writes, or final selection.
"""

from pathlib import Path

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, roc_auc_score


DATA_DIR = Path(__file__).resolve().parent / "data"
FEATURE_COLUMNS = ["past_active_days_7d", "past_order_count_7d"]
TARGET_COLUMN = "inactive_next_7d"
THRESHOLDS = [0.3, 0.4, 0.5]


def format_metric(value):
    return "undefined" if value is None else f"{value:.4f}"


def main():
    train = pd.read_csv(DATA_DIR / "development_train.csv", encoding="utf-8-sig")
    valid = pd.read_csv(DATA_DIR / "development_valid.csv", encoding="utf-8-sig")
    if train.empty or valid.empty:
        raise ValueError("Training and validation data must both be nonempty.")
    if not train["prediction_date"].isin(["2026-06-01", "2026-07-01"]).all():
        raise ValueError("Training must use June/July snapshots only.")
    if not valid["prediction_date"].eq("2026-08-01").all():
        raise ValueError("Validation must use August snapshots only.")
    for frame in (train, valid):
        if not frame[TARGET_COLUMN].isin([0, 1]).all():
            raise ValueError("Labels must be known binary values: 0 or 1.")
        if frame[FEATURE_COLUMNS].isna().any().any():
            raise ValueError("Missing features require a training-only handling plan.")
    if train[TARGET_COLUMN].nunique() != 2:
        raise ValueError("Logistic regression requires both training classes.")

    X_train = train[FEATURE_COLUMNS]
    y_train = train[TARGET_COLUMN]
    X_valid = valid[FEATURE_COLUMNS]
    y_valid = valid[TARGET_COLUMN]

    # Train once. Threshold changes below do not retrain this model.
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)
    positive_column = list(model.classes_).index(1)
    inactive_probability = model.predict_proba(X_valid)[:, positive_column]

    rows = []
    for threshold in THRESHOLDS:
        # Class 1 means completely inactive in the NEXT seven days.
        # This exercise explicitly includes probabilities equal to the cutoff.
        predictions = (inactive_probability >= threshold).astype(int)
        cm = confusion_matrix(y_valid, predictions, labels=[0, 1])
        tn, fp, fn, tp = (int(value) for value in cm.ravel())
        precision = tp / (tp + fp) if tp + fp else None
        recall = tp / (tp + fn) if tp + fn else None
        f1 = 2 * tp / (2 * tp + fp + fn) if 2 * tp + fp + fn else None
        rows.append({
            "threshold": f"{threshold:.1f}",
            "flagged": tp + fp,
            "tp": tp,
            "fp": fp,
            "fn": fn,
            "tn": tn,
            "precision": format_metric(precision),
            "recall": format_metric(recall),
            "f1": format_metric(f1),
            "accuracy": format_metric((tp + tn) / len(valid)),
        })

    auc = roc_auc_score(y_valid, inactive_probability) if y_valid.nunique() == 2 else None
    print("SIMULATED DATA: VALIDATION THRESHOLD COMPARISON ONLY")
    print("train_rows:", len(train))
    print("validation_rows:", len(valid))
    print("rule: predict class 1 when its probability >= threshold")
    print("threshold candidates were fixed before this run:", THRESHOLDS)
    print(pd.DataFrame(rows).to_string(index=False))
    print("flagged=reminder list size; tp=correct flags; fp=false alarms; fn=misses")
    print("roc_auc (same scores for every threshold):", format_metric(auc))
    print("The model was fitted once; only the decision threshold changed.")
    print("No final threshold was selected. Compare misses and reminder workload.")
    print("No files were written. Test features and test labels were not opened.")
    print("Simulated validation results do not establish real business impact.")


if __name__ == "__main__":
    main()
